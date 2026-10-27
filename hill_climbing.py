def get_cost(state):
    """Calculates the number of attacking pairs of queens (cost)."""
    cost = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            # Check for diagonal and row attacks
            if abs(state[i] - state[j]) == abs(i - j) or state[i] == state[j]:
                cost += 1
    return cost

def print_and_get_neighbors(state):
    """Generates all 6 possible pairs to swap"""

    n = len(state)
    best_neighbor = None
    best_cost = float('inf')
    
    # We swap pairs of columns: (0,1), (0,2), (0,3), (1,2), (1,3), (2,3)
    for i in range(n):
        for j in range(i + 1, n):
            neighbor = list(state)
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            
            neighbor_cost = get_cost(neighbor)
            
            # Extract individual elements to match the slide text format
            print(f"  • x0 = {neighbor[0]}, x1 = {neighbor[1]}, x2 = {neighbor[2]}, x3 = {neighbor[3]} cost is {neighbor_cost}.")
            
            # Select the first neighbor that yields the lowest cost
            if neighbor_cost < best_cost:
                best_cost = neighbor_cost
                best_neighbor = neighbor
                
    return best_neighbor, best_cost

def hill_climbing_swap_version(initial_state):
    current_state = list(initial_state)
    current_cost = get_cost(current_state)
    
    # Run loop step-by-step until goal cost of 0 is achieved
    while current_cost > 0:
        print(f"\nSolution: Neighbors of x0 = {current_state[0]}, x1 = {current_state[1]}, x2 = {current_state[2]}, x3 = {current_state[3]} (cost is {current_cost}.)\n")
        
        next_state, next_cost = print_and_get_neighbors(current_state)
        
        if next_cost >= current_cost:
            print("\n🛑 Local minimum reached.")
            break
            
        current_state = next_state
        current_cost = next_cost
        
    print(f"\n🎉 Goal state reached: x0 = {current_state[0]}, x1 = {current_state[1]}, x2 = {current_state[2]}, x3 = {current_state[3]} (cost is {current_cost}.)")

# --- Execute with the initial slide layout ---
initial = [3, 1, 2, 0]
hill_climbing_swap_version(initial)
