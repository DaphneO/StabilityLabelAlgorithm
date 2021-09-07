from .argumentation_engine_output import ArgumentationEngineOutput
from .argumentation_theory.argumentation_system import ArgumentationSystem
from .argumentation_theory.argumentation_theory import ArgumentationTheory
from .labelers.labeler_interface import LabelerInterface


class ArgumentationEngine:
    def __init__(self, argumentation_system: ArgumentationSystem, labeler: LabelerInterface):
        self.argumentation_system = argumentation_system
        self.labeler = labeler

    def _get_consistent_observations(self, input_observations_str: [str]):
        output_observations = []

        input_observations = self.argumentation_system.get_queryables(input_observations_str)

        for observation in input_observations:
            if all([not observation.is_contrary_of(other_observation) for other_observation in input_observations]):
                output_observations.append(observation)
            else:
                pass

        return output_observations

    def update(self, observations):
        # Consistency check
        consistent_observations = self._get_consistent_observations(observations)

        # Argumentation system and consistent observations form an argumentation theory
        argumentation_theory = ArgumentationTheory(self.argumentation_system, consistent_observations)
        labels = self.labeler.label(argumentation_theory)

        return ArgumentationEngineOutput(labels)
