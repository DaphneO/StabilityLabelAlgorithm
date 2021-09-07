from typing import Optional, Dict


class RandomArgumentationSystemGeneratorParameters:
    def __init__(self, language_size: int, rule_size: Optional[int], rule_antecedent_distribution: Dict[int, float],
                 queryable_size: Optional[int] = None, queryable_ratio: Optional[float] = None,
                 allow_rules_for_queryables: bool = True, allow_conclusion_in_antecedents: bool = True,
                 allow_inconsistent_antecedents: bool = True):
        """
        Parameters for randomly generating an ArgumentationSystem.

        :param language_size: Number of Literals (including negations)
        :param rule_size: Number of Rules
        :param rule_antecedent_distribution: Number of Rules with a specific number of antecedents.
        :param queryable_size: Number of Queryables.
        :param queryable_ratio: Fraction of Queryables by the number of Literals.
        :param allow_rules_for_queryables: Boolean indicating if there can be Rules for Queryables.
        :param allow_conclusion_in_antecedents: Boolean indicating if a Rule can have its conclusion as an antecedent.
        :param allow_inconsistent_antecedents: Boolean indicating if a Rule can have inconsistent antecedents.
        """
        if language_size % 2 != 0:
            raise ValueError('Language size should be even, since each literal should have a negated version.')
        self.language_size = language_size

        if queryable_size is None and queryable_ratio is None:
            raise ValueError('Specify either queryable_size or queryable_ratio.')
        if queryable_size is not None and queryable_ratio is not None:
            raise ValueError('Specify either queryable_size or queryable_ratio (not both).')

        if queryable_size is not None:
            if queryable_size % 2 != 0:
                raise ValueError('Queryable size should be even, since each queryable should have a negated version.')
            if queryable_size > language_size:
                raise ValueError('Queryable size should not exceed language size.')
            self.queryable_size = queryable_size
        elif queryable_ratio is not None:
            if queryable_ratio > 1:
                raise ValueError('Queryable size should not exceed language size.')
            self.queryable_size = int(self.language_size * queryable_ratio)

        if rule_size is None:
            rule_size = sum(rule_antecedent_distribution.values())
        self.rule_size = rule_size

        if sum(rule_antecedent_distribution.values()) == rule_size:
            self.rule_antecedent_distribution = rule_antecedent_distribution
        elif sum(rule_antecedent_distribution.values()) == 1:
            self.rule_antecedent_distribution = {nr_ants: int(proportion * self.rule_size)
                                                 for (nr_ants, proportion) in rule_antecedent_distribution.items()}
        else:
            raise ValueError('Distribution rule_antecedent_distribution should either add to one or to rule_size.')
        if any([nr_antecedents > language_size / 2 for nr_antecedents in self.rule_antecedent_distribution.keys()]):
            raise ValueError('Rules cannot have more antecedents than half of the language size.')

        self.allow_rules_for_queryables = allow_rules_for_queryables
        self.allow_conclusion_in_antecedents = allow_conclusion_in_antecedents
        self.allow_inconsistent_antecedents = allow_inconsistent_antecedents

    def __str__(self):
        return str(vars(self))

    def __repr__(self):
        return str(vars(self))
