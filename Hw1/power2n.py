import time

memo = {}


def power2n_1(n):
    return 2**n


def power2n_2b(n):
    if n == 0:
        return 1
    return 2 * power2n_2b(n - 1)


def power2n_3(n):
    if n == 0:
        return 1
    if n in memo:
        return memo[n]
    memo[n] = power2n_3(n - 1) + power2n_3(n - 1)
    return memo[n]


n = 100
print(f"=== 測試 n = {n} ===")

# 方法 1
t0 = time.perf_counter()
ans1 = power2n_1(n)
t1 = time.perf_counter()
print(f"方法 1 (2**n)            : 耗時 {t1 - t0:.8f} 秒")

# 方法 2b
t0 = time.perf_counter()
ans2b = power2n_2b(n)
t1 = time.perf_counter()
print(f"方法 2b (2 * f(n-1))     : 耗時 {t1 - t0:.8f} 秒")

# 方法 3
memo.clear()
t0 = time.perf_counter()
ans3 = power2n_3(n)
t1 = time.perf_counter()
print(f"方法 3 (遞迴 + 查表)      : 耗時 {t1 - t0:.8f} 秒")

# 方法 2a
print("方法 2a (f(n-1) + f(n-1)): [必須跳過] 需運算 2^100 次，需耗費數兆年")

print("\n2^100 計算結果 (共 31 位數):")
print(ans1)
