import pandas

from ..argumentation_theory.argumentation_system import ArgumentationSystem
from ..argumentation_theory.literal import Literal
from ..argumentation_theory.queryable import Queryable
from ..argumentation_theory.rule import Rule


class ArgumentationSystemJsonReader:
    def __init__(self):
        pass

    @staticmethod
    def from_json(json_object):
        # First round: add literals
        language = {}
        for literal_str, literal_dict in json_object['literals'].items():
            if literal_dict['is_observable']:
                language[literal_str] = Queryable(literal_dict['literal_str'],
                                                  literal_dict['description_if_present'],
                                                  literal_dict['description_if_not_present'],
                                                  literal_dict['natural_language_query'],
                                                  literal_dict['long_natural_language_query'],
                                                  literal_dict['priority'])
            else:
                language[literal_str] = Literal(literal_dict['literal_str'],
                                                literal_dict['description_if_present'],
                                                literal_dict['description_if_not_present'],
                                                literal_dict['is_observable'])

        # Add rules
        rules = {}
        for rule_dict in json_object['rules']:
            rule_id = rule_dict['id']
            new_rule = Rule(rule_id,
                            [language[antecedent_str] for antecedent_str in rule_dict['antecedents_str']],
                            language[rule_dict['consequent_str']],
                            rule_dict['rule_description'])
            new_rule.consequent.children.append(new_rule)
            for child in new_rule.antecedents:
                child.parents.append(new_rule)

            rules[rule_id] = new_rule

        # Second round: add relations between literals
        for literal_str, literal_dict in json_object['literals'].items():
            language[literal_str].contraries = [language[contrary_str]
                                                for contrary_str in literal_dict['contraries_str']]
            language[literal_str].negation = language[literal_dict['negation_str']]

        # Add rule preferences
        if 'rule_preferences' in json_object and json_object['rule_preferences']:
            rule_preferences = pandas.read_json(json_object['rule_preferences'])
        else:
            rule_preferences = None

        # Add topic literals
        if 'topic_literals' in json_object and json_object['topic_literals']:
            topic_literals = [language[literal_str] for literal_str in json_object['topic_literals']]
        else:
            topic_literals = None

        return ArgumentationSystem(language, list(rules.values()),
                                   rule_preferences=rule_preferences,
                                   topic_literals=topic_literals)

    def read_from_json(self, file_path: str) -> ArgumentationSystem:
        with open(file_path, 'r') as reader:
            argumentation_system_json = reader.read()
        return self.from_json(argumentation_system_json)
