details = [
    {
        "name": "Redmi",
        "model": "Note 7 Pro",
    },
    {
        "name": "Samsung",
        "model": "Galaxy M30",
    },
    {
        "name": "Realme",
        "model": "3 Pro",
    }
]

def add():
    name = input("Enter name: ")
    model = input("Enter model: ")
    details.append({
        "name": name,
        "model": model
    })
    for i in details:
        print(i)

def search():
    model = input("Enter model: ")
    for i in details:
        if i["model"] == model:
            print("Phone is "+ i["name"])
            print("Model is " + i["model"])
            break

def delete():
    model = input("Enter model: ")
    for i in details:
        if i["model"] == model:
            details.remove(i)
            break

def display():
    for i in details:
        print(i)


while True:
    print("1. Add")
    print("2. Search")
    print("3. Delete")
    print("4. Display")
    print("5. Exit")
    ch = int(input("Enter choice: "))
    if ch == 1:
        add()
    elif ch == 2:
        search()
    elif ch == 3:
        delete()
    elif ch == 4:
        display()
    elif ch == 5:
        break
    else:
        print("Invalid choice")