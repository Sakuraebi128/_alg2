def fibonacci_iterative(n):
    if n == 0:
        return 0
    if n == 1:
        return 1

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


f_520 = fibonacci_iterative(520)
print(f"F(520) = {f_520}")
print(f"位數 = {len(str(f_520))}")
