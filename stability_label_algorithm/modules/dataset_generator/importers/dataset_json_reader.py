import json

from stability_label_algorithm.modules.dataset_generator.dataset import Dataset
from stability_label_algorithm.modules.dataset_generator.dataset_item import DatasetItem


class DatasetJsonReader:
    def __init__(self):
        pass

    @staticmethod
    def from_json(json_str: str):
        json_object = json.loads(json_str)
        dataset_items = [DatasetItem.from_str(dataset_item_str) for dataset_item_str in json_object['dataset_items']]
        dataset = Dataset(json_object['name'], json_object['argumentation_system_name'])
        dataset.dataset_items = dataset_items
        return dataset

    def read_from_json(self, file_path: str) -> Dataset:
        with open(file_path, 'r') as reader:
            argumentation_system_json = reader.read()
        return self.from_json(argumentation_system_json)
