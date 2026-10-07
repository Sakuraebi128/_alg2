def my_filter(predicate, seq):
    if not seq:
        return []
    head, *tail = seq
    rest = my_filter(predicate, tail)
    return [head] + rest if predicate(head) else rest
