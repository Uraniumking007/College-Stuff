#  Process Count: pcount


pcount = int(input("Enter the number of processes: "))
processes = {}


def addProcesses():
    for i in range(pcount):
        processes.update({"process"+str(i+1):{
            "arrivalTime": int(input("Enter arrival time of process "+str(i+1)+": ")),
            "burstTime": int(input("Enter burst time of process "+str(i+1)+": "))
        }})


ganttChart = []

def sortedProcesses():
    return dict(sorted(processes.items(), key=lambda item: item[1]["arrivalTime"]))

def calculateGanttChart():
    countedTime = 0 
    for i in range(pcount):
        process = list(sortedProcesses())[i]
        ganttChart.append({
            "process": process,
            "startTime": countedTime,
            "endTime": countedTime + processes[process]["burstTime"]
        })
        countedTime += processes[process]["burstTime"]

    for i in range(pcount):
        print(ganttChart[i])

def updateData():
    for i in range(pcount):
        process = list(sortedProcesses())[i]
        processes[process]["completionTime"] = ganttChart[i]["endTime"]
        processes[process]["turnAroundTime"] = ganttChart[i]["endTime"] - processes[process]["arrivalTime"]
        processes[process]["waitingTime"] = processes[process]["turnAroundTime"] - processes[process]["burstTime"]


def calcAWT():
    sum = 0
    for i in range(pcount):
        process = list(sortedProcesses())[i]
        sum += processes[process]["waitingTime"]
    return sum/pcount
    
def calcATT():
    sum = 0
    for i in range(pcount):
        process = list(sortedProcesses())[i]
        sum += processes[process]["turnAroundTime"]
    return sum/pcount

addProcesses()
calculateGanttChart()
updateData()
while True:
    print("1. Calculate AWT")
    print("2. Calculate ATT")
    print("3. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        print("Average Waiting Time: ", calcAWT(), "ms")
    elif choice == 2:
        print("Average Turn Around Time: ", calcATT(), "ms")
    elif choice == 3:
        break
    else:
        print("Invalid Choice")