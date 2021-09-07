import random
from typing import Dict

from ..argumentation_system_generator_interface import ArgumentationSystemGeneratorInterface
from .random_argumentation_system_generator_parameters import RandomArgumentationSystemGeneratorParameters

from ....argumentation.argumentation_theory.literal import Literal
from ....argumentation.argumentation_theory.rule import Rule
from ....argumentation.argumentation_theory.queryable import Queryable
from ....argumentation.argumentation_theory.argumentation_system import ArgumentationSystem


class RandomArgumentationSystemGenerator(ArgumentationSystemGeneratorInterface):
    def __init__(self, argumentation_system_generation_parameters: RandomArgumentationSystemGeneratorParameters):
        super().__init__()
        self.argumentation_system_generation_parameters = argumentation_system_generation_parameters

    def generate(self) -> ArgumentationSystem:
        """
        Randomly generate a new ArgumentationSystem based on the RandomArgumentationSystemGeneratorParameters.

        :return: The generated ArgumentationSystem.
        """
        language = self._generate_language()
        rules = self._generate_rules(language)
        argumentation_system = ArgumentationSystem(language, rules)
        return argumentation_system

    def _generate_language(self):
        positive_language_size = int(self.argumentation_system_generation_parameters.language_size / 2)
        positive_queryable_size = int(self.argumentation_system_generation_parameters.queryable_size / 2)
        positive_queryable_indices = random.sample(range(positive_language_size), k=positive_queryable_size)

        language = {}
        for pos_literal_index in range(positive_language_size):
            literal_str_positive = 'lit' + str(pos_literal_index)
            literal_str_negative = '~lit' + str(pos_literal_index)
            literal_description_if_positive_present = literal_str_positive + ' is present.'
            literal_description_if_positive_not_present = literal_str_positive + ' is not present.'
            literal_description_if_negative_present = literal_str_negative + ' is present.'
            literal_description_if_negative_not_present = literal_str_negative + ' is not present.'

            if pos_literal_index in positive_queryable_indices:
                # Generate a Queryable: positive version
                new_literal_positive = Queryable(literal_str_positive, literal_description_if_positive_present,
                                                 literal_description_if_positive_not_present,
                                                 'How about ' + literal_str_positive + '?',
                                                 'Seriously, how about ' + literal_str_positive + '?', 0)
                # Generate a Queryable: negative version
                new_literal_negative = Queryable(literal_str_negative, literal_description_if_negative_present,
                                                 literal_description_if_negative_not_present,
                                                 'How about ' + literal_str_negative + '?',
                                                 'Seriously, how about ' + literal_str_negative + '?', 0)
            else:
                # Generate a Literal: positive version
                new_literal_positive = Literal(literal_str_positive, literal_description_if_positive_present,
                                               literal_description_if_positive_not_present, False)
                new_literal_negative = Literal(literal_str_negative, literal_description_if_negative_present,
                                               literal_description_if_negative_not_present, False)

            # Connect negations / contraries
            new_literal_positive.negation = new_literal_negative
            new_literal_negative.negation = new_literal_positive
            new_literal_positive.contraries = [new_literal_negative]
            new_literal_negative.contraries = [new_literal_positive]

            # Add to language dict
            language[literal_str_positive] = new_literal_positive
            language[literal_str_negative] = new_literal_negative

        return language

    def _generate_rules(self, language: Dict[str, Literal]):
        rules = []
        rule_index = 0
        non_queryables = [literal for literal in language.values() if not literal.is_observable]

        for number_of_antecedents, number_of_rules in \
                self.argumentation_system_generation_parameters.rule_antecedent_distribution.items():
            for rule_index_within_antecedent_round in range(number_of_rules):
                # Consequent
                if self.argumentation_system_generation_parameters.allow_rules_for_queryables:
                    rule_consequent = random.choice(list(language.values()))
                else:
                    rule_consequent = random.choice(non_queryables)

                # Antecedents
                rule_antecedents = []
                rule_antecedent_candidates = [literal for literal in language.values()]
                if not self.argumentation_system_generation_parameters.allow_conclusion_in_antecedents:
                    rule_antecedent_candidates.remove(rule_consequent)
                    rule_antecedent_candidates.remove(rule_consequent.negation)
                for antecedent_index in range(number_of_antecedents):
                    if len(rule_antecedent_candidates) == 0:
                        break
                    new_antecedent = random.choice(rule_antecedent_candidates)
                    rule_antecedents.append(new_antecedent)
                    rule_antecedent_candidates.remove(new_antecedent)
                    if not self.argumentation_system_generation_parameters.allow_inconsistent_antecedents:
                        if new_antecedent.negation in rule_antecedent_candidates:
                            rule_antecedent_candidates.remove(new_antecedent.negation)

                # Description / name
                rule_description = 'rule' + str(rule_index)

                new_rule = Rule(rule_index, rule_antecedents, rule_consequent, rule_description)
                new_rule.consequent.children.append(new_rule)
                for child in new_rule.antecedents:
                    child.parents.append(new_rule)
                rules.append(new_rule)
                rule_index += 1

        return rules
