str = ["hello", "world", "python", "is", "fun","hello"]

a = input("Enter a string: ")
count = 0

for i in range(len(str)):
    if str[i] == a:
        count+=1
        
print(count)