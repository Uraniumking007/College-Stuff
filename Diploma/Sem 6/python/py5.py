a = int(input("Enter Number 1 "))
b = int(input("Enter Number 2 "))

def fun(a,b):
    return [b,a]

# out = fun(a,b)
# a,b = out
a,b = fun(a,b)

print("After Swapping")
print("Number 1 is ",a)
print("Number 2 is ",b)
