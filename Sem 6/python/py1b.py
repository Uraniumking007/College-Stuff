side1 = float(input("Enter Side 1 Length"))
side2 = float(input("Enter Side 2 Length"))
side3 = float(input("Enter Side 3 Length"))

a = (side1*side2*side3)/2
area = (a*(a - side1)*(a-side2)*(a-side3))**0.5

print("Area of This Triangle" ,a )