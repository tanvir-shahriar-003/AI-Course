# BFS.py
from collections import deque

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
    
    # Ensure all mentioned nodes exist
    all_nodes = set(graph.keys())
    for neighbors in graph.values():
        for neighbor in neighbors:
            if neighbor not in graph: graph[neighbor] = []
    return graph

def bfs(graph, start_node, goal_node):
    """Performs Breadth-First Search."""
    if start_node not in graph or goal_node not in graph:
        return f"Start or goal node not found in graph."
        
    visited = set()
    queue = deque([start_node])
    
    print(f"\n--- 🚀 Running BFS from {start_node} to {goal_node} ---")
    
    while queue:
        node = queue.popleft()
        
        if node not in visited:
            print(f"Visited: {node}")
            visited.add(node)
            
            if node == goal_node:
                return f"✅ SUCCESS: Goal '{goal_node}' found!"
            
            # BFS explores all neighbors before moving to the next level
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    queue.append(neighbor)
    
    return f"❌ FAILURE: Goal '{goal_node}' not reachable from '{start_node}'."

if __name__ == "__main__":
    graph = get_user_graph()
    if not graph:
        print("Graph is empty. Exiting.")
    else:
        start_node = input("Enter Start Node: ").strip().upper()
        goal_node = input("Enter Goal Node: ").strip().upper()
        print(bfs(graph, start_node, goal_node))