"""問題 3：八皇后問題 (8-Queens Problem)

使用演算法：深度優先搜尋 + 回溯剪枝 (DFS / Backtracking)
特性：透過行列與主副對角線快速判斷衝突，提早剪除無效分支。
"""


def solve_n_queens(n=8):
    """n: 棋盤維度 (預設為 8)

    return: 所有合法放置方案 (每個方案為長度為 n 的 list，queens[col] = row)
    """
    solutions = []
    queens = [-1] * n

    occupied_rows = set()
    occupied_diag1 = set()  # row - col
    occupied_diag2 = set()  # row + col

    def backtrack(col):
        if col == n:
            solutions.append(list(queens))
            return

        for row in range(n):
            d1 = row - col
            d2 = row + col

            # 剪枝判斷：檢查是否處於同一列或同一對角線上
            if (
                row in occupied_rows
                or d1 in occupied_diag1
                or d2 in occupied_diag2
            ):
                continue

            # 放置皇后
            queens[col] = row
            occupied_rows.add(row)
            occupied_diag1.add(d1)
            occupied_diag2.add(d2)

            backtrack(col + 1)

            # 回溯撤銷
            queens[col] = -1
            occupied_rows.remove(row)
            occupied_diag1.remove(d1)
            occupied_diag2.remove(d2)

    backtrack(0)
    return solutions


def print_board(solution):
    n = len(solution)
    for r in range(n):
        line = []
        for c in range(n):
            line.append(" Q " if solution[c] == r else " . ")
        print("".join(line))


if __name__ == "__main__":
    n = 8
    print("=== 3. 八皇后問題 (回溯法 DFS) ===")
    solutions = solve_n_queens(n)
    print(f"在 {n}x{n} 棋盤上總共找到 {len(solutions)} 組相異合法解。")
    print("\n印出第 1 組解的棋盤佈局：")
    print_board(solutions[0])
