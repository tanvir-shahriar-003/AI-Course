# DLS.py

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

def dls(graph, start_node, goal_node, limit):
    """Performs Depth-Limited Search."""
    if start_node not in graph or goal_node not in graph:
        return "Start or goal node not found in graph."

    # Stack stores (node, depth)
    stack = [(start_node, 0)]
    
    print(f"\n--- 🚀 Running DLS (Limit={limit}) from {start_node} to {goal_node} ---")

    while stack:
        node, depth = stack.pop()
        
        print(f"Checking: {node} (Depth: {depth})")
        
        if node == goal_node:
            return f"✅ SUCCESS: Goal '{goal_node}' found at depth {depth}!"
        
        # Only proceed if current depth is less than the limit
        if depth < limit:
            # Add neighbors (reversed for standard DFS/stack order)
            for neighbor in reversed(graph.get(node, [])): 
                stack.append((neighbor, depth + 1))
                
    return f"❌ FAILURE: Goal '{goal_node}' not found within the depth limit of {limit}."

if __name__ == "__main__":
    graph = get_user_graph()
    if not graph:
        print("Graph is empty. Exiting.")
    else:
        start_node = input("Enter Start Node: ").strip().upper()
        goal_node = input("Enter Goal Node: ").strip().upper()
        try:
            limit = int(input("Enter Depth Limit (L): "))
            print(dls(graph, start_node, goal_node, limit))
        except ValueError:
            print("⚠️ Invalid limit. Must be an integer.")