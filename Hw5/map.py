def my_map(func, seq):
    if not seq:
        return []
    head, *tail = seq
    return [func(head)] + my_map(func, tail)
