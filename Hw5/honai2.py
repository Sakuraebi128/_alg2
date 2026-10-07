def hanoi_iterative_pure(n, source="A", target="C", auxiliary="B"):
    pegs = {source: list(range(n, 0, -1)), auxiliary: [], target: []}
    total_moves = (1 << n) - 1  


    if n % 2 == 1:
        peg_order = [source, target, auxiliary]
    else:
        peg_order = [source, auxiliary, target]

    p1_index = 0  

    for step in range(1, total_moves + 1):
        if step % 2 == 1:

            src_peg = peg_order[p1_index]
            p1_index = (p1_index + 1) % 3
            tgt_peg = peg_order[p1_index]

            disk = pegs[src_peg].pop()
            pegs[tgt_peg].append(disk)
            print(f"步數 {step}: 移動圓盤 {disk} 從 {src_peg} 到 {tgt_peg}")
        else:

            other_pegs = [p for p in [source, auxiliary, target] if p != peg_order[p1_index]]
            p_a, p_b = other_pegs[0], other_pegs[1]

            top_a = pegs[p_a][-1] if pegs[p_a] else float("inf")
            top_b = pegs[p_b][-1] if pegs[p_b] else float("inf")

            if top_a < top_b:
                disk = pegs[p_a].pop()
                pegs[p_b].append(disk)
                print(f"步數 {step}: 移動圓盤 {disk} 從 {p_a} 到 {p_b}")
            else:
                disk = pegs[p_b].pop()
                pegs[p_a].append(disk)
                print(f"步數 {step}: 移動圓盤 {disk} 從 {p_b} 到 {p_a}")



print("=== 純數學迭代解法 (3 個盤子) ===")
hanoi_iterative_pure(3)
