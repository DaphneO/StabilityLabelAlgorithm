from typing import List

from stability_label_algorithm.modules.argumentation.argumentation_theory.argumentation_system import ArgumentationSystem
from stability_label_algorithm.modules.argumentation.argumentation_theory.queryable import Queryable
from stability_label_algorithm.modules.dataset_generator.utils import get_argumentation_system_from_name


class DatasetItem:
    def __init__(self,
                 argumentation_system: ArgumentationSystem,
                 argumentation_system_name: str,
                 knowledge_base: List[Queryable]):
        """
        A DatasetItem has an ArgumentationSystem, its name and a knowledge base.

        :param argumentation_system: The ArgumentationSystem on which the DatasetItem is based.
        :param argumentation_system_name: The name of the ArgumentationSystem.
        :param knowledge_base: The knowledge base (list of Queryables).
        """
        self.argumentation_system = argumentation_system
        self.argumentation_system_name = argumentation_system_name
        self.knowledge_base = knowledge_base

    def __str__(self):
        as_name = self.argumentation_system_name
        knowledge_str = '+'.join([str(k) for k in self.knowledge_base])
        return f'AS={as_name},K={knowledge_str}'

    @classmethod
    def from_str(cls, dataset_item_str: str):
        """
        Read the DatasetItem from a string.

        :param dataset_item_str: String representation of the DatasetItem.
        :return: DatasetItem represented by the input string.
        """
        argumentation_system_name, knowledge_str = dataset_item_str.split(',', 2)
        argumentation_system = get_argumentation_system_from_name(argumentation_system_name)
        knowledge_str_list = knowledge_str.split('+')
        knowledge_base = argumentation_system.get_queryables(knowledge_str_list)
        return cls(argumentation_system, argumentation_system_name, knowledge_base)
