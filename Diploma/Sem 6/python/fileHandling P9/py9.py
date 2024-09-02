import os.path


def readFile():
    name = input("Enter File Name: ")

    if os.path.isfile(name) == False:
        print("File not found")
        print("Want to create a new file?")
        ch = input("Y/N: ")
        if ch == "Y" or ch == "y":
            f = open(name,"w")
            print("File created")
            f.close()
        else:
            exit()
    else:
        f = open(name,"r")
        contents = f.read()
        print(contents)



def addData():
    name = input("Enter File Name: ")
    f = open(name,"a")
    data = input("Enter data: ")
    f.write(data)
    f.close()

while True:
    print("1. Read File")
    print("2. Add Data")
    print("3. Exit")
    ch = int(input("Enter choice: "))
    if ch == 1:
        readFile()
    elif ch == 2:
        addData()
    elif ch == 3:
        break
    else:
        print("Invalid choice")
