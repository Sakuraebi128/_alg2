def simplify(expr):
    """遞迴化簡代數常數 (例如 0*x -> 0, 1*x -> x, 0+x -> x)"""
    if not isinstance(expr, tuple):
        return expr

    op = expr[0]
    args = [simplify(arg) for arg in expr[1:]]

    if op == "+":
        u, v = args
        if u == 0:
            return v
        if v == 0:
            return u
        if isinstance(u, (int, float)) and isinstance(v, (int, float)):
            return u + v
        return ("+", u, v)

    elif op == "-":
        u, v = args
        if v == 0:
            return u
        if u == v:
            return 0
        if isinstance(u, (int, float)) and isinstance(v, (int, float)):
            return u - v
        return ("-", u, v)

    elif op == "*":
        u, v = args
        if u == 0 or v == 0:
            return 0
        if u == 1:
            return v
        if v == 1:
            return u
        if isinstance(u, (int, float)) and isinstance(v, (int, float)):
            return u * v
        return ("*", u, v)

    elif op == "^":
        u, n = args
        if n == 0:
            return 1
        if n == 1:
            return u
        if u == 0:
            return 0
        return ("^", u, n)

    elif op == "/":
        u, v = args
        if u == 0:
            return 0
        if v == 1:
            return u
        return ("/", u, v)

    return (op, *args)


def to_str(expr):
    """將樹狀結構轉為標準中序數學字串"""
    if not isinstance(expr, tuple):
        return str(expr)
    op = expr[0]
    if len(expr) == 2:
        return f"{op}({to_str(expr[1])})"
    elif len(expr) == 3:
        left = to_str(expr[1])
        right = to_str(expr[2])
        return f"({left} {op} {right})"
    return str(expr)
