"""方法 1：改良法 (2-Opt Improvement Heuristic)

原理：
從給定的初始路徑出發，系統性地枚舉兩條邊並進行「反轉替換」(2-Opt Swap)。
只要新產生的路徑總長度縮短，就立即採納該改變，直到所有相交與次優邊都被解開、無法再改善為止。
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


def solve_2opt(cities, initial_path=None):
    names = list(cities.keys())
    n = len(names)

    # 建立歐氏距離矩陣
    dist = {
        c1: {
            c2: math.hypot(
                cities[c1][0] - cities[c2][0], cities[c1][1] - cities[c2][1]
            )
            for c2 in names
        }
        for c1 in names
    }

    if initial_path is None:
        path = list(names)
        random.shuffle(path)
    else:
        path = list(initial_path)

    improved = True
    best_cost = calculate_cost(path, dist)

    while improved:
        improved = False
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                # 執行邊翻轉
                new_path = path[:i] + path[i:j][::-1] + path[j:]
                new_cost = calculate_cost(new_path, dist)

                if new_cost < best_cost - 1e-9:
                    path = new_path
                    best_cost = new_cost
                    improved = True
                    break
            if improved:
                break

    return path, best_cost


if __name__ == "__main__":
    random.seed(42)
    # 建立 16 個隨機城市測試環境
    test_cities = {
        f"C{i+1:02d}": (
            round(random.uniform(0, 100), 2),
            round(random.uniform(0, 100), 2),
        )
        for i in range(16)
    }

    print("=== 方法 1：改良法 (2-Opt) ===")
    t0 = time.perf_counter()
    best_path, cost = solve_2opt(test_cities)
    elapsed = time.perf_counter() - t0

    print(f"最佳路徑總長度: {cost:.2f}")
    print(f"計算耗時: {elapsed:.5f} 秒")
    print(f"路徑順序: {' -> '.join(best_path)} -> {best_path[0]}")
