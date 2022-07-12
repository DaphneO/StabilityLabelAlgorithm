import pathlib
import time
from typing import Optional

import matplotlib as ml
import matplotlib.pyplot as plt
import pandas

from stability_label_algorithm.modules.argumentation.argumentation_theory.argumentation_theory import \
    ArgumentationTheory
from stability_label_algorithm.modules.argumentation.labelers.timed_four_bool_labeler import TimedFourBoolLabeler
from stability_label_algorithm.modules.dataset_generator.dataset_generator import DatasetGenerator
from tests.utils import path_to_resources_folder

ml.use("pgf")
ml.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})


class FourBoolTimingExperiment:
    """
    Measure the computation time of the FourBoolLabeler on a Dataset of 10.000 DatasetItems for each knowledge base size
    in the ArgumentationSystem.
    """
    def __init__(self,
                 argumentation_system_file_name: str,
                 experiments_name: Optional[str] = None,
                 do_recompute: bool = False):
        self.argumentation_system_file_name = argumentation_system_file_name
        self.do_recompute = do_recompute

        if experiments_name:
            self.experiments_name = experiments_name
        else:
            self.experiments_name = argumentation_system_file_name

        self.result_folder_path = pathlib.Path.cwd() / 'results' / 'FourBoolTiming' / self.experiments_name
        self.result_df_file_path = self.result_folder_path / 'comp_df.csv'

        self.computation_df = None

    def _recompute_df_if_necessary(self):
        if not self.result_folder_path.is_dir():
            self.result_folder_path.mkdir(parents=True)
        if self.do_recompute or not self.result_df_file_path.is_file():
            self.compute_computation_df()
        self.computation_df = pandas.read_csv(self.result_df_file_path)

    def compute_computation_df(self):
        dataset_generator = DatasetGenerator.from_file(self.argumentation_system_file_name)
        dataset = dataset_generator.generate_dataset_sample(
            custom_dataset_name=self.experiments_name,
            include_ground_truth=False,
            sample_size=10000)
        stability_labeler = TimedFourBoolLabeler()

        results = dict()

        for dataset_i, dataset_item in enumerate(dataset.dataset_items):
            # Read argumentation theory
            argumentation_theory = ArgumentationTheory(dataset_item.argumentation_system,
                                                       dataset_item.knowledge_base)
            knowledge_base_str = ','.join([str(k) for k in dataset_item.knowledge_base])

            # Time FourBoolLabeler
            nr_of_iterations = 10
            start_time = time.perf_counter()
            labels = [stability_labeler.label(argumentation_theory) for _ in range(nr_of_iterations)]
            # _estimated_labels = [labels[i][0].literal_labeling[dataset_item.topic_literal]
            #                      for i in range(nr_of_iterations)]
            end_time = time.perf_counter()
            elapsed_time_four_bool_labeler = (end_time - start_time) / nr_of_iterations
            relabel_literal_calls, relabel_rule_calls = labels[0][1:]

            # Store results
            nr_unknown_q = len(dataset_item.argumentation_system.positive_queryables) - len(dataset_item.knowledge_base)
            results[dataset_i] = {
                 'KnowledgeBase': knowledge_base_str,
                 'FourBoolMs': elapsed_time_four_bool_labeler * 1000,
                 'SizeQ': len(dataset_item.argumentation_system.queryables),
                 'SizeK': len(dataset_item.knowledge_base),
                 'QUnknown': nr_unknown_q,
                 'RelabelLiteralCalls': relabel_literal_calls,
                 'RelabelRuleCalls': relabel_rule_calls}

        computation_df = pandas.DataFrame(results).transpose()
        computation_df.to_csv(self.result_df_file_path)

    def plot_computation_time_naive_per_knowledge_base_size(self):
        fig, ax = plt.subplots(1, figsize=(8, 3))
        self.computation_df.boxplot(ax=ax, column=['FourBoolMs'], by='QUnknown', showfliers=False)
        ax.set_xlabel('Number of unknown queryables ($|\mathcal{Q}_\mathit{pos}| - |\mathcal{K}|$)')
        ax.set_ylabel('Computation time in ms')
        ax.grid(True)
        ax.set_title('')
        plt.suptitle('')
        plt.tight_layout()
        plt.savefig(self.result_folder_path /
                    ('FourBoolComputationTime' + '_' + self.argumentation_system_file_name + '.pgf'))

    def run_all_experiments(self):
        self._recompute_df_if_necessary()
        self.plot_computation_time_naive_per_knowledge_base_size()


if __name__ == "__main__":
    for file_name in path_to_resources_folder().iterdir():
        file_name = file_name.parts[-1]
        if str(file_name).startswith('0'):
                # str(file_name).startswith('counter') or \
            experiment = FourBoolTimingExperiment(file_name[:-5], do_recompute=False)
            experiment.run_all_experiments()
