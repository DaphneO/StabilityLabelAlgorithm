from stability_label_algorithm.modules.argumentation.argumentation_theory.argumentation_system import ArgumentationSystem
from stability_label_algorithm.modules.dataset_generator.argumentation_system_property_computer.argumentation_system_properties \
    import ArgumentationSystemProperties


def compute_argumentation_system_properties(argumentation_system: ArgumentationSystem) -> \
        ArgumentationSystemProperties:
    """
    Compute some properties of the given ArgumentationSystem, such as the number of literals or rule antecedents.

    :param argumentation_system: ArgumentationSystem for which properties are needed.
    :return: ArgumentationSystemProperties of the ArgumentationSystem.
    """
    properties = ArgumentationSystemProperties()
    properties.nr_of_literals = len(argumentation_system.language)
    properties.nr_of_topics = len(argumentation_system.topic_literals)
    properties.nr_of_rules = len(argumentation_system.rules)
    properties.nr_of_queryables = len([q for q in argumentation_system.language.values() if q.is_observable])
    rule_antecedents = [len(rule.antecedents) for rule in argumentation_system.rules]
    properties.rule_antecedent_distribution = {antecedent_nr: rule_antecedents.count(antecedent_nr)
                                               for antecedent_nr in sorted(list(set(rule_antecedents)))}
    return properties
