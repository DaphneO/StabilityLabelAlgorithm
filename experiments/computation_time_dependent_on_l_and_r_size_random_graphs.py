import itertools
import math
import multiprocessing as mp
import pathlib
import time

import matplotlib as ml
import matplotlib.pyplot as plt
import pandas

from stability_label_algorithm.modules.argumentation.argumentation_theory.argumentation_theory import ArgumentationTheory
from stability_label_algorithm.modules.argumentation.labelers.timed_four_bool_labeler import TimedFourBoolLabeler
from stability_label_algorithm.modules.dataset_generator.argumentation_system_generator.random.\
    random_argumentation_system_generator import RandomArgumentationSystemGenerator
from stability_label_algorithm.modules.dataset_generator.argumentation_system_generator.random.\
    random_argumentation_system_generator_parameters import RandomArgumentationSystemGeneratorParameters
from stability_label_algorithm.modules.dataset_generator.dataset_generator import DatasetGenerator

ml.use("pgf")
ml.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})


def r_a_d(rule_size):
    result = dict()
    result[1] = math.ceil(rule_size * 4 / 10)
    result[2] = math.ceil(rule_size * 4 / 10)
    if result[1] + result[2] < rule_size:
        result[3] = rule_size - result[1] - result[2]
    return result


argumentation_system_generation_parameters_list = [
    RandomArgumentationSystemGeneratorParameters(language_size=language_size,
                                                 rule_size=rule_size,
                                                 rule_antecedent_distribution=r_a_d(rule_size),
                                                 queryable_ratio=0.45,
                                                 allow_rules_for_queryables=True,
                                                 allow_inconsistent_antecedents=True,
                                                 allow_conclusion_in_antecedents=True)
    for (language_size, rule_size) in itertools.product([10, 20, 50, 100, 150, 200, 250], repeat=2)
]

todo_items = ((argumentation_system_generation_parameters, argumentation_system_index)
              for argumentation_system_generation_parameters in argumentation_system_generation_parameters_list
              for argumentation_system_index in range(50))


def time_stability(input_tuple):
    arg_sys_gen_parameters, argumentation_system_index = input_tuple
    argumentation_system_generator = RandomArgumentationSystemGenerator(arg_sys_gen_parameters)
    argumentation_system = argumentation_system_generator.generate()
    dataset_generator = DatasetGenerator(argumentation_system)
    dataset = dataset_generator.generate_dataset_sample(include_ground_truth=False, sample_size=5, verbose=False)
    stability_labeler = TimedFourBoolLabeler()

    results = []
    for nr, dataset_item in enumerate(dataset.dataset_items):
        argumentation_theory = ArgumentationTheory(dataset_item.argumentation_system,
                                                   dataset_item.knowledge_base)
        knowledge_base_str = ','.join([str(k) for k in dataset_item.knowledge_base])

        start_time = time.perf_counter()
        _labels, relabel_literal_calls, relabel_rule_calls = stability_labeler.label(argumentation_theory)
        end_time = time.perf_counter()
        elapsed_time_four_bool_labeler = (end_time - start_time)

        new_result = ';'.join([str(arg_sys_gen_parameters),
                               dataset.argumentation_system_name,
                               knowledge_base_str,
                               str(arg_sys_gen_parameters.language_size),
                               str(arg_sys_gen_parameters.rule_size),
                               str(elapsed_time_four_bool_labeler * 1000).replace('.', ','),
                               str(relabel_literal_calls),
                               str(relabel_rule_calls)])
        results.append(new_result)
    return results


def analyse_stability_runtimes(result_path: pathlib.Path):
    # Read result_df
    result_df = pandas.read_csv(result_path, sep=';', decimal=',', na_filter=False)

    # Boxplot of computation time given sizes of l and r (in multiple plots)
    l_sizes = sorted(list(set(result_df['size(l)'])))
    axes = result_df.groupby('size(l)').boxplot(column=['time_ms'], by=['size(r)'], showfliers=False,
                                                layout=(2, math.ceil(len(l_sizes) / 2)),
                                                figsize=(12, 6))
    for i, ax in enumerate(axes):
        ax.set_xlabel('Number of rules')
        ax.set_title('Number of literals = ' + str(l_sizes[i]))
        ax.set_ylabel('Computation time in ms')
    plt.suptitle('')
    plt.tight_layout()

    # Output in pdf and png
    for extension in ['pgf', 'png']:
        write_path = result_path.parent / ('FourBoolComputationTimeRandomDatasetBoxplot.' + extension)
        plt.savefig(write_path)


def main(do_recompute: bool = False):
    pool = mp.Pool(mp.cpu_count() - 1)

    folder_path = pathlib.Path.cwd() / 'results' / 'computation_time_dependent_on_l_and_r_size_random_graphs'
    if not folder_path.is_dir():
        folder_path.mkdir(parents=True)

    result_path = folder_path / 'computation_time_dependent_on_l_and_r_size_random_graphs.csv'

    if not result_path.is_file() or do_recompute:
        with open(result_path, 'w') as writer:
            writer.write('arg_sys_gen_parameters;argumentation_system;knowledge_base;size(l);size(r);time_ms;'
                         'RelabelLiteralCalls;RelabelRuleCalls\n')

            for result_lines in pool.map(time_stability, todo_items):
                for result in result_lines:
                    print(result)
                    writer.write(result + '\n')

    analyse_stability_runtimes(result_path)


if __name__ == "__main__":
    main(do_recompute=False)
