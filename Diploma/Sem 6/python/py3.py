arr = [1,2,3,5,1,2,6,7,8,9,1]

num = int(input("Enter Number to Search"))
count = 0

for i in range(len(arr)):
    if arr[i] == num:
        count = count + 1


if count == 0:
    print("Not Found")
else:
    print(count)