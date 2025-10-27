# IDS.py

def get_user_graph():
    """Reads graph from user input."""
    graph = {}
    print("--- 📝 Enter Graph (Adjacency List) ---")
    print("Format: Node: Neighbor1 Neighbor2 ... (e.g., A: B C)")
    print("Type 'done' when you are finished.")
    while True:
        user_input = input("> ").strip()
        if user_input.lower() == 'done': break
        if ':' in user_input:
            node, neighbors_str = user_input.split(':', 1)
            node = node.strip().upper()
            neighbors = [n.strip().upper() for n in neighbors_str.split()]
            graph[node] = neighbors
        elif user_input:
            print("⚠️ Invalid format. Use 'Node: Neighbor1 Neighbor2 ...'")
    
    all_nodes = set(graph.keys())
    for neighbors in graph.values():
        for neighbor in neighbors:
            if neighbor not in graph: graph[neighbor] = []
    return graph

def iterative_deepening_search(graph, start_node, goal_node, max_depth):
    """Performs Iterative Deepening Search by iteratively calling DLS."""
    if start_node not in graph or goal_node not in graph:
        return "Start or goal node not found in graph."

    print(f"\n--- 🚀 Running IDS from {start_node} to {goal_node} (Max Depth: {max_depth}) ---")
    
    for limit in range(max_depth + 1):
        print(f"\n>>> Starting Iteration with Depth Limit = {limit} <<<")
        
        # Stack stores (node, depth) for the current DLS iteration
        stack = [(start_node, 0)]
        
        while stack:
            node, depth = stack.pop()
            
            print(f"Checking: {node} (Depth: {depth})")
            
            if node == goal_node:
                return f"✅ SUCCESS: Goal '{goal_node}' found at depth {depth} (Limit was {limit})!"
            
            if depth < limit:
                # Add neighbors (reversed for standard DFS/stack order)
                for neighbor in reversed(graph.get(node, [])):
                    stack.append((neighbor, depth + 1))
    
    return f"❌ FAILURE: Goal '{goal_node}' not found within the maximum depth of {max_depth}."

if __name__ == "__main__":
    graph = get_user_graph()
    if not graph:
        print("Graph is empty. Exiting.")
    else:
        start_node = input("Enter Start Node: ").strip().upper()
        goal_node = input("Enter Goal Node: ").strip().upper()
        try:
            max_depth = int(input("Enter Maximum Depth (M) for iteration: "))
            print(iterative_deepening_search(graph, start_node, goal_node, max_depth))
        except ValueError:
            print("⚠️ Invalid maximum depth. Must be an integer.")