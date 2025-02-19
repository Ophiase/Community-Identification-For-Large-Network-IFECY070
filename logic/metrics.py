from typing import List, Dict
import numpy as np
from scipy.optimize import linear_sum_assignment


class Metrics:
    @staticmethod
    def _create_mapping(labels: List[int]) -> Dict[int, int]:
        # Map each unique label to a contiguous index.
        unique_labels = sorted(set(labels))
        return {label: idx for idx, label in enumerate(unique_labels)}

    @staticmethod
    def compare_partitions(true_labels: List[int], detected_labels: List[int]) -> float:
        """
        Compare two partitions and return the error rate (fraction of nodes misclassified)
        using the Hungarian algorithm for optimal label matching.

        Time Complexity: O(n + k^2 + n) ≈ O(n + k^2)
        - n: number of nodes.
        - k: number of unique labels.

        Args:
            true_labels (List[int]): Ground truth community labels.
            detected_labels (List[int]): Predicted community labels.

        Returns:
            float: Fraction of misclassified nodes.
        """
        true_map = Metrics._create_mapping(true_labels)
        detected_map = Metrics._create_mapping(detected_labels)
        cost_matrix = np.zeros((len(true_map), len(detected_map)), dtype=int)
        for t, d in zip(true_labels, detected_labels):
            cost_matrix[true_map[t], detected_map[d]] += 1
        row_ind, col_ind = linear_sum_assignment(-cost_matrix)
        correct = cost_matrix[row_ind, col_ind].sum()
        error_rate = 1 - correct / len(true_labels)
        return error_rate
