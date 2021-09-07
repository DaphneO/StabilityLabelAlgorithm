from typing import List, Optional, Set

from stability_label_algorithm.modules.argumentation.argumentation_theory.literal import Literal
from stability_label_algorithm.modules.argumentation.argumentation_theory.rule import Rule
from stability_label_algorithm.modules.dataset_generator.argumentation_system_property_computer.potential_argument import \
    PotentialArgument


class Argument(PotentialArgument):
    def __init__(self, direct_subarguments: List['Argument'], conclusion: Literal, top_rule: Optional[Rule]):
        super().__init__(direct_subarguments, conclusion, top_rule, True)
        if not self.is_consistent:
            raise ValueError('This cannot be an argument since the premises are inconsistent.')

    @classmethod
    def create_observation_based(cls, conclusion: Literal, *args):
        return cls([], conclusion, None)

    @classmethod
    def create_rule_based(cls, direct_subarguments: List['Argument'], top_rule: Rule):
        return cls(direct_subarguments, top_rule.consequent, top_rule)

    @property
    def subarguments(self) -> Set['Argument']:
        if self.is_observation_based:
            return {self}
        return {self} | {subargument for direct_subargument in self.direct_subarguments
                         for subargument in direct_subargument.subarguments}

    def attacks(self, other: 'Argument'):
        return any([other_sub_arg.conclusion in self.conclusion.contraries
                    and not other_sub_arg.is_observation_based
                    for other_sub_arg in other.subarguments])
