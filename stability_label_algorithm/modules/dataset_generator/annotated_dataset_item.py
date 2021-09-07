from typing import List

from stability_label_algorithm.modules.argumentation.argumentation_theory.argumentation_system import ArgumentationSystem
from stability_label_algorithm.modules.argumentation.argumentation_theory.literal import Literal
from stability_label_algorithm.modules.argumentation.argumentation_theory.queryable import Queryable
from stability_label_algorithm.modules.argumentation.labelers.stability_label import StabilityLabel
from stability_label_algorithm.modules.dataset_generator.dataset_item import DatasetItem
from stability_label_algorithm.modules.dataset_generator.utils import get_argumentation_system_from_name


class AnnotatedDatasetItem(DatasetItem):
    """
    An AnnotatedDatasetItem is a specific type of DatasetItem that also has a ground truth acceptability and stability
    label for a topic literal.
    """
    def __init__(self, argumentation_system: ArgumentationSystem, argumentation_system_name: str,
                 knowledge_base: List[Queryable], topic_literal: Literal, gt_acceptability_label: StabilityLabel,
                 gt_stability_label: StabilityLabel):
        """
        Create an AnnotatedDatasetItem.

        :param argumentation_system: The ArgumentationSystem on which the DatasetItem is based.
        :param argumentation_system_name: The name of the ArgumentationSystem.
        :param knowledge_base: The knowledge base (list of Queryables).
        :param topic_literal: The Literal for which the ground truth is given.
        :param gt_acceptability_label: Ground truth acceptability label for the topic Literal.
        :param gt_stability_label: Ground truth stability label for the topic Literal.
        """
        super().__init__(argumentation_system, argumentation_system_name, knowledge_base)
        self.topic_literal = topic_literal
        self.gt_acceptability_label = gt_acceptability_label
        self.gt_stability_label = gt_stability_label

    def __str__(self):
        as_name = self.argumentation_system_name
        knowledge_str = '+'.join([str(k) for k in self.knowledge_base])
        acc_str = str(self.gt_acceptability_label)
        stab_str = str(self.gt_stability_label)
        return f'AS={as_name},K={knowledge_str},t={str(self.topic_literal)},acc={acc_str},stab={stab_str}'

    @classmethod
    def from_str(cls, dataset_item_str: str):
        argumentation_system_name, knowledge_str, topic_literal_str, acc_str, stab_str = dataset_item_str.split(',', 5)
        argumentation_system = get_argumentation_system_from_name(argumentation_system_name)
        knowledge_base = [argumentation_system.language[k] for k in knowledge_str.split('+')]
        topic_literal = argumentation_system.language[topic_literal_str]
        acc_label = StabilityLabel.from_str(acc_str)
        stab_label = StabilityLabel.from_str(stab_str)
        # noinspection PyTypeChecker
        return cls(argumentation_system, argumentation_system_name, knowledge_base, topic_literal,
                   acc_label, stab_label)
