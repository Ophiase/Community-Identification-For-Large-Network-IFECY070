from collections import deque
import random
from typing import Dict, List, Tuple
import networkx as nx

from .bfs import bfs

###################################################################################


def graph_diameter(graph: nx.Graph) -> int:
    diameter = 0
    for node in graph:
        distances = bfs(graph, node)
        farthest_distance = max(distances.values())
        diameter = max(diameter, farthest_distance)
    
    return diameter

def double_bfs(graph: nx.Graph) -> int:
    """
    Perform a double BFS: start from a random node, find the farthest node, and perform BFS again from there.

    Args:
        graph: A NetworkX graph object.

    Returns:
        A dictionary with the start node, farthest node, and the diameter of the graph.
    """
    start_node = random.choice(list(graph.nodes))

    # First BFS to find the farthest node
    distances = bfs(graph, start_node)
    farthest_node = max(distances, key=distances.get)

    # Second BFS from the farthest node
    second_distances = bfs(graph, farthest_node)
    diameter = max(second_distances.values())

    return diameter
