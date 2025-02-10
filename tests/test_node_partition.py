import random
from logic.node_partition import NodePartition


class TestNodePartition:
    #########################################
    # UNSHUFFLED

    def test_partition_list_unshuffled_set(self):
        groups = NodePartition.partition_list(10, 3, shuffle=False, as_set=True)
        expected = [{0, 1, 2, 3}, {4, 5, 6}, {7, 8, 9}]
        assert groups == expected

    def test_partition_list_unshuffled_list(self):
        groups = NodePartition.partition_list(10, 3, shuffle=False, as_set=False)
        expected = [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert groups == expected

    def test_partition_nodes_unshuffled(self):
        parts = NodePartition.partition_nodes(10, 3, shuffle=False)
        expected = [0, 0, 0, 0, 1, 1, 1, 2, 2, 2]
        assert parts == expected

    #########################################
    # SHUFFLED

    def test_partition_list_shuffled(self):
        groups = NodePartition.partition_list(10, 3, shuffle=True, as_set=True)
        all_nodes = set().union(*groups)
        assert all_nodes == set(range(10))
        expected_sizes = [4, 3, 3]
        for group, size in zip(groups, expected_sizes):
            assert len(group) == size

    def test_partition_nodes_shuffled(self):
        parts = NodePartition.partition_nodes(10, 3, shuffle=True)
        assert len(parts) == 10
        expected_counts = NodePartition._compute_counters(10, 3)
        for i in range(3):
            assert parts.count(i) == expected_counts[i]
