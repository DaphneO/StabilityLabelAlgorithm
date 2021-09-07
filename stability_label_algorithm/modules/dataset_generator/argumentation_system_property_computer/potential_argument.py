from typing import List, Optional, Set

from stability_label_algorithm.modules.argumentation.argumentation_theory.literal import Literal
from stability_label_algorithm.modules.argumentation.argumentation_theory.rule import Rule
from stability_label_algorithm.modules.test_consistency_queryable_set import queryable_set_is_consistent


class PotentialArgument:
    def __init__(self, direct_subarguments: List['PotentialArgument'],
                 conclusion: Literal,
                 top_rule: Optional[Rule],
                 is_argument: bool):
        self.direct_subarguments = direct_subarguments
        self.conclusion = conclusion
        self.top_rule = top_rule
        self.is_argument = is_argument

    @classmethod
    def create_observation_based(cls, conclusion: Literal, is_observed: bool):
        return cls([], conclusion, None, is_observed)

    @classmethod
    def create_rule_based(cls, direct_subarguments: List['PotentialArgument'], top_rule: Rule):
        return cls(direct_subarguments, top_rule.consequent, top_rule,
                   all([sub_arg.is_argument for sub_arg in direct_subarguments]))

    @property
    def is_observation_based(self) -> bool:
        return not self.direct_subarguments and not self.top_rule

    @property
    def is_consistent(self):
        return queryable_set_is_consistent(list(self.premises))

    @property
    def is_rule_based(self) -> bool:
        return not self.is_observation_based

    @property
    def premises(self) -> Set[Literal]:
        if self.is_observation_based:
            return {self.conclusion}
        return {premise for subargument in self.direct_subarguments for premise in subargument.premises}

    @property
    def subarguments(self) -> Set['PotentialArgument']:
        if self.is_observation_based:
            return {self}
        return {self} | {subargument for direct_subargument in self.direct_subarguments
                         for subargument in direct_subargument.subarguments}

    @property
    def defeasible_rules(self) -> Optional[Set[Rule]]:
        if self.is_observation_based:
            return None
        return

    @property
    def height(self) -> int:
        if self.is_observation_based:
            return 0
        return max([subargument.height for subargument in self.direct_subarguments]) + 1

    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        if self.is_observation_based:
            return str(self.conclusion)
        direct_substring_str = ', '.join(sorted([str(subargument) for subargument in self.direct_subarguments]))
        return f'[{direct_substring_str} => {str(self.conclusion)}]'

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self)

    def p_attacks(self, other: 'PotentialArgument') -> bool:
        return any([other_sub_arg.conclusion in self.conclusion.contraries
                    and not other_sub_arg.is_observation_based
                    for other_sub_arg in other.subarguments])
