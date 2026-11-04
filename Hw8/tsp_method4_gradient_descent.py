"""方法 4：梯度下降法 (離散空間之最速下降法 Steepest Descent)

原理：
TSP 是離散排列問題，無法直接連續求導。在離散幾何中，相當於計算當前點在所有鄰域方向上的「數值差分梯度」。
最速下降法（Steepest Descent）在每一步枚舉所有可能的交換操作，嚴格選取能讓總距離縮短最多（負差分梯度最大）的方向推進。
"""

import math
import random
import time


def calculate_cost(path, dist_matrix):
    cost = 0.0
    n = len(path)
    for i in range(n):
        cost += dist_matrix[path[i]][path[(i + 1) % n]]
    return cost


def solve_steepest_descent(cities):
    names = list(cities.keys())
    n = len(names)

    dist = {
        c1: {
            c2: math.hypot(
                cities[c1][0] - cities[c2][0], cities[c1][1] - cities[c2][1]
            )
            for c2 in names
        }
        for c1 in names
    }

    path = list(names)
    random.shuffle(path)
    current_cost = calculate_cost(path, dist)

    while True:
        best_delta = 0.0
        best_move = None

        # 遍歷鄰域所有交換方向，找出負梯度最大的移動
        for i in range(n - 1):
            for j in range(i + 1, n):
                candidate = list(path)
                candidate[i], candidate[j] = candidate[j], candidate[i]
                cost = calculate_cost(candidate, dist)
                delta = cost - current_cost

                if delta < best_delta:
                    best_delta = delta
                    best_move = (i, j)

        # 梯度小於等於 0 的改善已不存在，達到離散駐點
        if best_move is None or best_delta >= -1e-9:
            break

        # 沿著最大負梯度方向更新狀態
        i, j = best_move
        path[i], path[j] = path[j], path[i]
        current_cost += best_delta

    return path, current_cost


if __name__ == "__main__":
    random.seed(42)
    test_cities = {
        f"C{i+1:02d}": (
            round(random.uniform(0, 100), 2),
            round(random.uniform(0, 100), 2),
        )
        for i in range(16)
    }

    print("=== 方法 4：梯度下降法 (最速下降 Steepest Descent) ===")
    t0 = time.perf_counter()
    best_path, cost = solve_steepest_descent(test_cities)
    elapsed = time.perf_counter() - t0

    print(f"最佳路徑總長度: {cost:.2f}")
    print(f"計算耗時: {elapsed:.5f} 秒")
    print(f"路徑順序: {' -> '.join(best_path)} -> {best_path[0]}")
