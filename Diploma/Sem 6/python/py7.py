tup = (1,2,5,6,32,4)
max = tup[0]
min = tup[0]
for i in tup:
    if i > max:
        max = i
    if i < min:
        min = i
    

print("Max is", max)
print("Min is", min)