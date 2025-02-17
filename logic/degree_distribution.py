import matplotlib.pyplot as plt
from collections import defaultdict
import random
from typing import Dict
import networkx as nx
import sys

from .bfs import bfs_restricted
from .graph_generation import GraphGeneration


class DegreeDistribution:
    def distribution(graph: nx.Graph, num_destinations: int) -> Dict[int, int]:
        """
        Compute the degree distribution from a restricted BFS on a given graph.

        Args:
            graph: The NetworkX graph object.
            num_destinations: The number of destination nodes to consider.

        Returns:
            A dictionary where the keys are degrees, and the values are the number of nodes with that degree.
        """
        # Select random start node and destinations
        nodes = list(graph.nodes)
        start_node = random.choice(nodes)
        destinations = set(random.sample(
            nodes, min(num_destinations, len(nodes))))

        # Perform restricted BFS
        restricted_result = bfs_restricted(graph, start_node, destinations)

        # Calculate degree distribution
        degree_count = defaultdict(int)
        for node in restricted_result:
            degree = graph.degree[node]
            degree_count[degree] += 1

        return dict(degree_count)

    def plot(distribution: Dict[int, int]) -> None:
        degrees = list(distribution.keys())
        counts = list(distribution.values())

        plt.figure(figsize=(10, 6))
        plt.bar(degrees, counts, color='blue', edgecolor='black')
        plt.xlabel('Degree')
        plt.ylabel('Number of Nodes')
        plt.title('Degree Distribution')
        plt.grid(True)
        plt.show()
