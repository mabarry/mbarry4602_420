import argparse
import queue

# Represents current state of the problem
class State:
    def __init__(self, stacks, depth=0):
        self.stacks = stacks
        self.depth = depth

    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        return "\n".join([" ".join(stack) for stack in self.stacks])

class Node:
    def __init__(self, state, parent=None, depth=0):
        self.state = state
        self.parent = parent
        self.depth = depth
        self.g = 0
        self.h = 0
        self.f = 0
        
    def __lt__(self, other):
        return self.f < other.f

# Reads and parses problem from input
def parse_problem_file(filename):
    try:
        with open(filename, "r") as file:
            line = file.readline().strip() # Read for problem parameters
            s, b, m = map(int, line.split())  # Number of stacks, blocks, moves
            
            # Read separator line
            file.readline()

            # Initialize empty lists for initial state and goal state
            initial_state = []
            goal_state = []

            # Read initial state
            for _ in range(s):
                stack = list(file.readline().strip())
                initial_state.append(stack)
            
            # Read separator line
            file.readline()

            # Read goal state
            for _ in range(s):
                stack = list(file.readline().strip())
                goal_state.append(stack)
            
            # Return parsed data
            return State(initial_state), State(goal_state)

    # Minor error handling
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        exit(1)
    except Exception as e:
        print(f"Error parsing file '{filename}': {str(e)}")
        exit(1)

# ----------------------------------------------------------------------------------------

# Print the solution path from the goal node to the initial node
def print_solution_path(goal_node):
    path = []
    current_node = goal_node

    while current_node:
        path.append(current_node)
        current_node = current_node.parent

    path.reverse()

    for step, node in enumerate(path):
        state = node.state
        print(f"Move {step}, Pathcost={node.g}, Heuristic={node.h}, f(n)={node.f}")
        print_state(state)
        print(">>>>>>>>>>")

# Prints the state (stacks of blocks)
def print_state(state):
    for stack in state.stacks:
        print(" ".join(stack))

# Calculate the heuristic value (h(n))
def calculate_heuristic(current_state, goal_state, heuristic):
    
    # H0, trivial heuristic
    if heuristic == "H0":
        return 0

    # Blocks out of place heuristic
    if heuristic == "H1":
        h1_score = 0 # Initialize heuristic value

        # Step 1: Number of blocks outside stack 0
        for i in range(1, len(current_state.stacks)):  # Start from index 1 to skip stack 0
            h1_score += len(current_state.stacks[i])  # Penalize each block outside stack 0 with 1 unit

        # Step 2: Number of blocks in stack 0 in a position different than in the goal state
        min_stack_size = min(len(current_state.stacks[0]), len(goal_state.stacks[0]))
        for i in range(min_stack_size):
            if current_state.stacks[0][i] != goal_state.stacks[0][i]:
                h1_score += 1  # Penalize each block in stack 0 in the wrong position with 1 unit

        # If goal state has fewer blocks in stack 0, penalize the extra blocks in the current state
        h1_score += abs(len(current_state.stacks[0]) - len(goal_state.stacks[0]))

        return h1_score
    
    # Modified blocks out of place heuristic
    if heuristic == "H2":
        h2_score = 0 # Initialize heuristic value

        # Step 1: Iterate over the blocks in the goal state
        for i, goal_stack in enumerate(goal_state.stacks):
            for j, goal_block in enumerate(goal_stack):
                # Step 1a. Find the corresponding block in the current state
                current_block = None
                for curr_stack in current_state.stacks:
                    if goal_block in curr_stack:
                        current_block = curr_stack[curr_stack.index(goal_block):]
                        break

                # Step 1b. Check if Block A is supposed to be on top of B and under C
                if j < len(goal_stack) - 1:
                    block_on_top = goal_stack[j + 1]
                    if current_block and block_on_top not in current_block:
                        h2_score += 2
                
                if j > 0:
                    block_under = goal_stack[j - 1]
                    if current_block and block_under not in current_block:
                        h2_score += 2

                # Step 1c. Check if Block A is either on top of B or under C
                if current_block:
                    if j < len(goal_stack) - 1 and block_on_top in current_block:
                        h2_score += 1
                    if j > 0 and block_under in current_block:
                        h2_score += 1

        return h2_score

    return 0  # Default to H0

# ---------------------------------------------------------------------------------

# Generates successor states for a given state
def successors(state):
    stacks = state.stacks # Get current state's stacks
    num_stacks = len(stacks)

    # Initialize list to store successor states
    successor_states = []

    # Generate successor states for legal moves
    for source_stack in range(num_stacks):
        for target_stack in range(num_stacks):
            if source_stack != target_stack and stacks[source_stack]:
                
                successor_stacks = [stack[:] for stack in stacks] # Create a copy of the current state
                block = successor_stacks[source_stack].pop() # Pop the top block from the source stack                
                
                successor_stacks[target_stack].append(block) # Push the block onto the target stack                
                successor_state = State(successor_stacks) # Create a new State object for the successor state

                # Append the successor state to the list
                successor_states.append(successor_state)

    return successor_states

# A* search
def astar_search(initial_state, goal_state, heuristic, max_iters, filename):
    open_set = queue.PriorityQueue()
    visited = set()
    max_queue_size = 0
    
    # Start node
    start_node = Node(initial_state)
    start_node.h = calculate_heuristic(initial_state, goal_state, heuristic)
    start_node.f = start_node.g + start_node.h
    open_set.put((start_node.f, start_node))  # Priority queue with f(n) as priority
    
    # Init statistics
    iterations = 0
    max_queue_size = 0
    
    while not open_set.empty():
        current_tuple = open_set.get()
        current_node = current_tuple[1]
        current_state = current_node.state

        iterations += 1

        if current_state == goal_state:
            print() # debugging   
            print_solution_path(current_node)
            print(f"statistics: {filename.split('/')[-1]} method Astar planlen {current_node.depth} iter {iterations} maxq {max_queue_size}")
            return

        visited.add(str(current_state))  # Store state as a string for hashing

        # Generate successor states
        successor_states = successors(current_state)

        for successor_state in successor_states:
            if str(successor_state) not in visited:
                successor_node = Node(successor_state, current_node, current_node.depth + 1)
                successor_node.g = current_node.g + 1
                successor_node.h = calculate_heuristic(successor_state, goal_state, heuristic)
                successor_node.f = successor_node.g + successor_node.h
                open_set.put((successor_node.f, successor_node))

                # Debugging output for each iteration
                if(iterations%100==0):
                    print(f"iter={iterations}, depth={successor_node.depth}, pathcost={successor_node.g}, heuristic={successor_node.h}, score={successor_node.f}, children={len(successor_states)}, Qsize={open_set.qsize()}")
  
        # Update max queue size
        max_queue_size = max(max_queue_size, open_set.qsize())
        
        # Check for max iterations
        if iterations >= max_iters:
            print(f"statistics: {filename.split('/')[-1]} method Astar planlen FAILED iters {iterations} maxq {max_queue_size}")
            return  

# Command-line argument parsing
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Input problem file")
    parser.add_argument("-H", choices=["H0", "H1", "H2"], default="H2", help="Heuristic function to use")
    parser.add_argument("-MAX_ITERS", type=int, default=100000, help="Maximum number of iterations")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    filename = args.filename
    heuristic = args.H
    max_iters = args.MAX_ITERS

    # Read and parse the problem description from the input file
    initial_state, goal_state = parse_problem_file(filename)
    astar_search(initial_state, goal_state, heuristic, max_iters, filename)