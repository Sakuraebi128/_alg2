import itertools
import re


# =====================================================================
# 1. 語法樹 AST 定義
# =====================================================================
class AST:
    pass


class Var(AST):
    """變數：x"""

    def __init__(self, name):
        self.name = name

    def free_vars(self):
        return {self.name}

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, Var) and self.name == other.name

    def __hash__(self):
        return hash(self.name)


class Abs(AST):
    """抽象（Abstraction / Function）：\var. body"""

    def __init__(self, var, body):
        self.var = var  # str
        self.body = body  # AST

    def free_vars(self):
        return self.body.free_vars() - {self.var}

    def __str__(self):
        return f"(λ{self.var}. {self.body})"

    def __eq__(self, other):
        return (
            isinstance(other, Abs)
            and self.var == other.var
            and self.body == other.body
        )


class App(AST):
    """應用（Application）：(func arg)"""

    def __init__(self, func, arg):
        self.func = func  # AST
        self.arg = arg  # AST

    def free_vars(self):
        return self.func.free_vars() | self.arg.free_vars()

    def __str__(self):
        return f"({self.func} {self.arg})"

    def __eq__(self, other):
        return (
            isinstance(other, App)
            and self.func == other.func
            and self.arg == other.arg
        )


# =====================================================================
# 2. 變數置換與 Alpha 轉換（避免 Variable Capture）
# =====================================================================
_var_counter = itertools.count(1)


def fresh_var(base="v"):
    """生成不會重複的新變數名稱"""
    return f"{base}_{next(_var_counter)}"


def substitute(expr, var_name, replacement):
    """執行 [var_name |-> replacement] expr 置換"""
    if isinstance(expr, Var):
        return replacement if expr.name == var_name else expr

    elif isinstance(expr, App):
        return App(
            substitute(expr.func, var_name, replacement),
            substitute(expr.arg, var_name, replacement),
        )

    elif isinstance(expr, Abs):
        if expr.var == var_name:
            # 變數被遮蔽，停止向下置換
            return expr

        # 若綁定變數出現在 replacement 的自由變數中，需做 alpha-conversion (重新命名)
        if expr.var in replacement.free_vars():
            new_v = fresh_var(expr.var)
            renamed_body = substitute(expr.body, expr.var, Var(new_v))
            return Abs(
                new_v, substitute(renamed_body, var_name, replacement)
            )

        return Abs(expr.var, substitute(expr.body, var_name, replacement))


# =====================================================================
# 3. 正規序單步化簡 (Normal-Order Step Reduction)
# =====================================================================
def step_reduce(expr):
    """嘗試執行單步 beta-reduction (最左最外層優先)。

    若可化簡，回傳 (True, new_expr, explanation)；若已是正規形 (Normal Form)，回傳 (False, expr, "")
    """
    if isinstance(expr, Var):
        return False, expr, ""

    elif isinstance(expr, Abs):
        reduced, new_body, note = step_reduce(expr.body)
        if reduced:
            return True, Abs(expr.var, new_body), note
        return False, expr, ""

    elif isinstance(expr, App):
        # 核心情況：(λx. body) arg  -> 觸發 beta-reduction
        if isinstance(expr.func, Abs):
            applied_abs = expr.func
            arg_val = expr.arg
            new_expr = substitute(applied_abs.body, applied_abs.var, arg_val)
            note = f"β-約簡: (λ{applied_abs.var}. ...) 套用引數 {arg_val}"
            return True, new_expr, note

        # 先化簡左側函式
        reduced, new_func, note = step_reduce(expr.func)
        if reduced:
            return True, App(new_func, expr.arg), note

        # 若左側不可化簡，再化簡右側引數
        reduced, new_arg, note = step_reduce(expr.arg)
        if reduced:
            return True, App(expr.func, new_arg), note

        return False, expr, ""


# =====================================================================
# 4. 詞法與語法解析器 (Lexer & Recursive Descent Parser)
# =====================================================================
def tokenize(s):
    # 支援 '\' 或 'λ' 作為 lambda 符號
    token_spec = [
        ("LAMBDA", r"[\\λ]"),
        ("DOT", r"\."),
        ("LPAREN", r"\("),
        ("RPAREN", r"\)"),
        ("IDENT", r"[a-zA-Z_][a-zA-Z0-9_]*"),
        ("SKIP", r"\s+"),
    ]
    tok_regex = "|".join(f"(?P<{pair[0]}>{pair[1]})" for pair in token_spec)
    tokens = []
    for mo in re.finditer(tok_regex, s):
        kind = mo.lastgroup
        if kind != "SKIP":
            tokens.append((kind, mo.group()))
    return tokens


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected_kind=None):
        tok = self.peek()
        if not tok:
            raise SyntaxError("非預期的語法結束 (Unexpected EOF)")
        if expected_kind and tok[0] != expected_kind:
            raise SyntaxError(
                f"預期為 {expected_kind}，但得到 {tok[0]} ('{tok[1]}')"
            )
        self.pos += 1
        return tok

    def parse_expr(self):
        """Expr -> Application"""
        return self.parse_app()

    def parse_app(self):
        """Application -> Atom+ (左結合)"""
        expr = self.parse_atom()
        while True:
            nxt = self.peek()
            if (
                nxt
                and nxt[0] in ("IDENT", "LPAREN", "LAMBDA")
                and nxt[0] != "RPAREN"
            ):
                arg = self.parse_atom()
                expr = App(expr, arg)
            else:
                break
        return expr

    def parse_atom(self):
        """Atom -> Var | '(' Expr ')' | Lambda"""
        tok = self.peek()
        if not tok:
            raise SyntaxError("表達式未完成")

        if tok[0] == "IDENT":
            self.consume("IDENT")
            return Var(tok[1])

        elif tok[0] == "LPAREN":
            self.consume("LPAREN")
            expr = self.parse_expr()
            self.consume("RPAREN")
            return expr

        elif tok[0] == "LAMBDA":
            self.consume("LAMBDA")
            vars_list = []
            while self.peek() and self.peek()[0] == "IDENT":
                vars_list.append(self.consume("IDENT")[1])

            if not vars_list:
                raise SyntaxError("Lambda 宣告後方缺少參數")

            self.consume("DOT")
            body = self.parse_expr()

            # 展開多參數：\x y. body  =>  \x. (\y. body)
            for v in reversed(vars_list):
                body = Abs(v, body)
            return body

        raise SyntaxError(f"語法錯誤，非預期的 Token: {tok[1]}")


def parse(code_str):
    tokens = tokenize(code_str)
    parser = Parser(tokens)
    return parser.parse_expr()


# =====================================================================
# 5. 解譯評估器（逐步追蹤執行過程）
# =====================================================================
def interpret(code, max_steps=50):
    print("=" * 65)
    print(f"輸入表達式: {code}")
    ast = parse(code)
    print(f"解析 AST  : {ast}")
    print("-" * 65)

    current = ast
    step = 0

    while step < max_steps:
        reduced, next_expr, note = step_reduce(current)
        if not reduced:
            print(f"\n[達成正規形 (Normal Form)] 經過 {step} 步化簡。")
            print(f"最終結果: {current}")
            print("=" * 65 + "\n")
            return current

        step += 1
        print(f"步驟 {step:02d}: {note}")
        print(f"        -> {next_expr}")
        current = next_expr

    print(f"\n[警告] 超過最大化簡步數 ({max_steps})，可能為非終止循環 (如 Ω 組合子)。")
    print(f"中斷狀態: {current}")
    print("=" * 65 + "\n")
    return current


# =====================================================================
# 6. 經典實例測試
# =====================================================================
if __name__ == "__main__":
    # 範例 1：基本的恆等函式與自乘 (I 組合子)
    # (\x. x) y
    interpret(r"(\x. x) y")

    # 範例 2：邱奇布林值邏輯 - NOT TRUE == FALSE
    # TRUE  := \x y. x
    # FALSE := \x y. y
    # NOT   := \b. b FALSE TRUE
    # 展開測試： (\b. b (\x y. y) (\x y. x)) (\x y. x)
    interpret(r"(\b. b (\x y. y) (\x y. x)) (\x y. x)")

    # 範例 3：變數捕捉與 Alpha 轉換測試
    # (\x y. x) y  --> y 不能被內層的 y 捕捉，內層 y 需自動重命名
    interpret(r"(\x. \y. x) y")

    # 範例 4：邱奇數加法 1 + 1 == 2
    # ONE  := \f x. f x
    # PLUS := \m n f x. m f (n f x)
    # (PLUS ONE ONE)
    church_add = (
        r"(\m n f x. m f (n f x)) "
        r"(\f x. f x) "
        r"(\f x. f x)"
    )
    interpret(church_add)
