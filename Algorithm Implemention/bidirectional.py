from collections import deque

def bfs_step(queue, visited, parent, other_visited, graph):
    """
    Perform one level of BFS from one side.
    Returns meeting node if frontiers intersect, else None.
    """
    if not queue:
        return None

    current = queue.popleft()
    for neigh in graph[current]:
        if neigh not in visited:
            visited[neigh] = visited[current] + 1
            parent[neigh] = current
            queue.append(neigh)
            if neigh in other_visited:
                return neigh
    return None


def reconstruct_path(meet, parent_s, parent_t):
    """
    Reconstruct path from source to target given meeting point.
    """
    # Path from source → meet
    path_s = []
    node = meet
    while node is not None:
        path_s.append(node)
        node = parent_s.get(node)
    path_s.reverse()

    # Path from meet → target
    path_t = []
    node = parent_t.get(meet)
    while node is not None:
        path_t.append(node)
        node = parent_t.get(node)

    return path_s + path_t


def bidirectional_search(graph, source, target):
    """
    Perform bidirectional BFS on an undirected graph.
    Returns the shortest path or None if no path.
    """
    if source not in graph or target not in graph:
        print("Source or Target node not found in the graph.")
        return None

    if source == target:
        return [source]

    q_s = deque([source])
    q_t = deque([target])

    visited_s = {source: 0}
    visited_t = {target: 0}

    parent_s = {source: None}
    parent_t = {target: None}

    while q_s and q_t:
        # Expand from the smaller frontier for efficiency
        if len(q_s) <= len(q_t):
            meet = bfs_step(q_s, visited_s, parent_s, visited_t, graph)
        else:
            meet = bfs_step(q_t, visited_t, parent_t, visited_s, graph)

        if meet is not None:
            return reconstruct_path(meet, parent_s, parent_t)

    return None


# -----------------------------
# MAIN PROGRAM (USER INPUT)
# -----------------------------
if __name__ == "__main__":
    graph = {}

    n = int(input("Enter number of nodes: "))
    e = int(input("Enter number of edges: "))

    print("Enter each edge (u v):")
    for _ in range(e):
        u, v = input().split()
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        # Undirected graph: add both directions
        graph[u].append(v)
        graph[v].append(u)

    source = input("Enter source node: ")
    target = input("Enter target node: ")

    path = bidirectional_search(graph, source, target)

    print("\nGraph:", graph)
    if path:
        print("Shortest Path:", " -> ".join(path))
    else:
        print("No path found between", source, "and", target)
