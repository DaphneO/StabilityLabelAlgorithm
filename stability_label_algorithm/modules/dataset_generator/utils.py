import pathlib

from stability_label_algorithm.modules.argumentation.argumentation_theory.argumentation_system import ArgumentationSystem
from stability_label_algorithm.modules.argumentation.exporters.argumentation_system_json_writer import ArgumentationSystemJsonWriter
from stability_label_algorithm.modules.argumentation.importers.argumentation_system_json_reader import ArgumentationSystemJsonReader

dataset_folder_path = pathlib.Path(__file__).parent.parent.parent / 'resources' / 'datasets'


def get_path(file_name: str) -> pathlib.Path:
    return pathlib.Path(dataset_folder_path / str(file_name + '.json'))


def write_argumentation_system(argumentation_system: ArgumentationSystem, argumentation_system_name: str):
    argumentation_system_path = get_path(argumentation_system_name)
    folder_path = argumentation_system_path.parent
    if not folder_path.is_dir():
        folder_path.mkdir(parents=True)
    ArgumentationSystemJsonWriter().write_to_json(argumentation_system, str(argumentation_system_path))


def get_argumentation_system_from_name(argumentation_system_name: str) -> ArgumentationSystem:
    argumentation_system_path = get_path(argumentation_system_name)
    argumentation_system = ArgumentationSystemJsonReader().read_from_json(str(argumentation_system_path))
    return argumentation_system
