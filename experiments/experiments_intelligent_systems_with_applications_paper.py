from experiments.timing_and_accuracy_experiment import TimingAndAccuracyExperiment
from tests.utils import path_to_resources_folder
import experiments.computation_time_dependent_on_l_and_r_size_layered_graphs as layered_graph_experiments
import experiments.computation_time_dependent_on_l_and_r_size_random_graphs as random_graph_experiments

if __name__ == "__main__":
    DO_RECOMPUTE = False

    # Runtime of STABILITY-NAIVE and FOUR-BOOL-LABEL on the toy example on fraud.
    for file_name in path_to_resources_folder().iterdir():
        file_name = file_name.parts[-1]
        if str(file_name).startswith('02'):
            experiment = TimingAndAccuracyExperiment(file_name[:-5], do_recompute=DO_RECOMPUTE)
            experiment.run_all_experiments()

    # Accuracy of toy example on fraud and artificial example
    for file_name in path_to_resources_folder().iterdir():
        file_name = file_name.parts[-1]
        if str(file_name).startswith('02') or str(file_name).startswith('04'):
            experiment = TimingAndAccuracyExperiment(file_name[:-5], do_recompute=DO_RECOMPUTE)
            experiment.run_all_experiments()

    # Experiment 2
    random_graph_experiments.main(do_recompute=DO_RECOMPUTE)

    # Experiment 3
    layered_graph_experiments.main(do_recompute=DO_RECOMPUTE)
