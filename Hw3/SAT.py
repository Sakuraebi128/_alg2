import itertools
import re


class TruthTableSATSolver:

    def __init__(self, formula_str):
        """formula_str: 邏輯表達式字串。

        支援語法：
          - 變數：如 A, B, C, x1, x2 (英文字母開頭的識別字)
          - 運算子：
              否定 NOT :  ~ 或 not
              交集 AND :  & 或 and
              聯集 OR  :  | 或 or
              蘊涵 IMPLIES (P -> Q) :  ->
              雙條件 IFF (P <-> Q)   :  <->
              異或 XOR :  ^ 或 xor
        """
        self.raw_formula = formula_str
        self.variables = self._extract_variables(formula_str)
        self.python_expr = self._convert_to_python_expr(formula_str)

    def _extract_variables(self, expr):
        """提取表達式中所有相異的變數名稱"""
        tokens = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", expr)
        keywords = {"and", "or", "not", "xor", "True", "False"}
        variables = sorted(list(set(t for t in tokens if t not in keywords)))
        return variables

    def _convert_to_python_expr(self, expr):
        """將常見命題邏輯符號轉為 Python 合法運算子

        P -> Q  等價於  (not P or Q)
        P <-> Q 等價於  (P == Q)
        """
        # 替換雙條件 <->
        expr = re.sub(
            r"([a-zA-Z0-9_]+)\s*<->\s*([a-zA-Z0-9_]+)", r"(\1 == \2)", expr
        )
        # 替換蘊涵 ->
        expr = re.sub(
            r"([a-zA-Z0-9_]+)\s*->\s*([a-zA-Z0-9_]+)",
            r"(not \1 or \2)",
            expr,
        )

        # 替換邏輯符號
        expr = expr.replace("~", " not ")
        expr = expr.replace("&", " and ")
        expr = expr.replace("|", " or ")
        expr = expr.replace("^", " != ")  # 邏輯 XOR 等價於 !=
        return expr

    def evaluate(self, assignment):
        """代入單一組賦值計算真假值"""
        # assignment 格式如 {'A': True, 'B': False}
        return bool(eval(self.python_expr, {}, assignment))

    def solve(self, print_table=True):
        """系統性列舉真值表並求解 SAT"""
        n = len(self.variables)
        satisfying_models = []

        # 格式化表格欄位
        col_width = 8
        headers = self.variables + ["Result"]

        if print_table:
            print(f"\n原始式子: {self.raw_formula}")
            print(f"內部邏輯式: {self.python_expr}")
            print("=" * (col_width * len(headers)))
            header_row = "".join(f"{h:^{col_width}}" for h in headers)
            print(header_row)
            print("-" * (col_width * len(headers)))

        # 系統性生成 2^n 種賦值：(False, True) 的笛卡兒積
        for values in itertools.product([True, False], repeat=n):
            assignment = dict(zip(self.variables, values))
            result = self.evaluate(assignment)

            if result:
                satisfying_models.append(assignment)

            if print_table:
                row_str = "".join(
                    f"{'T' if v else 'F':^{col_width}}" for v in values
                )
                res_str = f"{'T' if result else 'F':^{col_width}}"
                print(row_str + res_str)

        if print_table:
            print("=" * (col_width * len(headers)))

        # 輸出 SAT 結果
        if satisfying_models:
            print(
                f"\n[SATISFIABLE] 共有 {len(satisfying_models)} 組解可使式子為真："
            )
            for i, model in enumerate(satisfying_models, 1):
                formatted_model = ", ".join(
                    f"{k}={v}" for k, v in model.items()
                )
                print(f"  解 {i}: {formatted_model}")
        else:
            print("\n[UNSATISFIABLE] 無解（無論變數如何賦值，式子恆為假）。")

        return satisfying_models


# ================= 測試示範 =================
if __name__ == "__main__":
    # 範例 1：可滿足表達式 (A 或 B) 且 (非 A 或 C)
    f1 = "(A | B) & (~A | C)"
    solver1 = TruthTableSATSolver(f1)
    solver1.solve()

    # 範例 2：不可滿足表達式 (矛盾式) A 且 非 A
    f2 = "A & ~A"
    solver2 = TruthTableSATSolver(f2)
    solver2.solve()

    # 範例 3：含蘊涵的式子 (A -> B) & A
    f3 = "(A -> B) & A"
    solver3 = TruthTableSATSolver(f3)
    solver3.solve()
