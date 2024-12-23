import numpy as np

# Definimos dos matrices booleanas
A = np.full((30, 7), True)
A[27,2] = False


B = np.full((30,7), True)

# Diferencia entre matrices: A AND NOT B
result = np.logical_and(B, np.logical_not(A))

print("Matriz A:")
print(A)
print("\nMatriz B:")
print(B)
print("\nDiferencia A - B:")
print(result)
