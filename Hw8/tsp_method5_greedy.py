"""方法 5：貪婪演算法 (Nearest Neighbor Heuristic)

原理：
屬於構建法。從起始城市出發，每一步都在所有「尚未拜訪的城市」中挑選距離當前城市最近的那一個，
走完所有城市後直接閉合返回起點。計算速度極快 (O(N^2))，但最後幾步容易產生極長跨度。
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


def solve_greedy(cities, start_city=None):
    names = list(cities.keys())
    dist = {
        c1: {
            c2: math.hypot(
                cities[c1][0] - cities[c2][0], cities[c1][1] - cities[c2][1]
            )
            for c2 in names
        }
        for c1 in names
    }

    if start_city is None:
        start_city = names[0]

    unvisited = set(names)
    path = [start_city]
    unvisited.remove(start_city)
    current = start_city

    while unvisited:
        # 貪婪挑選最近的未訪問城市
        next_city = min(unvisited, key=lambda c: dist[current][c])
        path.append(next_city)
        unvisited.remove(next_city)
        current = next_city

    return path, calculate_cost(path, dist)


if __name__ == "__main__":
    random.seed(42)
    test_cities = {
        f"C{i+1:02d}": (
            round(random.uniform(0, 100), 2),
            round(random.uniform(0, 100), 2),
        )
        for i in range(16)
    }

    print("=== 方法 5：貪婪演算法 (Nearest Neighbor) ===")
    t0 = time.perf_counter()
    best_path, cost = solve_greedy(test_cities)
    elapsed = time.perf_counter() - t0

    print(f"最佳路徑總長度: {cost:.2f}")
    print(f"計算耗時: {elapsed:.5f} 秒")
    print(f"路徑順序: {' -> '.join(best_path)} -> {best_path[0]}")
