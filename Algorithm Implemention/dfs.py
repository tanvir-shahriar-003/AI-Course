# DFS.py

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

def dfs_recursive(graph, node, goal_node, visited=None):
    """Performs Depth-First Search recursively."""
    if visited is None:
        visited = set()
        
    if node not in visited:
        print(f"Visited: {node}")
        visited.add(node)
        
        if node == goal_node:
            return True 
        
        # DFS goes as deep as possible before backtracking
        for neighbor in graph.get(node, []):
            if dfs_recursive(graph, neighbor, goal_node, visited):
                return True
                
    return False

def dfs(graph, start_node, goal_node):
    """Driver for DFS."""
    if start_node not in graph or goal_node not in graph:
        return "Start or goal node not found in graph."
        
    print(f"\n--- 🚀 Running DFS from {start_node} to {goal_node} ---")
    
    if dfs_recursive(graph, start_node, goal_node):
        return f"\n✅ SUCCESS: Goal '{goal_node}' found!"
    else:
        return f"\n❌ FAILURE: Goal '{goal_node}' not reachable from '{start_node}' or not found."

if __name__ == "__main__":
    graph = get_user_graph()
    if not graph:
        print("Graph is empty. Exiting.")
    else:
        start_node = input("Enter Start Node: ").strip().upper()
        goal_node = input("Enter Goal Node: ").strip().upper()
        print(dfs(graph, start_node, goal_node))