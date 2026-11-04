"""方法 2：爬山演算法 (Hill Climbing)

原理：
隨機或局部探尋相鄰解（例如隨機交換兩個城市位置 2-Exchange）。
只要鄰居解的成本比當前解好就直接移過去；當達到最大探索步數或周遭無法再前進時即停止。
特點：速度快，但極易卡在局部極佳值 (Local Optimum)。
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


def solve_hill_climbing(cities, max_iter=3000):
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

    # 隨機初始解
    current_path = list(names)
    random.shuffle(current_path)
    current_cost = calculate_cost(current_path, dist)

    for _ in range(max_iter):
        # 隨機產生 2-Exchange 鄰近解
        i, j = random.sample(range(n), 2)
        neighbor = list(current_path)
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        neighbor_cost = calculate_cost(neighbor, dist)

        # 只要成本下降就前進 (爬山)
        if neighbor_cost < current_cost:
            current_path = neighbor
            current_cost = neighbor_cost

    return current_path, current_cost


if __name__ == "__main__":
    random.seed(42)
    test_cities = {
        f"C{i+1:02d}": (
            round(random.uniform(0, 100), 2),
            round(random.uniform(0, 100), 2),
        )
        for i in range(16)
    }

    print("=== 方法 2：爬山演算法 (Hill Climbing) ===")
    t0 = time.perf_counter()
    best_path, cost = solve_hill_climbing(test_cities, max_iter=4000)
    elapsed = time.perf_counter() - t0

    print(f"最佳路徑總長度: {cost:.2f}")
    print(f"計算耗時: {elapsed:.5f} 秒")
    print(f"路徑順序: {' -> '.join(best_path)} -> {best_path[0]}")
