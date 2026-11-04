原始式子: (A | B) & (~A | C)
內部邏輯式: (A  or  B)  and  ( not A  or  C)
================================
   A       B       C     Result 
--------------------------------
   T       T       T       T    
   T       T       F       F    
   T       F       T       T    
   T       F       F       F    
   F       T       T       T    
   F       T       F       T    
   F       F       T       F    
   F       F       F       F    
================================

[SATISFIABLE] 共有 4 組解可使式子為真：
  解 1: A=True, B=True, C=True
  解 2: A=True, B=False, C=True
  解 3: A=False, B=True, C=True
  解 4: A=False, B=True, C=False

原始式子: A & ~A
內部邏輯式: A  and   not A
================
   A     Result 
----------------
   T       F    
   F       F    
================

[UNSATISFIABLE] 無解（無論變數如何賦值，式子恆為假）。
