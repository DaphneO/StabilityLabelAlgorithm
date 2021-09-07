from typing import List

from stability_label_algorithm.modules.dataset_generator.dataset_item import DatasetItem


class Dataset:
    def __init__(self, name: str, argumentation_system_name: str, dataset_items: List[DatasetItem]):
        """
        A Dataset has a name, the name of its ArgumentationSystem and a list of DatasetItems.

        :param name: Name of the Dataset.
        :param argumentation_system_name: Name of the ArgumentationSystem on which the Dataset is based.
        :param dataset_items: Items in the Dataset.
        """
        self.name = name
        self.argumentation_system_name = argumentation_system_name
        self.dataset_items = dataset_items
