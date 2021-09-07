from .labels import Labels
from .labeler_interface import LabelerInterface
from .stability_label import StabilityLabel
from ..argumentation_theory.argumentation_theory import ArgumentationTheory


class SatisfiableLabeler(LabelerInterface):
    """
    The SatisfiableLabeler is used in the preprocessing step of the AcceptabilityLabeler. It checks for each Literal
    if there is an argument for the Literal in the current ArgumentationTheory and for each Rule if there is an argument
    based on this Rule in the current ArgumentationTheory.
    """
    def __init__(self):
        super().__init__()

    def label(self, argumentation_theory: ArgumentationTheory) -> Labels:
        labels = Labels(dict(), dict())

        for literal in argumentation_theory.argumentation_system.language.values():
            if literal in argumentation_theory.knowledge_base:
                labels.literal_labeling[literal] = StabilityLabel(False, True, True, True)
            else:
                labels.literal_labeling[literal] = StabilityLabel(True, False, False, False)
        for rule in argumentation_theory.argumentation_system.rules:
            labels.rule_labeling[rule] = StabilityLabel(True, False, False, False)

        label_changed = True

        while label_changed:
            label_changed = False
            for rule in argumentation_theory.argumentation_system.rules:
                if labels.rule_labeling[rule].unsatisfiable:
                    if all([not labels.literal_labeling[child].unsatisfiable for child in rule.antecedents]):
                        labels.rule_labeling[rule] = StabilityLabel(False, True, True, True)
                        labels.literal_labeling[rule.consequent] = StabilityLabel(False, True, True, True)
                        label_changed = True
        return labels
