from collections import deque
from typing import Dict, List, Optional, Set
import networkx as nx

###################################################################################


def bfs_old(graph: Dict[int, List[int]], start: int = 0) -> Dict[int, int]:
    """
    Deprecated BFS
    """
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    queue = deque([start])

    while queue:
        current = queue.popleft()
        for neighbor in graph[current]:
            if distances[neighbor] == float('inf'):
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)

    return distances


def bfs(graph: nx.Graph, start_node: int = 0) -> Dict[int, int]:
    """
    Perform a BFS and compute distances from the start_node.

    Args:
        graph: A NetworkX graph object.
        start_node: The starting node for BFS.

    Returns:
        A dictionary where each key is a node and the value is the distance from the start_node.
    """
    distances = {start_node: 0}
    queue = [start_node]

    while queue:
        current = queue.pop(0)
        for neighbor in graph.neighbors(current):
            if neighbor not in distances:
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)

    return distances


def bfs_restricted(
    graph: nx.Graph, start_node: int = 0, destinations: Optional[Set[int]] = None
) -> Dict[int, int]:
    """
    Perform a BFS starting from start_node and restrict it to the given destinations if provided.

    Args:
        graph: A NetworkX graph object.
        start_node: The starting node for BFS.
        destinations: An optional set of destination nodes to include in the BFS.

    Returns:
        A dictionary where each key is a node, and the value is another dictionary containing:
            - 'parent': The parent node in the BFS tree.
            - 'distance': The distance from the start node.
    """
    parent = {start_node: start_node}
    distance = {start_node: 0}
    queue = [start_node]
    visited = {start_node}

    if destinations is None:
        destinations = set(graph.nodes)

    while queue:
        current = queue.pop(0)

        if current in destinations:
            destinations.remove(current)
            if not destinations:
                break

        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                parent[neighbor] = current
                distance[neighbor] = distance[current] + 1

    return distance
