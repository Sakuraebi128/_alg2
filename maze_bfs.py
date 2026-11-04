"""問題 1：老鼠走迷宮問題 (Maze Routing)

使用演算法：廣度優先搜尋 (Breadth-First Search, BFS)
特性：保證在每步代價均等的前提下找到步數最少的最短路徑。
"""

from collections import deque


def solve_maze_bfs(maze, start, goal):
    """maze: 2D 二維網格串列 (0: 可通行通道, 1: 障礙物/牆壁)

    start: 起點座標 (row, col)
    goal: 終點座標 (row, col)
    return: (路徑串列, 探索節點數)
    """
    rows, cols = len(maze), len(maze[0])
    queue = deque([start])
    visited = {start}
    parent = {}

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 上、下、左、右

    found = False
    while queue:
        curr = queue.popleft()
        if curr == goal:
            found = True
            break

        r, c = curr
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if maze[nr][nc] == 0 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    parent[(nr, nc)] = (r, c)
                    queue.append((nr, nc))

    if not found:
        return None, len(visited)

    # 從終點回溯還原路徑
    path = []
    curr = goal
    while curr != start:
        path.append(curr)
        curr = parent[curr]
    path.append(start)
    path.reverse()

    return path, len(visited)


def print_maze_with_path(maze, path):
    path_set = set(path) if path else set()
    for r in range(len(maze)):
        line = []
        for c in range(len(maze[0])):
            if (r, c) == path[0]:
                line.append(" S ")
            elif (r, c) == path[-1]:
                line.append(" E ")
            elif (r, c) in path_set:
                line.append(" * ")
            elif maze[r][c] == 1:
                line.append("###")
            else:
                line.append(" . ")
        print("".join(line))


if __name__ == "__main__":
    sample_maze = [
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 1, 1, 1, 0, 1],
        [0, 0, 0, 0, 0, 0],
    ]
    start_pos = (0, 0)
    goal_pos = (4, 5)

    print("=== 1. 老鼠走迷宮問題 (BFS) ===")
    path, explored = solve_maze_bfs(sample_maze, start_pos, goal_pos)
    if path:
        print(
            f"找到最短路徑，總步數: {len(path) - 1} 步 (探索了 {explored} 個節點)"
        )
        print(f"路徑座標序列: {path}")
        print("\n迷宮路徑可視化 (* 代表老鼠路徑, S 起點, E 終點):")
        print_maze_with_path(sample_maze, path)
    else:
        print("無法從起點到達終點！")
