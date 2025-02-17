import random
from typing import List, Set
from typing import Union

import numba

PartitionGroupList = List[List[int]]
PartitionListSet = List[Set[int]]
PartitionNodes = List[int]
Partition = Union[PartitionGroupList, PartitionListSet, PartitionNodes]


class NodePartition:
    @staticmethod
    def partition_list(
        n_nodes: int,
        n_partitions: int = 4,
        shuffle: bool = True,
        as_set: bool = True
    ) -> PartitionGroupList | PartitionListSet:
        """
        Partitions `n_nodes` nodes into `n_partitions` groups as evenly as possible.

        Args:
            as_set (bool): Whether to returns the partitions as sets. Default is True.

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

    @staticmethod
    def _compute_counters(n_nodes: int, n_partitions: int) -> List[int]:
        """
        Returns:
            List[int]: A list where the ith index corresponds to the number of nodes attributed to the ith partition.
        """
        base = n_nodes // n_partitions
        rem = n_nodes % n_partitions
        return [base + (1 if i < rem else 0) for i in range(n_partitions)]

    @staticmethod
    def partition_nodes(
        n_nodes: int,
        n_partitions: int = 4,
        shuffle: bool = True
    ) -> PartitionNodes:
        """
        Partitions `n_nodes` nodes into `n_partitions` groups as evenly as possible.

        Returns:
            List[int]: A list where each element represents the partition index of the corresponding node.

        Example:
            >>> NodePartition.partition_nodes(10, 3, shuffle=False)
            [0, 0, 0, 0, 1, 1, 1, 2, 2, 2]
            >>> NodePartition.partition_nodes(10, 3, shuffle=True)
            [0, 1, 0, 2, 2, 1, 0, 2, 2, 1]
        """

        if not shuffle:
            return [(n_partitions * i) // n_nodes for i in range(n_nodes)]

        counters = NodePartition._compute_counters(n_nodes, n_partitions)
        available = list(range(n_partitions))
        result = []

        for _ in range(n_nodes):
            part = random.choice(available)
            result.append(part)
            counters[part] -= 1
            if counters[part] == 0:
                available.remove(part)

        return result

    @staticmethod
    def partition_list_to_partition_nodes(
        partition: PartitionGroupList,
        n_nodes: int = None
    ) -> PartitionNodes:
        """
        Convert a partition list (list of communities, each a list of node indices) into a label list.

        Example:
            Input: partition_list = [[0, 1, 2], [3, 4]], n = 5
            Output: [0, 0, 0, 1, 1]
        """
        if n_nodes is None:
            n_nodes = sum([len(group) for group in partition])
        result = [0] * n_nodes

        for which_group, group in enumerate(partition):
            for e in group:
                result[e] = which_group

        return result
