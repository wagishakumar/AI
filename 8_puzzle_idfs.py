INITIAL_STATE = (
    (1, 2, 3),
    (0, 4, 6),
    (7, 5, 8)
)

GOAL_STATE = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 0)
)

def find_zero(state):
    for r in range(3):
        for c in range(3):
            if state[r][c] == 0:
                return r, c

def get_neighbors(state):
    r, c = find_zero(state)
    neighbors = []
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
   
    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_state = [list(row) for row in state]
            new_state[r][c], new_state[nr][nc] = new_state[nr][nc], new_state[r][c]
            neighbors.append(tuple(tuple(row) for row in new_state))
           
    return neighbors

def print_board(state):
    for row in state:
        print(" ".join(str(val) for val in row))
    print()

def depth_limited_search(state, goal_state, limit, path):
    if state == goal_state:
        return path

    if limit <= 0:
        return None

    for neighbor in get_neighbors(state):
        if neighbor not in path:  # Avoid cycles within the active path branch
            result = depth_limited_search(neighbor, goal_state, limit - 1, path + [neighbor])
            if result is not None:
                return result

    return None

def iterative_deepening_search(initial_state, goal_state, max_depth=20):
    for depth in range(max_depth + 1):
        print(f"Testing depth limit: {depth}")
        result = depth_limited_search(initial_state, goal_state, depth, [initial_state])
        if result is not None:
            return result, depth
           
    return None, max_depth

if __name__ == "__main__":
    solution_path, solved_depth = iterative_deepening_search(INITIAL_STATE, GOAL_STATE, max_depth=20)

    if solution_path:
        print(f"\nIDS Solution Found at depth {solved_depth} ({len(solution_path) - 1} steps):\n")
        for step, state in enumerate(solution_path):
            print(f"Step {step}:")
            print_board(state)
    else:
        print("No solution found within maximum depth limit.")