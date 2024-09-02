number = int(input("Enter Number"))
fact = 1 # 1 is the identity for multiplication, so we can use it to initialize



if number < 0:
    print("No Factorial for Negative Number")
elif number  ==  0:
    print("Factorial of 0 is 0")
else:
    for i in range(1,number+1):
        fact = fact * i
        
print(fact)