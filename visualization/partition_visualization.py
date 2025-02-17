
import math
import random
from typing import Dict, List, Tuple
from matplotlib import pyplot as plt
import networkx as nx
from logic.node_partition import NodePartition


class PartitionVisualization:
    @staticmethod
    def compute_layout_from_true_partition(graph: nx.Graph, partition_list: List[List[int]]) -> Dict[int, Tuple[float, float]]:
        """
        Compute a layout for the graph where each community is assigned a position on a large circle.
        Within each community, nodes are positioned randomly on a small subcircle around the community center.

        Example:
            Input: partition_list = [[0, 1, 2], [3, 4]]
            Output: {0: (x0, y0), 1: (x1, y1), ..., 4: (x4, y4)} where positions reflect community structure.
        """
        pos: Dict[int, Tuple[float, float]] = {}
        num_groups = len(partition_list)
        big_radius = 10.0
        small_radius = 6.0
        for i, community in enumerate(partition_list):
            angle = 2 * math.pi * i / num_groups
            center_x = big_radius * math.cos(angle)
            center_y = big_radius * math.sin(angle)
            for node in community:
                theta = random.uniform(0, 2 * math.pi)
                r = random.uniform(0, small_radius)
                pos[node] = (center_x + r * math.cos(theta),
                             center_y + r * math.sin(theta))
        return pos

    @staticmethod
    def display_partition(
        graph: nx.Graph, 
        name: str = "", 
        partition_list=None, 
        partition_nodes=None, pos=None) -> None:
        """partition_list
        Display the graph using a given partition.

        Example:
            Input: a graph and partition_list = [[0,1,2],[3,4]]
            Behavior: displays the graph colored by communities.
        """
        if (partition_list is not None) and (partition_nodes is None):
            partition_nodes = NodePartition.partition_list_to_partition_nodes(
                partition_list)
        nx.draw(graph, pos=pos, node_color=partition_nodes,
                with_labels=True, cmap=plt.cm.rainbow)
        plt.title(name)
