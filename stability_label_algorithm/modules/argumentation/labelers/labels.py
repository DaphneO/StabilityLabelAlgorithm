from typing import Dict
from ..argumentation_theory.literal import Literal
from ..argumentation_theory.rule import Rule
from .stability_label import StabilityLabel


class Labels:
    """
    A Labels object consists of a Literal labeling, assigning StabilityLabels to Literals, and a Rule labeling,
    assigning StabilityLabels to Rules.
    """
    def __init__(self, literal_labeling: Dict[Literal, StabilityLabel], rule_labeling: Dict[Rule, StabilityLabel]):
        self.literal_labeling = literal_labeling
        self.rule_labeling = rule_labeling
