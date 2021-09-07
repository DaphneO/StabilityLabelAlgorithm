import random
from typing import Dict, List

from ..argumentation_system_generator_interface import ArgumentationSystemGeneratorInterface
from .layered_argumentation_system_generator_parameters import LayeredArgumentationSystemGeneratorParameters

from ....argumentation.argumentation_theory.literal import Literal
from ....argumentation.argumentation_theory.rule import Rule
from ....argumentation.argumentation_theory.queryable import Queryable
from ....argumentation.argumentation_theory.argumentation_system import ArgumentationSystem


class LayeredArgumentationSystemGenerator(ArgumentationSystemGeneratorInterface):
    def __init__(self, argumentation_system_generation_parameters: LayeredArgumentationSystemGeneratorParameters):
        super().__init__()
        self.argumentation_system_generation_parameters = argumentation_system_generation_parameters

    def generate(self) -> ArgumentationSystem:
        """
        Generate an ArgumentationSystem with a layered structure according to the
        LayeredArgumentationSystemGeneratorParameters.

        :return: The generated ArgumentationSystem.
        """
        max_remaining_tries = 25
        while max_remaining_tries > 0:
            try:
                max_remaining_tries -= 1
                layered_language = self._generate_language_initial()
                rules = self._generate_rules(layered_language)
                language = {str(literal): literal for literals in layered_language.values() for literal in literals}
                highest_layer = max(list(layered_language.keys()))
                topic_literals = layered_language[highest_layer]
                argumentation_system = ArgumentationSystem(language, rules, topic_literals=topic_literals)
                return argumentation_system
            except ValueError:
                pass
        raise ValueError('Could not generate an ArgumentationSystem with these properties.')

    def _generate_language_initial(self) -> Dict[int, List[Literal]]:
        positive_language_size = int(self.argumentation_system_generation_parameters.language_size / 2)
        layers = self.argumentation_system_generation_parameters.literal_layer_distribution.copy()

        layered_language = {layer_nr: [] for layer_nr in layers.keys()}

        for pos_literal_index in range(positive_language_size):
            literal_str_positive = 'lit' + str(pos_literal_index)
            literal_str_negative = '~lit' + str(pos_literal_index)
            literal_description_if_positive_present = literal_str_positive + ' is present.'
            literal_description_if_positive_not_present = literal_str_positive + ' is not present.'
            literal_description_if_negative_present = literal_str_negative + ' is present.'
            literal_description_if_negative_not_present = literal_str_negative + ' is not present.'

            # Get layer and update layers for future random layer choices
            new_literal_positive_layer = random.choices(list(layers.keys()), list(layers.values()), k=1)[0]
            layers[new_literal_positive_layer] -= 1
            new_literal_negative_layer = random.choices(list(layers.keys()), list(layers.values()), k=1)[0]
            layers[new_literal_negative_layer] -= 1

            if new_literal_positive_layer == 0 or new_literal_negative_layer == 0:
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
                # Generate a Literal: negative version
                new_literal_negative = Literal(literal_str_negative, literal_description_if_negative_present,
                                               literal_description_if_negative_not_present, False)

            # Connect negations / contraries
            new_literal_positive.negation = new_literal_negative
            new_literal_negative.negation = new_literal_positive
            new_literal_positive.contraries = [new_literal_negative]
            new_literal_negative.contraries = [new_literal_positive]

            # Add to layered language dict
            layered_language[new_literal_positive_layer].append(new_literal_positive)
            layered_language[new_literal_negative_layer].append(new_literal_negative)

        return layered_language

    def _generate_rules(self, layered_language: Dict[int, List[Literal]]):
        # Keep track of remaining antecedent options
        r_a_d = self.argumentation_system_generation_parameters.rule_antecedent_distribution.copy()

        rules = []

        # Start with the necessary rules
        necessary_consequents = [(literal, layer) for layer, literals in layered_language.items()
                                 for literal in literals
                                 if layer > 0]
        for consequent, consequent_layer in necessary_consequents:
            antecedents = []

            if not layered_language[consequent_layer - 1]:
                raise ValueError('Could not add a rule with the required number of literals')
            highest_antecedent = random.choice(layered_language[consequent_layer - 1])
            antecedents.append(highest_antecedent)

            nr_of_antecedents = random.choices(list(r_a_d.keys()), list(r_a_d.values()), k=1)[0]
            r_a_d[nr_of_antecedents] -= 1

            while len(antecedents) < nr_of_antecedents:
                antecedent_candidates = []
                for other_layer, other_literals in layered_language.items():
                    if other_layer < consequent_layer:
                        for other_literal in other_literals:
                            if other_literal not in antecedents and other_literal != consequent and \
                                    all([contrary not in antecedents and contrary != consequent
                                         for contrary in other_literal.contraries]):
                                antecedent_candidates.append(other_literal)

                if not antecedent_candidates:
                    raise ValueError('Could not add a rule with the required number of literals')

                new_antecedent = random.choice(antecedent_candidates)
                antecedents.append(new_antecedent)

            new_rule = Rule(len(rules), antecedents, consequent, '')
            new_rule.consequent.children.append(new_rule)
            for child in new_rule.antecedents:
                child.parents.append(new_rule)
            rules.append(new_rule)

        # Add additional rules
        while len(rules) < self.argumentation_system_generation_parameters.rule_size:
            if not necessary_consequents:
                raise ValueError('It is not possible to generate the required number of rules.')
            consequent, consequent_layer = random.choice(necessary_consequents)

            # Find antecedents
            nr_of_antecedents = random.choices(list(r_a_d.keys()), list(r_a_d.values()), k=1)[0]
            r_a_d[nr_of_antecedents] -= 1

            antecedents = []
            while len(antecedents) < nr_of_antecedents:
                antecedent_candidates = []
                for other_layer, other_literals in layered_language.items():
                    if other_layer < consequent_layer:
                        for other_literal in other_literals:
                            if other_literal not in antecedents and other_literal != consequent and \
                                    all([contrary not in antecedents and contrary != consequent
                                         for contrary in other_literal.contraries]):
                                antecedent_candidates.append(other_literal)

                if not antecedent_candidates:
                    raise ValueError('Could not add a rule with the required number of literals')

                new_antecedent = random.choice(antecedent_candidates)
                antecedents.append(new_antecedent)

            new_rule = Rule(len(rules), antecedents, consequent, '')
            new_rule.consequent.children.append(new_rule)
            for child in new_rule.antecedents:
                child.parents.append(new_rule)
            rules.append(new_rule)

        return rules
