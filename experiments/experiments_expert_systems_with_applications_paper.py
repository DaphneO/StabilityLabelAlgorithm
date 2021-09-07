from experiments.four_bool_timing_experiment import FourBoolTimingExperiment
from experiments.timing_and_accuracy_experiment import TimingAndAccuracyExperiment
from tests.utils import path_to_resources_folder

if __name__ == "__main__":
    # Runtime of STABILITY-NAIVE
    for file_name in path_to_resources_folder().iterdir():
        file_name = file_name.parts[-1]
        if str(file_name).startswith('02'):
            experiment = TimingAndAccuracyExperiment(file_name[:-5], do_recompute=True)
            experiment.run_all_experiments()
        elif str(file_name).startswith('01_2020_Police_Intake_System.xlsx'):
            experiment = FourBoolTimingExperiment(file_name[:-5], do_recompute=True)
            experiment.run_all_experiments()
