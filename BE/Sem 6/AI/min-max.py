def heuristic(current, goal):
    return goal - current


def minimax(current, goal, is_max):

    if current >= goal:
        if is_max:
            return -1
        else:
            return 1

    if is_max:
        best = -float('inf')
        for move in [1, 2]:
            value = minimax(current + move, goal, False)
            best = max(best, value)
        return best
    else:
        best = float('inf')
        for move in [1, 2]:
            value = minimax(current + move, goal, True)
            best = min(best, value)
        return best



def best_move(current, goal):
    best_val = -float('inf')
    move_choice = None

    for move in [1, 2]:
        value = minimax(current + move, goal, False)
        if value > best_val:
            best_val = value
            move_choice = move

    return move_choice



def play_game(start, goal):
    current = start

    print("Game Start! Target =", goal)

    while current < goal:
        move = best_move(current, goal)
        print(f"Current: {current}, Best Move: +{move}")
        current += move

    print("Reached:", current)
    print("Game Over!")

play_game(0, 5)