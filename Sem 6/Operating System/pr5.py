def is_safe(state, available, max_claim, allocated):
    def is_less_or_equal(a, b):
        return all(x <= y for x, y in zip(a, b))

    def add_resources(a, b):
        return [x + y for x, y in zip(a, b)]

    def subtract_resources(a, b):
        return [x - y for x, y in zip(a, b)]

    def can_finish(process_id):
        return is_less_or_equal(need[process_id], available_resources)

    num_processes = len(state)
    num_resources = len(available)

    need = [subtract_resources(max_claim[i], allocated[i]) for i in range(num_processes)]
    work = available.copy()
    finish = [False] * num_processes

    while True:
        for i in range(num_processes):
            if not finish[i] and can_finish(i):
                work = add_resources(work, state[i])
                finish[i] = True

                if all(finish):
                    return True

                break
        else:
            return False

state = [
    [0, 1, 0],
    [2, 0, 0],
    [3, 0, 2],
    [2, 1, 1],
    [0, 0, 2]
]

available_resources = [3, 3, 2]
max_claim = [
    [7, 5, 3],
    [3, 2, 2],
    [9, 0, 2],
    [2, 2, 2],
    [4, 3, 3]
]
allocated = [
    [0, 1, 0],
    [2, 0, 0],
    [3, 0, 2],
    [2, 1, 1],
    [0, 0, 2]
]

if is_safe(state, available_resources, max_claim, allocated):
    print("System is in safe state.")
else:
    print("System is in unsafe state.")
