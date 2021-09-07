from typing import List, Union

from ..argumentation_theory.argumentation_theory import ArgumentationTheory
from ..argumentation_theory.literal import Literal
from ..argumentation_theory.queryable import Queryable
from .acceptability_labeler import JustificationLabeler
from .labeler_interface import LabelerInterface
from .labels import Labels
from .stability_label import StabilityLabel
from ...dataset_generator.argumentation_theory_property_computer.argumentation_theory_property_computer import \
    enumerate_future_argumentation_theories


class NaiveStabilityLabeler(LabelerInterface):
    """
    An exact but extremely slow labeler for detecting stability. Given some ArgumentationTheory, NaiveStabilityLabeler
    generates all future ArgumentationTheories and runs the JustificationLabeler's label algorithm on each of them.
    Only if the label is the same for all future ArgumentationTheories, the corresponding Literal or Rule is labelled
    stable. This algorithm is exponential.
    """
    def __init__(self):
        super().__init__()

    def label(self, argumentation_theory: ArgumentationTheory) -> Labels:
        labels = Labels(dict(), dict())
        for literal in argumentation_theory.argumentation_system.language.values():
            labels.literal_labeling[literal] = StabilityLabel(False, False, False, False)
        for rule in argumentation_theory.argumentation_system.rules:
            labels.rule_labeling[rule] = StabilityLabel(False, False, False, False)

        all_possible_future_argumentation_theories = \
            enumerate_future_argumentation_theories(argumentation_theory)
        for possible_future_argumentation_theory in all_possible_future_argumentation_theories:
            acc_labels = JustificationLabeler().label(possible_future_argumentation_theory)

            for literal in argumentation_theory.argumentation_system.language.values():
                labels.literal_labeling[literal] += acc_labels.literal_labeling[literal]
            for rule in argumentation_theory.argumentation_system.rules:
                labels.rule_labeling[rule] += acc_labels.rule_labeling[rule]

        return labels

    @staticmethod
    def _is_consistent(queryable_list: List[Union[Literal, Queryable]]):
        for i1 in range(len(queryable_list)):
            for i2 in range(i1 + 1, len(queryable_list)):
                if queryable_list[i1].is_contrary_of(queryable_list[i2]):
                    return False
        return True
