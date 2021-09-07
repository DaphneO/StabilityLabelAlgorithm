import itertools
from typing import List, Tuple, Dict

from stability_label_algorithm.modules.argumentation.argumentation_theory.argumentation_theory import ArgumentationTheory
from stability_label_algorithm.modules.argumentation.argumentation_theory.literal import Literal
from stability_label_algorithm.modules.dataset_generator.argumentation_theory_property_computer.argument import Argument


class ArgumentationFramework:
    def __init__(self, arguments_by_literal: Dict[Literal, List[Argument]]):
        self.arguments_by_literal = arguments_by_literal

    @classmethod
    def from_argumentation_theory(cls, argumentation_theory: ArgumentationTheory):
        arguments_by_literal = cls.get_arguments(argumentation_theory)
        return cls(arguments_by_literal)

    @classmethod
    def create_empty(cls):
        return cls({})

    @staticmethod
    def get_arguments(argumentation_theory: ArgumentationTheory, verbose=False) -> Dict[Literal, List[Argument]]:
        argumentation_system = argumentation_theory.argumentation_system
        arguments = {literal: [] for literal in argumentation_system.language.values()}

        for literal in argumentation_theory.knowledge_base:
            obs_based_argument = Argument.create_observation_based(literal, True)
            arguments[literal].append(obs_based_argument)

        change = True
        while change:
            change = False
            for rule in argumentation_system.rules:
                possible_antecedents = [arguments[antecedent] for antecedent in rule.antecedents]
                if all(possible_antecedents):
                    for direct_subargument_tuple in itertools.product(*possible_antecedents):
                        try:
                            new_argument = Argument(list(direct_subargument_tuple), rule.consequent, rule)
                            arguments[rule.consequent].append(new_argument)
                            if verbose:
                                print('Added ' + str(new_argument))
                        except ValueError:
                            if verbose:
                                print('No consistent argument could be made from ' +
                                      ', '.join([str(pa) for pa in direct_subargument_tuple]))
        return arguments

    @property
    def arguments(self):
        return [argument for argument_list in self.arguments_by_literal.values() for argument in argument_list]

    @property
    def attacks(self) -> List[Tuple[Argument, Argument]]:
        attacks = []
        for attacker_candidate, attacked_candidate in itertools.product(self.arguments, repeat=2):
            if attacker_candidate.attacks(attacked_candidate):
                attacks.append((attacker_candidate, attacked_candidate))
        return attacks
