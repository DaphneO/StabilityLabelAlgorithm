from datetime import datetime
from itertools import combinations, chain
from typing import List, Optional

from stability_label_algorithm.modules.argumentation.argumentation_theory.argumentation_system import ArgumentationSystem
from stability_label_algorithm.modules.argumentation.argumentation_theory.argumentation_theory import ArgumentationTheory
from stability_label_algorithm.modules.argumentation.importers.argumentation_system_xlsx_reader import ArgumentationSystemXLSXReader
from stability_label_algorithm.modules.argumentation.labelers.acceptability_labeler import JustificationLabeler
from stability_label_algorithm.modules.dataset_generator.annotated_dataset_item import AnnotatedDatasetItem
from stability_label_algorithm.modules.dataset_generator.argumentation_theory_lattice_item import ArgumentationTheoryLatticeItem
from stability_label_algorithm.modules.dataset_generator.dataset import Dataset
from stability_label_algorithm.modules.dataset_generator.dataset_item import DatasetItem
from stability_label_algorithm.modules.dataset_generator.dataset_sample_generator.dataset_sample_generator import \
    generate_dataset_sample
from stability_label_algorithm.modules.dataset_generator.exporters.dataset_json_writer import DatasetJsonWriter
from stability_label_algorithm.modules.dataset_generator.utils import write_argumentation_system
from stability_label_algorithm.modules.test_consistency_queryable_set import queryable_set_is_consistent
from tests.utils import path_to_resources


class DatasetGenerator:
    def __init__(self,
                 argumentation_system: ArgumentationSystem,
                 argumentation_system_custom_name: Optional[str] = None):
        self.argumentation_system = argumentation_system
        self.argumentation_system_custom_name = argumentation_system_custom_name

    @classmethod
    def from_file(cls, argumentation_system_file_name: str):
        """
        Generate a Dataset for an ArgumentationSystem that must still be read from a file.

        :param argumentation_system_file_name: Name of ArgumentationSystem for which a Dataset should be generated.
        :return: Dataset for specified ArgumentationSystem.
        """
        asr = ArgumentationSystemXLSXReader(path_to_resources(argumentation_system_file_name))
        arg_system = ArgumentationSystem(asr.language, asr.rules, asr.topic_literals)
        return cls(arg_system, argumentation_system_file_name)

    def _get_argumentation_system_name(self, timestamp: str):
        argumentation_system_name = f'AS_{timestamp}'
        if self.argumentation_system_custom_name:
            argumentation_system_name += f'_{self.argumentation_system_custom_name}'
        return argumentation_system_name

    @staticmethod
    def _get_dataset_name(custom_dataset_name: str, argumentation_system_name: str, timestamp: str):
        if custom_dataset_name:
            return 'DS_{}_on_{}_{}'.format(timestamp, argumentation_system_name, custom_dataset_name)
        else:
            return 'DS_{}_on_{}'.format(timestamp, argumentation_system_name)

    def generate_dataset_sample(self, custom_dataset_name: Optional[str] = None, include_ground_truth: bool = True,
                                sample_size: int = 1000, verbose: bool = True) -> Dataset:
        """
        Generate a Dataset, where the number of DatasetItems for each number of items in the knowledge base is
        specified. For example, if there are 4 Queryables in the ArgumentationSystem, then a knowledge base can contain
        either 0, 1, or 2 (=4/2) items. If, for example, sample_size = 10 then for each knowledge base size 10
        ArgumentationTheories are generated, so the total number of DatasetItems is 30.

        :param custom_dataset_name: Optional, name of the Dataset. Otherwise a name based on the timestamp is chosen.
        :param include_ground_truth: Boolean indicating if the ground truth should be computed. Note: this takes time!
        :param sample_size: Number of DatasetItems for each number of items in the knowledge base.
        :param verbose: Boolean indicating if information should be printed.
        :return: The resulting Dataset.
        """
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S%f')

        # Store argumentation system
        argumentation_system_name = self._get_argumentation_system_name(timestamp)
        write_argumentation_system(self.argumentation_system, argumentation_system_name)

        # Compute and store dataset
        dataset_name = self._get_dataset_name(custom_dataset_name, argumentation_system_name, timestamp)
        argumentation_theory_dataset = DatasetGenerator._generate_argumentation_theory_dataset_sample(
            dataset_name, self.argumentation_system, argumentation_system_name, sample_size, verbose)
        DatasetJsonWriter().write_to_json(argumentation_theory_dataset)
        if not include_ground_truth:
            return argumentation_theory_dataset

        # Compute and store annotated dataset if required
        raise NotImplementedError('Moet nog!')

    def generate_dataset(self, custom_dataset_name: Optional[str] = None, include_ground_truth: bool = True,
                         verbose: bool = True) -> Dataset:
        """
        Generate a Dataset, where all possible ArgumentationTheories for the given ArgumentationSystem are generated.
        Note: for ArgumentationSystems with many Queryables, this takes a lot of time.

        :param custom_dataset_name: Optional, name of the Dataset. Otherwise a name based on the timestamp is chosen.
        :param include_ground_truth: Boolean indicating if the ground truth should be computed. Note: this takes time!
        :param verbose: Boolean indicating if information should be printed.
        :return: The resulting Dataset.
        """
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S%f')

        # Store argumentation system
        argumentation_system_name = self._get_argumentation_system_name(timestamp)
        write_argumentation_system(self.argumentation_system, argumentation_system_name)

        # Compute and store dataset
        dataset_name = self._get_dataset_name(custom_dataset_name, argumentation_system_name, timestamp)
        argumentation_theory_dataset = DatasetGenerator._generate_argumentation_theory_dataset(
            dataset_name, self.argumentation_system, argumentation_system_name, verbose)
        DatasetJsonWriter().write_to_json(argumentation_theory_dataset)
        if not include_ground_truth:
            return argumentation_theory_dataset

        # Compute and store annotated dataset if required
        annotated_dataset_name = dataset_name + '_annotated'
        annotated_dataset = DatasetGenerator._generate_dataset_for_argumentation_system_with_ground_truth(
            annotated_dataset_name, self.argumentation_system, argumentation_system_name, argumentation_theory_dataset)
        DatasetJsonWriter().write_to_json(annotated_dataset)
        return annotated_dataset

    @staticmethod
    def _generate_argumentation_theory_dataset(dataset_name: str,
                                               argumentation_system: ArgumentationSystem,
                                               argumentation_system_name: str,
                                               verbose: bool) -> Dataset:
        queryables = argumentation_system.queryables
        all_queryable_combinations = chain.from_iterable(combinations(queryables, r)
                                                         for r in range(len(queryables) + 1))

        dataset_items: List[DatasetItem] = []
        for queryable_tuple in all_queryable_combinations:
            queryable_list = list(queryable_tuple)
            if queryable_set_is_consistent(queryable_list):
                dataset_items.append(DatasetItem(argumentation_system, argumentation_system_name, queryable_list))
                if verbose and len(dataset_items) % 100000 == 0:
                    queryable_list_str = '+'.join([str(q) for q in queryable_list])
                    print(f'Added {str(len(queryable_list))}-length knowledge base {str(len(dataset_items))}: '
                          f'{queryable_list_str}.')
        return Dataset(dataset_name, argumentation_system_name, dataset_items)

    @staticmethod
    def _generate_argumentation_theory_dataset_sample(dataset_name: str,
                                                      argumentation_system: ArgumentationSystem,
                                                      argumentation_system_name: str,
                                                      sample_size: int,
                                                      verbose: bool) -> Dataset:
        nr_of_pos_queryables = len(argumentation_system.positive_queryables) + 1
        queryable_set_sample = generate_dataset_sample(argumentation_system,
                                                       {i: sample_size for i in range(0, nr_of_pos_queryables)},
                                                       verbose)
        dataset_items = [DatasetItem(argumentation_system, argumentation_system_name, knowledge_base)
                         for knowledge_base in queryable_set_sample]
        return Dataset(dataset_name, argumentation_system_name, dataset_items)

    @staticmethod
    def _generate_argumentation_theory_lattice(argumentation_theory_dataset: Dataset) \
            -> List[ArgumentationTheoryLatticeItem]:
        acceptability_labeler = JustificationLabeler()
        argumentation_theories = (ArgumentationTheory(dataset_item.argumentation_system, dataset_item.knowledge_base)
                                  for dataset_item in argumentation_theory_dataset.dataset_items)
        argumentation_theory_lattice_items = \
            [ArgumentationTheoryLatticeItem(argumentation_theory, acceptability_labeler.label(argumentation_theory))
             for argumentation_theory in argumentation_theories]
        for i1, first_item in enumerate(argumentation_theory_lattice_items):
            for second_item in argumentation_theory_lattice_items[i1 + 1:]:
                first_item.connect(second_item)
        return argumentation_theory_lattice_items

    @staticmethod
    def _generate_dataset_for_argumentation_system_with_ground_truth(
            dataset_name: str,
            argumentation_system: ArgumentationSystem,
            argumentation_system_name: str,
            argumentation_theory_dataset: Dataset) -> Dataset:
        if argumentation_system.topic_literals:
            topics = argumentation_system.topic_literals
        else:
            topics = argumentation_system.language.values()

        lattice_items = DatasetGenerator._generate_argumentation_theory_lattice(argumentation_theory_dataset)
        lattice_update_round = {lattice_item for lattice_item in lattice_items if lattice_item.is_largest}

        dataset_items = []

        while lattice_update_round:
            new_round = set()

            for lattice_item in lattice_update_round:
                lattice_item.update_possible_future_acceptability_statuses()
                for topic_literal in topics:
                    gt_acceptability_label = lattice_item.acceptability_labels.literal_labeling[topic_literal]
                    gt_stability_label = lattice_item.stability_labels.literal_labeling[topic_literal]
                    new_item = AnnotatedDatasetItem(argumentation_system, argumentation_system_name,
                                                    lattice_item.argumentation_theory.knowledge_base,
                                                    topic_literal, gt_acceptability_label, gt_stability_label)
                    dataset_items.append(new_item)

                new_round |= set(lattice_item.direct_previous_theories)

            lattice_update_round = new_round

        return Dataset(dataset_name, argumentation_system_name, dataset_items)
