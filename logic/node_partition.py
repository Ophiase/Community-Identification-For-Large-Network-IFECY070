import random
from typing import List, Set


class NodePartion:
    @staticmethod
    def partition_list(
        n_nodes: int,
        n_partitions: int = 4,
        shuffle: bool = True,
        as_set: bool = True
    ) -> List[List[int] | Set[int]]:
        """
        Partitions `n_nodes` nodes into `n_partitions` groups as evenly as possible.

        Args:
            n_nodes (int): Total number of nodes to partition.
            n_partitions (int): Number of partitions to create. Default is 4.
            shuffle (bool): Whether to shuffle the nodes before partitioning. Default is True.

        Returns:
            List[List[int]]: A list of lists, where each sublist represents a partition of nodes.

        Example:
            >>> GraphGeneration._partition_nodes(10, 3)
            [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9]]
        """
        nodes = list(range(n_nodes))
        if shuffle:
            random.shuffle(nodes)

        groups = []
        base = n_nodes // n_partitions
        remainder = n_nodes % n_partitions
        start = 0
        for i in range(n_partitions):
            group_size = base + (1 if i < remainder else 0)

            this_group_nodes = nodes[start:start + group_size]
            if as_set:
                this_group_nodes = set(this_group_nodes)
            groups.append(this_group_nodes)

            start += group_size

        return groups
