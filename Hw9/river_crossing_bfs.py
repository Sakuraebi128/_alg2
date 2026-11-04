"""問題 2：狼羊甘藍菜過河問題 (Wolf, Goat, and Cabbage Problem)

使用演算法：狀態圖廣度優先搜尋 (State-Space BFS)
特性：精確枚舉有限離散合法狀態，找出無人傷亡的最短渡河步驟。
"""

from collections import deque


def is_valid_state(state):
    """state 為四元組 (F, W, G, C)，1 代表在右岸，0 代表在左岸。

    約束條件：農夫不在場時，狼不能與羊同岸，羊不能與甘藍菜同岸。
    """
    f, w, g, c = state
    if w == g and f != w:
        return False
    if g == c and f != g:
        return False
    return True


def solve_river_crossing():
    initial_state = (0, 0, 0, 0)  # 起初全部在左岸
    goal_state = (1, 1, 1, 1)  # 目標全部到右岸

    queue = deque([(initial_state, [])])
    visited = {initial_state}

    while queue:
        curr_state, history = queue.popleft()
        if curr_state == goal_state:
            return history + [(curr_state, "已全員安全抵達右岸")]

        f, w, g, c = curr_state
        next_f = 1 - f  # 農夫每次必定過河

        # 可能的動作：農夫單獨過河，或者帶任一與他同岸的物件過河
        candidates = [
            ((next_f, w, g, c), "農夫獨自過河"),
        ]
        if w == f:
            candidates.append(((next_f, 1 - w, g, c), "農夫帶【狼】過河"))
        if g == f:
            candidates.append(((next_f, w, 1 - g, c), "農夫帶【羊】過河"))
        if c == f:
            candidates.append(((next_f, w, g, 1 - c), "農夫帶【甘藍菜】過河"))

        for nxt_state, action in candidates:
            if is_valid_state(nxt_state) and nxt_state not in visited:
                visited.add(nxt_state)
                target_bank = "右岸" if next_f == 1 else "左岸"
                step_desc = f"{action} -> 前往{target_bank}"
                queue.append((nxt_state, history + [(curr_state, step_desc)]))

    return None


if __name__ == "__main__":
    print("=== 2. 狼羊甘藍菜過河問題 (狀態圖 BFS) ===")
    solution = solve_river_crossing()
    if solution:
        print(f"找到成功渡河步驟，共 {len(solution) - 1} 步：")
        for idx, (st, act) in enumerate(solution):
            f, w, g, c = st
            left_bank = [
                name
                for name, loc in zip(
                    ["農夫", "狼", "羊", "菜"], [f, w, g, c]
                )
                if loc == 0
            ]
            right_bank = [
                name
                for name, loc in zip(
                    ["農夫", "狼", "羊", "菜"], [f, w, g, c]
                )
                if loc == 1
            ]
            status = f"左岸: {left_bank} | 右岸: {right_bank}"
            if idx == len(solution) - 1:
                print(f"  完成: {status}")
            else:
                print(f"  步驟 {idx + 1:02d}: {act:<20} [現狀 -> {status}]")
    else:
        print("無解！")
