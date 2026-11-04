import math
import itertools
import time
import random
import matplotlib.pyplot as plt


class TSPSolver:
    def __init__(self, cities):
        """
        :param cities: 城市座標字典，例如 {'A': (x1, y1), 'B': (x2, y2), ...}
        """
        self.cities = cities
        self.city_names = list(cities.keys())
        self.n = len(self.city_names)

    def _dist(self, c1, c2):
        """計算兩城市間的歐氏距離"""
        p1 = self.cities[c1]
        p2 = self.cities[c2]
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def calculate_path_cost(self, path):
        """計算閉合迴圈路徑的總長度 (包含回到起點)"""
        cost = 0.0
        for i in range(len(path)):
            cost += self._dist(path[i], path[(i + 1) % len(path)])
        return cost

    # -------------------------------------------------------------
    # 方法 1：暴力列舉法 (Brute Force) - 保證全局最佳，但複雜度 O(n!)
    # -------------------------------------------------------------
    def solve_brute_force(self):
        start_time = time.perf_counter()
        start_city = self.city_names[0]
        other_cities = self.city_names[1:]

        best_path = None
        best_cost = float('inf')

        for perm in itertools.permutations(other_cities):
            current_path = [start_city] + list(perm)
            current_cost = self.calculate_path_cost(current_path)
            if current_cost < best_cost:
                best_cost = current_cost
                best_path = current_path

        elapsed = time.perf_counter() - start_time
        return best_path, best_cost, elapsed

    # -------------------------------------------------------------
    # 方法 2：最近鄰居貪婪法 (Nearest Neighbor Heuristic) - O(n^2)
    # -------------------------------------------------------------
    def solve_nearest_neighbor(self):
        start_time = time.perf_counter()
        unvisited = set(self.city_names)
        current = self.city_names[0]
        path = [current]
        unvisited.remove(current)

        while unvisited:
            next_city = min(unvisited, key=lambda city: self._dist(current, city))
            path.append(next_city)
            unvisited.remove(next_city)
            current = next_city

        cost = self.calculate_path_cost(path)
        elapsed = time.perf_counter() - start_time
        return path, cost, elapsed

    # -------------------------------------------------------------
    # 方法 3：2-Opt 局部搜尋演算法 (2-Opt Local Search)
    # -------------------------------------------------------------
    def solve_2opt(self, initial_path=None):
        start_time = time.perf_counter()
        if initial_path is None:
            # 預設以貪婪法的結果作為初始解
            path, _, _ = self.solve_nearest_neighbor()
        else:
            path = list(initial_path)

        improved = True
        best_cost = self.calculate_path_cost(path)

        while improved:
            improved = False
            for i in range(1, self.n - 1):
                for j in range(i + 1, self.n):
                    # 進行邊反轉 (2-Opt Swap)
                    new_path = path[:i] + path[i:j][::-1] + path[j:]
                    new_cost = self.calculate_path_cost(new_path)

                    if new_cost < best_cost - 1e-9:
                        path = new_path
                        best_cost = new_cost
                        improved = True
                        break
                if improved:
                    break

        elapsed = time.perf_counter() - start_time
        return path, best_cost, elapsed

    # -------------------------------------------------------------
    # 視覺化比較與繪圖
    # -------------------------------------------------------------
    def plot_comparison(self, solutions, filename="tsp_comparison.png"):
        fig, axes = plt.subplots(1, len(solutions), figsize=(6 * len(solutions), 5))
        if len(solutions) == 1:
            axes = [axes]

        for ax, (title, path, cost, elapsed) in zip(axes, solutions):
            # 繪製閉合路徑
            full_path = path + [path[0]]
            xs = [self.cities[c][0] for c in full_path]
            ys = [self.cities[c][1] for c in full_path]

            ax.plot(xs, ys, 'o-', color='#2b5c8f', markersize=8, linewidth=2, label='Path')
            
            # 起點標記為紅色
            start_c = path[0]
            ax.plot(self.cities[start_c][0], self.cities[start_c][1], 's', color='#d9534f', markersize=10, label='Start')

            for city, (x, y) in self.cities.items():
                ax.annotate(f" {city}", (x, y), fontsize=11, fontweight='bold')

            ax.set_title(f"{title}
Cost: {cost:.2f} | Time: {elapsed:.5f}s", fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.legend(loc='upper right')

        plt.tight_layout()
        plt.savefig(filename, dpi=300)
        plt.close()
        print(f"--> 圖表已儲存為：{filename}")


def main():
    print("=" * 60)
    print("   旅行推銷員問題 (TSP) 多演算法求解與性能評測")
    print("=" * 60)

    # 隨機產生 9 個城市座標（保證暴力搜尋可以在數秒內完成比對）
    random.seed(42)
    num_cities = 9
    city_names = [f"City_{i+1}" for i in range(num_cities)]
    cities = {name: (round(random.uniform(10, 90), 2), round(random.uniform(10, 90), 2)) for name in city_names}

    solver = TSPSolver(cities)

    print(f"城市數量: {num_cities} 個")
    for name, pos in cities.items():
        print(f"  {name}: {pos}")
    print("-" * 60)

    # 1. 暴力法
    print("1. 正在執行【暴力法 (Brute Force)】...")
    bf_path, bf_cost, bf_time = solver.solve_brute_force()
    print(f"   最佳路徑長度: {bf_cost:.4f} | 耗時: {bf_time:.5f} 秒")

    # 2. 貪婪最近鄰居法
    print("2. 正在執行【最近鄰居貪婪法 (Nearest Neighbor)】...")
    nn_path, nn_cost, nn_time = solver.solve_nearest_neighbor()
    print(f"   路徑長度: {nn_cost:.4f} | 耗時: {nn_time:.5f} 秒")

    # 3. 2-Opt 局部優化
    print("3. 正在執行【2-Opt 局部優化法 (2-Opt Search)】...")
    opt_path, opt_cost, opt_time = solver.solve_2opt(nn_path)
    print(f"   路徑長度: {opt_cost:.4f} | 耗時: {opt_time:.5f} 秒")

    print("=" * 60)
    print("綜合比較：")
    print(f" - 暴力法 (全局最佳) : 長度 = {bf_cost:.2f}, 耗時 = {bf_time:.5f}s")
    print(f" - 貪婪法 (啟發式)   : 長度 = {nn_cost:.2f}, 耗時 = {nn_time:.5f}s, 差距 = {((nn_cost - bf_cost) / bf_cost * 100):+.2f}%")
    print(f" - 2-Opt 優化法      : 長度 = {opt_cost:.2f}, 耗時 = {opt_time:.5f}s, 差距 = {((opt_cost - bf_cost) / bf_cost * 100):+.2f}%")

    # 產出視覺化圖表
    solutions = [
        ("Brute Force (Exact)", bf_path, bf_cost, bf_time),
        ("Nearest Neighbor", nn_path, nn_cost, nn_time),
        ("2-Opt Optimized", opt_path, opt_cost, opt_time)
    ]
    solver.plot_comparison(solutions, filename="tsp_comparison.png")


if __name__ == "__main__":
    main()
