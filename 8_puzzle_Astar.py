import heapq
import random

# Helper class to represent a node in the search tree
class Node:
    def __init__(self, state, parent=None, action=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.action = action  # The move (UP, DOWN, LEFT, RIGHT) taken to reach this state
        self.g = g
        self.h = h
        self.f = g + h

    # Defining less-than for the priority queue to sort by f(n)
    def __lt__(self, other):
        return self.f < other.f

# ==========================================
# ALGORITHM 2A: MISPLACED TILES HEURISTIC
# ==========================================
def heuristic_misplaced_tiles(current_state, goal_state):
    h = 0
    for i in range(9):
        # Exclude the blank tile (0) from the calculation
        if current_state[i] != 0 and current_state[i] != goal_state[i]:
            h += 1
    return h

# ==========================================
# ALGORITHM 2B: MANHATTAN DISTANCE HEURISTIC
# ==========================================
def heuristic_manhattan_distance(current_state, goal_state):
    h = 0
    for i in range(9):
        tile = current_state[i]
        # Exclude the blank tile (0) from the calculation
        if tile != 0:
            # Find current x, y (row, col)
            curr_row, curr_col = divmod(i, 3)
            # Find goal x, y (row, col)
            goal_idx = goal_state.index(tile)
            # divmod returns (row, col)
            goal_row, goal_col = divmod(goal_idx, 3)
            # Add absolute differences
            h += abs(curr_row - goal_row) + abs(curr_col - goal_col)
    return h

# ==========================================
# HELPER: GET NEIGHBORS (UP, DOWN, LEFT, RIGHT)
# ==========================================
def get_neighbors(state):
    neighbors = []
    blank_idx = state.index(0)
    row, col = divmod(blank_idx, 3)
   
    moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
   
    for dr, dc, action in moves:
        new_row, new_col = row + dr, col + dc
        # Check if the move is within the 3x3 grid boundaries
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_blank_idx = new_row * 3 + new_col
            # Swap blank tile with the target tile
            new_state = list(state)
            new_state[blank_idx], new_state[new_blank_idx] = new_state[new_blank_idx], new_state[blank_idx]
            neighbors.append((tuple(new_state), action))
    return neighbors

# ==========================================
# RANDOM CONFIGURATION GENERATOR (GUARANTEED SOLVABLE)
# ==========================================
def generate_random_solvable_state(goal_state, moves_count=15):
    """
    Generates a guaranteed solvable random puzzle state by walking 
    backwards away from the goal state by a set number of steps.
    """
    current_state = goal_state
    for _ in range(moves_count):
        neighbors = get_neighbors(current_state)
        # Select a random valid next state from the list of neighbors
        current_state = random.choice(neighbors)[0]
    return current_state

# ==========================================
# ALGORITHM 1: A* SEARCH (TREE SEARCH VERSION)
# ==========================================
def a_star_tree_search(start_state, goal_state, heuristic_func):
    # 1. Initialize OPEN as a priority queue
    open_list = []
   
    # Counter to track how many nodes we expand (to measure efficiency)
    nodes_expanded = 0
   
    # 2. Set g(Start) = 0, calculate h(Start), and set f(Start)
    h_start = heuristic_func(start_state, goal_state)
    start_node = Node(state=start_state, parent=None, action=None, g=0, h=h_start)
   
    # 3. Insert Start node into OPEN
    heapq.heappush(open_list, start_node)
   
    # 4. While OPEN is not empty:
    while open_list:
        # a. Pop node N with the lowest f(N) from OPEN
        current_node = heapq.heappop(open_list)
        nodes_expanded += 1
       
        # b. If N is Goal State, return SUCCESS (solution path and metrics)
        if current_node.state == goal_state:
            return reconstruct_path(current_node), nodes_expanded
           
        # c. For each valid neighbor node C:
        for child_state, action in get_neighbors(current_node.state):
            # i. Set g(C) = g(N) + 1
            g_child = current_node.g + 1
            # ii. Calculate h(C) using chosen heuristic
            h_child = heuristic_func(child_state, goal_state)
            # iii. Set f(C) = g(C) + h(C) (Handled inside Node constructor)
            child_node = Node(state=child_state, parent=current_node, action=action, g=g_child, h=h_child)
            # iv. Insert C into OPEN
            heapq.heappush(open_list, child_node)
           
    # 5. Return FAILURE
    return None, nodes_expanded

def reconstruct_path(node):
    """Helper function to trace back the solution path from the goal node to the start node."""
    path = []
    while node.parent is not None:
        path.append((node.action, node.state))
        node = node.parent
    path.reverse()
    return path

# ==========================================
# TEST IMPLEMENTATION
# ==========================================
if __name__ == "__main__":
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
   
    # Generate a random, valid initial puzzle state 
    # (Default 15 shuffle moves keeps it fast enough for pure tree search)
    start = generate_random_solvable_state(goal, moves_count=15)
    
    print("="*50)
    print(f"GENERATED RANDOM START STATE: {start[0:3]}")
    print(f"                              {start[3:6]}")
    print(f"                              {start[6:9]}")
    print("="*50)
   
    heuristics = [
        ("Misplaced Tiles", heuristic_misplaced_tiles),
        ("Manhattan Distance", heuristic_manhattan_distance)
    ]
   
    for name, heuristic_func in heuristics:
        print("\n" + "="*50)
        print(f"Testing A* with {name}...")
        print("="*50)
       
        solution, nodes_count = a_star_tree_search(start, goal, heuristic_func)
       
        if solution:
            print(f"SUCCESS! Solved in {len(solution)} steps.")
            print(f"Total nodes popped/expanded: {nodes_count}")
            print("\nSolution Steps:")
            for step, state in solution:
                print(f"Move: {step} -> State: {state[0:3]}\n{' '*18}{state[3:6]}\n{' '*18}{state[6:9]}")
        else:
            print(f"FAILURE: No solution found. Expanded {nodes_count} nodes.")
