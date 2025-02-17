from typing import List
import numpy as np
from scipy.optimize import linear_sum_assignment


class Metrics:
    def compare_partitions(true_labels: List[int], detected_labels: List[int]) -> float:
        """
        Compare two partitions and return the error rate (fraction of nodes misclassified).
        Uses the Hungarian algorithm for optimal matching between community labels.

        Example:
            Input: true_labels = [0, 0, 1, 1], detected_labels = [1, 1, 0, 0]
            Output: 0.0 (all nodes correctly classified after label matching)
        """
        unique_true = sorted(set(true_labels))
        unique_detected = sorted(set(detected_labels))
        cost_matrix = np.zeros(
            (len(unique_true), len(unique_detected)), dtype=int)
        for i in range(len(true_labels)):
            cost_matrix[true_labels[i]][detected_labels[i]] += 1
        row_ind, col_ind = linear_sum_assignment(-cost_matrix)
        correct = cost_matrix[row_ind, col_ind].sum()
        error_rate = 1 - correct / len(true_labels)
        return error_rate
