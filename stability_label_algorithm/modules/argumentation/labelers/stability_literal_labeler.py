from .labels import Labels
from .labeler_interface import LabelerInterface
from .stability_label import StabilityLabel
from ..argumentation_theory.argumentation_theory import ArgumentationTheory


class StabilityLiteralLabeler(LabelerInterface):
    def __init__(self):
        super().__init__()

    def label(self, argumentation_theory: ArgumentationTheory) -> Labels:
        labels = Labels(dict(), dict())

        for literal in argumentation_theory.argumentation_system.language.values():
            if literal.is_observable and all([contrary not in argumentation_theory.knowledge_base
                                              for contrary in literal.contraries]):
                labels.literal_labeling[literal] = StabilityLabel(True, True, True, True)
            else:
                labels.literal_labeling[literal] = StabilityLabel(True, False, False, False)

        label_changed = True

        while label_changed:
            label_changed = False
            for rule in argumentation_theory.argumentation_system.rules:
                if labels.literal_labeling[rule.consequent] != StabilityLabel(True, True, True, True):
                    if all([labels.literal_labeling[child] == StabilityLabel(True, True, True, True)
                            for child in rule.antecedents]):
                        labels.literal_labeling[rule.consequent] = StabilityLabel(True, True, True, True)
                        label_changed = True
        return labels
