"""問題 5：IC 設計中的電路繞線問題 (VLSI / PCB Routing)

使用演算法：李氏繞線演算法 (Lee's Maze Router / 3D Grid Wave Propagation)
特性：透過波前擴展與貫孔 (Via) 跨層切換，保證找出滿足設計規則的最短導線路徑。
"""

from collections import deque


def solve_ic_routing_lee(layers, pin_a, pin_b, via_cost=3):
    """layers: 三維網格矩陣 [z][y][x]，0 為可走佈線區，1 為既有金屬障礙或不可繞線區

    pin_a: 起始接腳 (layer, y, x)
    pin_b: 目標接腳 (layer, y, x)
    via_cost: 打貫孔跨層的代價
    return: (繞線座標列表, 總繞線代價)
    """
    num_layers = len(layers)
    height = len(layers[0])
    width = len(layers[0][0])

    queue = deque([pin_a])
    cost_grid = {pin_a: 0}
    parent = {}
    found = False

    planar_moves = [(0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]
    via_moves = [(-1, 0, 0), (1, 0, 0)]

    while queue:
        curr = queue.popleft()
        if curr == pin_b:
            found = True
            break

        lz, ly, lx = curr
        curr_cost = cost_grid[curr]

        # 1. 同金屬層平移擴展
        for dz, dy, dx in planar_moves:
            nz, ny, nx = lz + dz, ly + dy, lx + dx
            if 0 <= ny < height and 0 <= nx < width:
                if layers[nz][ny][nx] == 0:
                    nxt = (nz, ny, nx)
                    new_cost = curr_cost + 1
                    if nxt not in cost_grid or new_cost < cost_grid[nxt]:
                        cost_grid[nxt] = new_cost
                        parent[nxt] = curr
                        queue.append(nxt)

        # 2. 跨層打貫孔 (Via) 擴展
        for dz, dy, dx in via_moves:
            nz = lz + dz
            if 0 <= nz < num_layers:
                if layers[nz][ly][lx] == 0:
                    nxt = (nz, ly, lx)
                    new_cost = curr_cost + via_cost
                    if nxt not in cost_grid or new_cost < cost_grid[nxt]:
                        cost_grid[nxt] = new_cost
                        parent[nxt] = curr
                        queue.append(nxt)

    if not found:
        return None, float("inf")

    wire_path = []
    curr = pin_b
    while curr != pin_a:
        wire_path.append(curr)
        curr = parent[curr]
    wire_path.append(pin_a)
    wire_path.reverse()

    return wire_path, cost_grid[pin_b]


if __name__ == "__main__":
    M1 = [
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
    ]
    M2 = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]
    grid_3d = [M1, M2]

    pin_start = (0, 1, 0)
    pin_end = (0, 1, 4)

    print("=== 5. IC 電路繞線問題 (Lee 演算法 / 3D 網格波前擴展) ===")
    path, wire_cost = solve_ic_routing_lee(
        grid_3d, pin_start, pin_end, via_cost=2
    )
    if path:
        print(f"成功完成繞線！總佈線成本 (含 Via 貫孔): {wire_cost}")
        print("導線路徑節點 (層別, Y, X):")
        for step_idx, node in enumerate(path):
            via_tag = (
                " [打 Via 貫孔]"
                if step_idx > 0 and node[0] != path[step_idx - 1][0]
                else ""
            )
            print(
                f"  節點 {step_idx:02d}: M{node[0]+1} 層 (y={node[1]}, x={node[2]}){via_tag}"
            )
    else:
        print("無解：該線網無法完成繞線。")
