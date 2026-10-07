def hanoi_recursive(n, source, target, auxiliary):
    """
    n: 圓盤數量
    source: 來源柱 (A)
    target: 目標柱 (C)
    auxiliary: 輔助柱 (B)
    """
    if n == 1:
        print(f"移動圓盤 1 從 {source} 到 {target}")
        return


    hanoi_recursive(n - 1, source, auxiliary, target)

 
    print(f"移動圓盤 {n} 從 {source} 到 {target}")

    
    hanoi_recursive(n - 1, auxiliary, target, source)



print("=== 遞迴解法 (3 個盤子) ===")
hanoi_recursive(3, "A", "C", "B")
