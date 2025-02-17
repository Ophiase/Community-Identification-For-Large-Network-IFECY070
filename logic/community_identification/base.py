
from typing import List


class CommunityIdentification:
    @staticmethod
    def project_partition(
        target_groups: int,
        detected_partition: List[int]
    ) -> List[int]:
        """
        Project the detected partition to a specified number of groups by merging groups.
        The merging is done by sorting the unique detected groups and mapping them proportionally 
        to new labels ranging from 0 to target_groups - 1.

        Example:
            Input: target_groups = 3, detected_partition = [0, 1, 2, 3, 4]
            Suppose unique groups sorted are [0, 1, 2, 3, 4] (total 5 groups). Then:
              mapping: 0 -> int(0*3/5)=0,
                       1 -> int(1*3/5)=0,
                       2 -> int(2*3/5)=1,
                       3 -> int(3*3/5)=1,
                       4 -> int(4*3/5)=2.
            Output: [0, 0, 1, 1, 2]
        """
        unique = sorted(set(detected_partition))
        k = len(unique)
        mapping = {group: int(index * target_groups / k)
                   for index, group in enumerate(unique)}
        return [mapping[label] for label in detected_partition]
