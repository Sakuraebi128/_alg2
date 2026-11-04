"""問題 4：NPC 搜尋玩家問題 (Game AI Pathfinding)

使用演算法：A* 啟發式搜尋演算法 (A* Search)
特性：結合實際路徑成本 g(n) 與曼哈頓啟發式距離 h(n)，快速高效尋找最優追捕軌跡。
"""

import heapq


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def solve_npc_pathfinding(grid_map, npc_pos, player_pos):
    """grid_map: 2D 地圖網格 (1: 平地成本1, 3: 泥濘沼澤成本3, 999: 障礙物不可通行)

    npc_pos: NPC 初始座標 (row, col)
    player_pos: 玩家座標 (row, col)
    return: (路徑串列, 總路徑成本, 探索節點數)
    """
    rows, cols = len(grid_map), len(grid_map[0])

    open_set = []
    heapq.heappush(open_set, (heuristic(npc_pos, player_pos), 0, npc_pos))

    g_score = {npc_pos: 0}
    parent = {}
    explored_count = 0

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while open_set:
        f, current_g, current = heapq.heappop(open_set)
        explored_count += 1

        if current == player_pos:
            path = []
            curr = player_pos
            while curr != npc_pos:
                path.append(curr)
                curr = parent[curr]
            path.append(npc_pos)
            path.reverse()
            return path, current_g, explored_count

        if current_g > g_score.get(current, float("inf")):
            continue

        r, c = current
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                terrain_cost = grid_map[nr][nc]
                if terrain_cost >= 999:
                    continue

                tentative_g = current_g + terrain_cost
                if tentative_g < g_score.get((nr, nc), float("inf")):
                    g_score[(nr, nc)] = tentative_g
                    parent[(nr, nc)] = current
                    f_cost = tentative_g + heuristic((nr, nc), player_pos)
                    heapq.heappush(open_set, (f_cost, tentative_g, (nr, nc)))

    return None, float("inf"), explored_count


if __name__ == "__main__":
    game_map = [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 999, 999, 999, 1, 3, 3, 1],
        [1, 1, 1, 999, 1, 3, 3, 1],
        [1, 999, 1, 999, 1, 1, 1, 1],
        [1, 999, 1, 1, 1, 999, 999, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ]
    npc_start = (0, 0)
    player_loc = (5, 7)

    print("=== 4. NPC 搜尋玩家問題 (A* 演算法) ===")
    path, cost, visited_cnt = solve_npc_pathfinding(
        game_map, npc_start, player_loc
    )
    if path:
        print(
            f"NPC 成功規劃出追擊路線！總移動耗費: {cost} (探索節點數: {visited_cnt})"
        )
        print(f"路線座標: {path}")
    else:
        print("路徑被封死，NPC 無法抵達玩家位置。")
