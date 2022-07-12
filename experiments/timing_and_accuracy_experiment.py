import pathlib
import time
from typing import Any, Callable, Optional

import matplotlib as ml
import matplotlib.pyplot as plt
import numpy
import pandas

from stability_label_algorithm.modules.argumentation.argumentation_theory.argumentation_theory import \
    ArgumentationTheory
from stability_label_algorithm.modules.argumentation.labelers.timed_four_bool_labeler import TimedFourBoolLabeler
from stability_label_algorithm.modules.argumentation.labelers.naive_stability_labeler import NaiveStabilityLabeler
from stability_label_algorithm.modules.argumentation.labelers.stability_label import StabilityLabel
from stability_label_algorithm.modules.dataset_generator.dataset_generator import DatasetGenerator
from tests.utils import path_to_resources_folder

ml.use("pgf")
ml.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
    'font.size': 12
})

EXTENSIONS = ['pgf', 'pdf']


class TimingAndAccuracyExperiment:
    """
    Measure the computation time and the accuracy of various labelers (FourBoolLabeler and NaiveLabeler) on the full
    Dataset generated from the ArgumentationSystem.
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

        self.result_folder_path = pathlib.Path.cwd() / 'results' / 'Naive_VS_FourBool' / self.experiments_name
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
        dataset = dataset_generator.generate_dataset(self.experiments_name, include_ground_truth=True)
        stability_labeler = TimedFourBoolLabeler()
        naive_stability_labeler = NaiveStabilityLabeler()

        results = dict()

        for dataset_item in dataset.dataset_items:
            # Read argumentation theory
            argumentation_theory = ArgumentationTheory(dataset_item.argumentation_system,
                                                       dataset_item.knowledge_base)
            knowledge_base_str = ','.join([str(k) for k in dataset_item.knowledge_base])

            # Time FourBoolLabeler
            nr_of_iterations = 10
            start_time = time.perf_counter()
            labels = [stability_labeler.label(argumentation_theory) for _ in range(nr_of_iterations)]
            estimated_labels = [labels[i][0].literal_labeling[dataset_item.topic_literal]
                                for i in range(nr_of_iterations)]
            end_time = time.perf_counter()
            elapsed_time_four_bool_labeler = (end_time - start_time) / nr_of_iterations
            estimated_label = estimated_labels[0]
            relabel_literal_calls, relabel_rule_calls = labels[0][1:]

            # Time NaiveLabeler
            start_time = time.perf_counter()
            labels = naive_stability_labeler.label(argumentation_theory)
            _ = labels.literal_labeling[dataset_item.topic_literal]
            end_time = time.perf_counter()
            elapsed_time_naive_stability_labeler = end_time - start_time

            # Store results
            results[knowledge_base_str] = \
                {'FourBoolMs': elapsed_time_four_bool_labeler * 1000,
                 'NaiveMs': elapsed_time_naive_stability_labeler * 1000,
                 'SizeQ': len(dataset_item.argumentation_system.queryables),
                 'SizeK': len(dataset_item.knowledge_base),
                 'QUnknown':
                     len(dataset_item.argumentation_system.positive_queryables) - len(dataset_item.knowledge_base),
                 'FourBoolLabel': estimated_label,
                 'GTLabel': dataset_item.gt_stability_label,
                 'RelabelLiteralCalls': relabel_literal_calls,
                 'RelabelRuleCalls': relabel_rule_calls
                 }

        computation_df = pandas.DataFrame(results).transpose()
        computation_df.to_csv(self.result_df_file_path)

    def plot_computation_time_naive_per_knowledge_base_size(self):
        fig, ax = plt.subplots(1, figsize=(8, 4))
        x = numpy.linspace(0, 8.2, 100)
        ax.plot(x + 1, 0.392 * 3 ** x, 'r', linewidth=0.6, linestyle=':')
        self.computation_df.boxplot(ax=ax, column=['NaiveMs'], by='QUnknown', showfliers=False)
        ax.set_xlabel(r'Number of unknown queryables ($|\mathcal{Q}_\mathit{pos}| - |\mathcal{K}|$)')
        ax.set_ylabel('Computation time in ms')
        ax.set_yticks([0, 500, 1000, 1500, 2000, 2500, 3000])
        ax.grid(True)
        ax.set_title('')
        plt.suptitle('')
        plt.tight_layout()
        for extension in EXTENSIONS:
            plt.savefig(self.result_folder_path /
                        ('NaiveComputationTime' + '_' + self.argumentation_system_file_name + '.' + extension))

    def plot_computation_time_four_bool_per_knowledge_base_size(self):
        fig, ax = plt.subplots(1, figsize=(8, 4))
        self.computation_df.boxplot(ax=ax, column=['FourBoolMs'], by='QUnknown', showfliers=False)
        ax.set_xlabel(r'Number of unknown queryables ($|\mathcal{Q}_\mathit{pos}| - |\mathcal{K}|$)')
        ax.set_ylabel('Computation time in ms')
        ax.grid(True)
        ax.set_title('')
        plt.suptitle('')
        plt.tight_layout()
        for extension in EXTENSIONS:
            plt.savefig(self.result_folder_path /
                        ('FourBoolComputationTime' + '_' + self.argumentation_system_file_name + '.' + extension))

    def plot_computation_time_naive_vs_four_bool_per_knowledge_base_size(self):
        fig, axes = plt.subplots(2, figsize=(8, 6))
        x = numpy.linspace(0, 8.2, 100)
        axes[0].plot(x + 1, 0.392 * 3 ** x, 'r', linewidth=0.6, linestyle=':')
        self.computation_df.boxplot(ax=axes[0], column=['NaiveMs'], by='QUnknown', showfliers=False)
        self.computation_df.boxplot(ax=axes[1], column=['FourBoolMs'], by='QUnknown', showfliers=False)
        for ax in axes:
            ax.set_xlabel(r'Number of unknown queryables ($|\mathcal{Q}_\mathit{pos}| - |\mathcal{K}|$)')
            ax.set_ylabel('Computation time in ms')
            ax.grid(True)
        axes[0].set_title(r'Computation time of \textsc{stability-naive}')
        axes[1].set_title(r'Computation time of \textsc{stability-label}')
        plt.suptitle(r'\textsc{stability-naive} vs. \textsc{stability-label}')
        plt.tight_layout()
        for extension in EXTENSIONS:
            plt.savefig(self.result_folder_path /
                        ('NaiveVersusFourBoolComputationTime' + '_' +
                         self.argumentation_system_file_name + '.' + extension))

    def _export_confusion_matrix(self,
                                 data_categorisation_function: Callable[[str], Any],
                                 name: str):
        stable_gt = self.computation_df.GTLabel.apply(data_categorisation_function)
        stable_four_bool = self.computation_df.FourBoolLabel.apply(data_categorisation_function)

        confusion_matrix = pandas.crosstab(stable_gt, stable_four_bool)
        accurate_labels = numpy.diag(confusion_matrix)
        accuracy = sum(accurate_labels) / confusion_matrix.to_numpy().sum()

        confusion_matrix.to_csv(self.result_folder_path / (name + 'ConfusionMatrix.csv'))
        with open(self.result_folder_path / (name + 'Accuracy.txt'), 'w') as writer:
            writer.write(str(accuracy))

    def show_binary_confusion_matrix(self):
        self._export_confusion_matrix(lambda x: StabilityLabel.from_str(x).is_stable, 'Binary')

    def show_multi_value_confusion_matrix(self):
        self._export_confusion_matrix(lambda x: x, 'MultiValue')

    def run_all_experiments(self):
        self._recompute_df_if_necessary()

        self.plot_computation_time_naive_per_knowledge_base_size()
        self.plot_computation_time_four_bool_per_knowledge_base_size()
        self.plot_computation_time_naive_vs_four_bool_per_knowledge_base_size()
        self.show_binary_confusion_matrix()
        self.show_multi_value_confusion_matrix()


if __name__ == "__main__":
    for file_name in path_to_resources_folder().iterdir():
        file_name = file_name.parts[-1]
        if str(file_name).startswith('counter') or str(file_name).startswith('02') or str(file_name).startswith('03') \
                or str(file_name).startswith('04'):
            experiment = TimingAndAccuracyExperiment(file_name[:-5], do_recompute=False)
            experiment.run_all_experiments()
