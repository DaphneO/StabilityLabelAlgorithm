import pathlib


def path_to_resources_folder():
    return pathlib.Path(__file__).parent.parent / 'stability_label_algorithm' / 'resources' / 'rule_sets'


def path_to_resources(file_name):
    if len(file_name) < 5 or file_name[-5:] != '.xlsx':
        file_name = file_name + '.xlsx'
    return path_to_resources_folder() / file_name
