def is_safe_state(allocated, max_demand, available):
    def check_resources(need, available):
        return all(need[i] <= available[i] for i in range(len(need)))

    def allocate_resources(need, allocated, available):
        return [allocated[i] + need[i] for i in range(len(need))], [
            available[i] - need[i] for i in range(len(need))
        ]

    num_processes = len(allocated)
    num_resources = len(available)

    work = available[:]
    finish = [False] * num_processes

    # Calculate the need matrix
    need = [
        [max_demand[i][j] - allocated[i][j] for j in range(num_resources)]
        for i in range(num_processes)
    ]

    # Iterate through processes
    for _ in range(num_processes):
        found = False
        for i in range(num_processes):
            if not finish[i] and check_resources(need[i], work):
                finish[i] = True
                work, available = allocate_resources(allocated[i], work, available)
                found = True
                break
        if not found:
            return False
    return True


def main():
    allocated = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
    max_demand = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
    available = [3, 3, 2]

    if is_safe_state(allocated, max_demand, available):
        print("Safe state: No deadlock")
    else:
        print("Unsafe state: Deadlock may occur")


if __name__ == "__main__":
    main()
