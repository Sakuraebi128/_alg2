"""方法 3：模擬退火法 (Simulated Annealing)

原理：
模擬高溫固體退火降溫的物理過程。
除了接受更好的鄰居解之外，在溫度 T 較高時，允許以 Metropolis 準則 P = exp(-delta / T) 接受劣解，
從而具備跳脫局部最佳解、尋找全域最優解的能力。
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


def solve_simulated_annealing(
    cities, t_start=100.0, t_end=1e-4, cooling_rate=0.995, iter_per_temp=50
):
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

    current_path = list(names)
    random.shuffle(current_path)
    current_cost = calculate_cost(current_path, dist)

    best_path = list(current_path)
    best_cost = current_cost

    temp = t_start

    while temp > t_end:
        for _ in range(iter_per_temp):
            # 隨機子片段反轉
            i, j = sorted(random.sample(range(n), 2))
            neighbor = (
                current_path[:i]
                + current_path[i : j + 1][::-1]
                + current_path[j + 1 :]
            )
            neighbor_cost = calculate_cost(neighbor, dist)

            delta = neighbor_cost - current_cost

            # Metropolis 機率接受判斷
            if delta < 0 or random.random() < math.exp(-delta / temp):
                current_path = neighbor
                current_cost = neighbor_cost

                if current_cost < best_cost:
                    best_path = list(current_path)
                    best_cost = current_cost

        temp *= cooling_rate

    return best_path, best_cost


if __name__ == "__main__":
    random.seed(42)
    test_cities = {
        f"C{i+1:02d}": (
            round(random.uniform(0, 100), 2),
            round(random.uniform(0, 100), 2),
        )
        for i in range(16)
    }

    print("=== 方法 3：模擬退火法 (Simulated Annealing) ===")
    t0 = time.perf_counter()
    best_path, cost = solve_simulated_annealing(test_cities)
    elapsed = time.perf_counter() - t0

    print(f"最佳路徑總長度: {cost:.2f}")
    print(f"計算耗時: {elapsed:.5f} 秒")
    print(f"路徑順序: {' -> '.join(best_path)} -> {best_path[0]}")
