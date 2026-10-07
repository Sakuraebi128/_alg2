def my_reduce(func, seq, initial=None):
    if initial is not None:
        if not seq:
            return initial
        head, *tail = seq
        return my_reduce(func, tail, func(initial, head))
    else:
        if not seq:
            raise TypeError("my_reduce() of empty sequence with no initial value")
        head, *tail = seq
        return my_reduce(func, tail, head)
