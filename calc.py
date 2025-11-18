import properties as pr

def shear_calculation(V, Q, I, b):
    return V * Q / I / b


V = 323.4
I = 521600
print(shear_calculation(V, 7356.2, I, 4* 1.27)) #Qmax
print(shear_calculation(V, 6125.5, I, 12.54)) #Q glue
print(shear_calculation(V, 6784.7, I, 2* 1.27)) #Q before ears

print(f"Case 1 buckling {pr.local_buckling(2.54, 63.73, 4)}") #Centre of top
print(f"Case 2 buckling {pr.local_buckling(2.54, 16.865, 0.425)}") #Flaps of top
print(f"Case 3 buckling {pr.local_buckling(1.27, 22.846, 6)}") #stilts above centroidal axis
print(f"Case 4 buckling {pr.shear_buckling(1.27, 97.46, 112)}")