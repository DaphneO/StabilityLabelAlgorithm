from .labels import Labels
from .labeler_interface import LabelerInterface
from .stability_label import StabilityLabel
from ..argumentation_theory.argumentation_theory import ArgumentationTheory


class SatisfiabilityLabeler(LabelerInterface):
    """
    Proprocessing step of the FourBoolLabeler. Checks for each Literal if there is a potential argument for this Literal
    and for each Rule if there is a potential argument based on this Rule.
    """
    def __init__(self):
        super().__init__()

    @staticmethod
    def _preprocess_visit(rule, labels):
        if labels.rule_labeling[rule].defended:
            return False
        if all([labels.literal_labeling[literal].defended for literal in rule.antecedents]):
            labels.rule_labeling[rule] = StabilityLabel(True, True, True, True)
            labels.literal_labeling[rule.consequent] = StabilityLabel(True, True, True, True)
            return True
        return False

    def label(self, argumentation_theory: ArgumentationTheory) -> Labels:
        labels = Labels(dict(), dict())

        for literal in argumentation_theory.argumentation_system.language.values():
            if literal.is_observable and all([contrary not in argumentation_theory.knowledge_base
                                              for contrary in literal.contraries]):
                labels.literal_labeling[literal] = StabilityLabel(True, True, True, True)
            else:
                labels.literal_labeling[literal] = StabilityLabel(True, False, False, False)

        for rule in argumentation_theory.argumentation_system.rules:
            labels.rule_labeling[rule] = StabilityLabel(True, False, False, False)

        label_added = True
        while label_added:
            label_added = False
            for rule in argumentation_theory.argumentation_system.rules:
                label_added = self._preprocess_visit(rule, labels) or label_added

        return labels
