import json
from ..argumentation_theory.argumentation_system import ArgumentationSystem


class ArgumentationSystemJsonWriter:
    def __init__(self):
        pass

    @staticmethod
    def to_json(argumentation_system: ArgumentationSystem) -> str:
        json_dict = {'literals': {}, 'rules': []}
        for literal_str, literal in argumentation_system.language.items():
            if literal.is_observable:
                json_dict['literals'][literal_str] = {
                    'is_observable': literal.is_observable,
                    'literal_str': literal.s1,
                    'description_if_present': literal.description_if_present,
                    'description_if_not_present': literal.description_if_not_present,
                    'contraries_str': [str(contrary) for contrary in literal.contraries],
                    'negation_str': str(literal.negation),
                    'natural_language_query': literal.natural_language_query,
                    'long_natural_language_query': literal.long_natural_language_query,
                    'priority': int(literal.priority)
                }
            else:
                json_dict['literals'][literal_str] = {
                    'is_observable': literal.is_observable,
                    'literal_str': literal.s1,
                    'description_if_present': literal.description_if_present,
                    'description_if_not_present': literal.description_if_not_present,
                    'contraries_str': [str(contrary) for contrary in literal.contraries],
                    'negation_str': str(literal.negation)
                }

        for rule in argumentation_system.rules:
            json_dict['rules'].append(
                {'id': rule.id, 'antecedents_str': [str(antecedent) for antecedent in rule.antecedents],
                 'consequent_str': str(rule.consequent), 'rule_description': rule.rule_description})

        if argumentation_system.topic_literals is not None:
            json_dict['topic_literals'] = [str(topic_literal) for topic_literal in argumentation_system.topic_literals]

        return json.dumps(json_dict)

    def write_to_json(self, argumentation_system: ArgumentationSystem, file_path: str):
        with open(file_path, 'w') as writer:
            writer.write(self.to_json(argumentation_system))
