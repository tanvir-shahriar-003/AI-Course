
graph = {}       # Dictionary to store adjacency list with edge weights for each node
heuristic = {}   # Dictionary to store heuristic values for each node
cost = {}        # Dictionary to store cumulative cost from start to each node

# Input graph with edge weights
n = int(input("Enter number of edges: "))  # Read the number of edges
for i in range(n):
    u, v, w = input("Enter edge (u v w): ").split()  # Read edge from u to v with weight w
    w = int(w)  # Convert weight to integer
    if u not in graph:
        graph[u] = []  
    if v not in graph:
        graph[v] = []  
    graph[u].append((v, w))  
    graph[v].append((u, w))  

# Input heuristic values
m = int(input("Enter number of heuristic values: "))  
for i in range(m):
    node, h = input("Enter node and heuristic: ").split()  
    heuristic[node] = int(h) 

start = input("Enter start node: ")  
goal = input("Enter goal node: ")    

open_list = [start]    # Nodes to explore, initialized with start
closed_list = []       # Nodes already visited
cost[start] = 0 # Cost to reach start node is 0
novisit_list = []
parent = {start: None} # Dictionary to keep track of parent nodes (for path reconstruction)

while open_list:
    open_list.sort(key=lambda x: cost[x] + heuristic[x])  # Sort by f(n) = g(n) + h(n)
    current = open_list.pop(0)  # Node with lowest f(n)

    print("Visiting:", current)

    if current == goal:
        print("Goal reached!")
        path = []
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()
        print("Path:", " -> ".join(path))
        break

    closed_list.append(current)

    for neighbor, w in graph[current]:
        if neighbor in closed_list:
            continue
        new_cost = cost[current] + w
        if neighbor not in open_list or new_cost < cost.get(neighbor, float('inf')):
            cost[neighbor] = new_cost
            parent[neighbor] = current
            if neighbor not in open_list:
                open_list.append(neighbor)
