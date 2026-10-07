def bubble_pass(acc, current):
    """reduce 的步進函式：acc 是累計已處理的串列，current 是當前走訪的元素。

    維持將目前遇到的最大值置於 acc[-1]，若 current 較小則將其留在前面。
    """
    if not acc:
        return [current]

    prev = acc[-1]
    front = acc[:-1]

    if prev > current:
        # 逆序：將較小的 current 留在前面，較大的 prev 繼續往後推進浮泡
        return front + [current, prev]
    else:
        # 已保有序：prev 留在原地，current 作為新的最大值推進
        return acc + [current]


def bubble_sort(seq, steps_left=None):
    """外層遞迴取代外層迴圈：

    長度為 n 的串列最多只需浮泡 n 次即可保證全排序。
    """
    if len(seq) <= 1:
        return seq

    if steps_left is None:
        steps_left = len(seq)

    # 終止條件：已完成足夠輪次
    if steps_left == 0:
        return seq

    # 使用自製 my_reduce 執行單趟氣泡浮動
    one_pass_done = my_reduce(bubble_pass, seq, [])

    # 遞迴進行下一輪外層浮泡
    return bubble_sort(one_pass_done, steps_left - 1)
