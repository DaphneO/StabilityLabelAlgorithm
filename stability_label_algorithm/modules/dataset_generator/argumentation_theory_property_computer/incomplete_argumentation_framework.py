import itertools
from typing import List, Tuple, Dict

from stability_label_algorithm.modules.argumentation.argumentation_theory.argumentation_theory import ArgumentationTheory
from stability_label_algorithm.modules.argumentation.argumentation_theory.literal import Literal
from stability_label_algorithm.modules.dataset_generator.argumentation_system_property_computer.potential_argument import \
    PotentialArgument
from stability_label_algorithm.modules.dataset_generator.argumentation_theory_property_computer.argument import Argument
from stability_label_algorithm.modules.dataset_generator.argumentation_theory_property_computer.argumentation_framework import \
    ArgumentationFramework


class IncompleteArgumentationFramework(ArgumentationFramework):
    def __init__(self, arguments_by_literal: Dict[Literal, List[Argument]],
                 potential_arguments_by_literal: Dict[Literal, List[PotentialArgument]]):
        super().__init__(arguments_by_literal)
        self.potential_arguments_by_literal = potential_arguments_by_literal

    @classmethod
    def from_argumentation_theory(cls, argumentation_theory: ArgumentationTheory):
        arguments_by_literal = cls.get_arguments(argumentation_theory)
        potential_arguments_by_literal = cls.get_potential_arguments(argumentation_theory)
        return cls(arguments_by_literal, potential_arguments_by_literal)

    @classmethod
    def create_empty(cls):
        return cls({}, {})

    @staticmethod
    def get_potential_arguments(argumentation_theory: ArgumentationTheory, verbose=False) -> \
            Dict[Literal, List[PotentialArgument]]:
        argumentation_system = argumentation_theory.argumentation_system
        potential_arguments = {literal: [] for literal in argumentation_system.language.values()}

        for literal in argumentation_system.language.values():
            if literal.is_observable:
                if literal in argumentation_theory.knowledge_base:
                    obs_based_argument = Argument.create_observation_based(literal, True)
                    potential_arguments[literal].append(obs_based_argument)
                elif all([contrary not in argumentation_theory.knowledge_base for contrary in literal.contraries]):
                    obs_based_potential_argument = PotentialArgument.create_observation_based(literal, False)
                    potential_arguments[literal].append(obs_based_potential_argument)

        change = True
        while change:
            change = False
            for rule in argumentation_system.rules:
                possible_antecedents = [potential_arguments[antecedent] for antecedent in rule.antecedents]
                if all(possible_antecedents):
                    for direct_subargument_tuple in itertools.product(*possible_antecedents):
                        direct_subarguments = list(direct_subargument_tuple)
                        if all([direct_subargument.is_argument for direct_subargument in direct_subarguments]):
                            new_potential_argument = Argument.create_rule_based(direct_subarguments, rule)
                        else:
                            new_potential_argument = PotentialArgument.create_rule_based(direct_subarguments, rule)
                        potential_arguments[rule.consequent].append(new_potential_argument)
                        if verbose:
                            print('Added ' + str(new_potential_argument))
        return potential_arguments

    @property
    def potential_arguments(self) -> List[PotentialArgument]:
        return [potential_argument for potential_argument_list in self.potential_arguments_by_literal.values()
                for potential_argument in potential_argument_list]

    @property
    def p_attacks(self) -> List[Tuple[PotentialArgument, PotentialArgument]]:
        p_attacks = []
        for attacker_candidate, attacked_candidate in itertools.product(self.potential_arguments, repeat=2):
            if attacker_candidate.p_attacks(attacked_candidate):
                p_attacks.append((attacker_candidate, attacked_candidate))
        return p_attacks
