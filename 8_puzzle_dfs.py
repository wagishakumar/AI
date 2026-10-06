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
        # Replaces 0 with a blank space for visual clarity
        print(" ".join(str(val) if val != 0 else " " for val in row))
    print()

def dfs_8_puzzle(initial_state, goal_state, max_depth=20):
    stack = [(initial_state, [initial_state])]
    # Tracks visited states globally to avoid getting stuck in infinite loops
    visited = {initial_state}

    while stack:
        current_state, path = stack.pop()

        if current_state == goal_state:
            return path

        if len(path) - 1 < max_depth:
            for neighbor in get_neighbors(current_state):
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor]))

    return None

if __name__ == "__main__":
    # Increased depth slightly if needed, but 15 is plenty for this short path
    solution_path = dfs_8_puzzle(INITIAL_STATE, GOAL_STATE, max_depth=15)

    if solution_path:
        print(f"DFS Solution Found in {len(solution_path) - 1} steps:\n")
        for step, state in enumerate(solution_path):
            print(f"Step {step}:")
            print_board(state)
    else:
        print("No solution found within the depth limit.")
