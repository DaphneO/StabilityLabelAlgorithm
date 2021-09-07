from typing import Optional, Dict


class ArgumentationSystemProperties:
    def __init__(self,
                 nr_of_literals: int = 0,
                 nr_of_topics: int = 0,
                 nr_of_rules: int = 0,
                 nr_of_queryables: int = 0,
                 rule_antecedent_distribution: Optional[Dict[int, int]] = None):
        self.nr_of_literals = nr_of_literals
        self.nr_of_topics = nr_of_topics
        self.nr_of_rules = nr_of_rules
        self.nr_of_queryables = nr_of_queryables
        self.rule_antecedent_distribution = rule_antecedent_distribution
