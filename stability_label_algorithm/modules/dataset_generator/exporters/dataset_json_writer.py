import simplejson as json

from stability_label_algorithm.modules.dataset_generator.dataset import Dataset
from stability_label_algorithm.modules.dataset_generator.utils import get_path


class DatasetJsonWriter:
    def __init__(self):
        pass

    @staticmethod
    def to_json(dataset: Dataset) -> str:
        json_dict = {'name': dataset.name, 'argumentation_system_name': dataset.argumentation_system_name,
                     'dataset_items': (str(dataset_item) for dataset_item in dataset.dataset_items)}
        return json.dumps(json_dict, iterable_as_array=True)

    def write_to_json(self, dataset: Dataset):
        # file_path = get_path(dataset.name)
        # with open(file_path, 'w') as writer:
            # writer.write(self.to_json(dataset))
        file_path = get_path(dataset.name)
        with open(file_path, 'w') as writer:
            writer.write(dataset.name + '\n')
            writer.write(dataset.argumentation_system_name + '\n')
            for dataset_item in dataset.dataset_items:
                writer.write(str(dataset_item) + '\n')
