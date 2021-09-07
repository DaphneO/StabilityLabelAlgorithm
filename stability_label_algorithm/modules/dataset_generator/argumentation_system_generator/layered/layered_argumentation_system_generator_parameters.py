from typing import Dict


class LayeredArgumentationSystemGeneratorParameters:
    def __init__(self,
                 language_size: int,
                 rule_size: int,
                 rule_antecedent_distribution: Dict[int, int],
                 literal_layer_distribution: Dict[int, int]):
        """
        Parameters for randomly generating an ArgumentationSystem with a layered structure.

        :param language_size: The number of Literals (including negations).
        :param rule_size: The number of Rules.
        :param rule_antecedent_distribution: The number of Rules having a specific number of antecedents.
        :param literal_layer_distribution: The number of Literals in a specific layer.
        """
        if language_size % 2 != 0:
            raise ValueError('Language size should be even, since each literal should have a negated version.')
        self.language_size = language_size

        required_rules = sum([value for key, value in literal_layer_distribution.items() if key != 0])
        if rule_size < required_rules:
            raise ValueError('You need more rules to enable this literal layer distribution.')
        self.rule_size = rule_size

        possible_layers = sorted(literal_layer_distribution.keys())
        if 0 not in possible_layers:
            raise ValueError('There should at least be a literal of layer 0.')
        if any([x + 1 != y for x, y in zip(possible_layers[:-1], possible_layers[1:])]):
            raise ValueError('Each layer between the minimum and maximum should have a value.')
        if sum(literal_layer_distribution.values()) != language_size:
            raise ValueError('The sum of the literal layer distribution should equal the language size.')
        self.literal_layer_distribution = literal_layer_distribution

        if sum(rule_antecedent_distribution.values()) != rule_size:
            raise ValueError('The sum of the rule antecedent distribution should equal the rule size.')
        self.rule_antecedent_distribution = rule_antecedent_distribution

        if any([nr_antecedents > language_size / 2 for nr_antecedents in self.rule_antecedent_distribution.keys()]):
            raise ValueError('Rules cannot have more antecedents than half of the language size.')

    def __str__(self):
        return str(vars(self))

    def __repr__(self):
        return str(vars(self))
