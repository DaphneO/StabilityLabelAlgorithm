import unittest

from stability_label_algorithm.modules.dataset_generator.argumentation_system_generator.random.\
    random_argumentation_system_generator import RandomArgumentationSystemGenerator
from stability_label_algorithm.modules.dataset_generator.argumentation_system_generator.random.\
    random_argumentation_system_generator_parameters import RandomArgumentationSystemGeneratorParameters
from stability_label_algorithm.modules.dataset_generator.dataset_generator import DatasetGenerator


class TestDatasetGenerator(unittest.TestCase):
    def test_random_argumentation_system_generation(self):
        argumentation_system_generation_parameters = \
            RandomArgumentationSystemGeneratorParameters(10, 4, {1: 2, 2: 2}, 2)
        argumentation_system_generator = RandomArgumentationSystemGenerator(argumentation_system_generation_parameters)
        argumentation_system = argumentation_system_generator.generate()
        self.assertEqual(argumentation_system_generation_parameters.language_size,
                         len(argumentation_system.language))
        self.assertEqual(argumentation_system_generation_parameters.rule_size,
                         len(argumentation_system.rules))
        self.assertEqual(argumentation_system_generation_parameters.queryable_size,
                         len([q for q in argumentation_system.language.values() if q.is_observable]))
        for nr_antecedents, nr_rules in argumentation_system_generation_parameters.rule_antecedent_distribution.items():
            self.assertEqual(nr_rules, len([rule for rule in argumentation_system.rules
                                            if len(rule.antecedents) == nr_antecedents]))

    def test_dataset_generation(self):
        # Generate argumentation system
        argumentation_system_generation_parameters = \
            RandomArgumentationSystemGeneratorParameters(language_size=8, rule_size=10,
                                                         rule_antecedent_distribution={1: 9, 2: 1},
                                                         queryable_size=6,
                                                         allow_conclusion_in_antecedents=False,
                                                         allow_inconsistent_antecedents=False,
                                                         allow_rules_for_queryables=True)
        argumentation_system_generator = RandomArgumentationSystemGenerator(argumentation_system_generation_parameters)
        argumentation_system = argumentation_system_generator.generate()

        dataset_generator = DatasetGenerator(argumentation_system)
        dataset = dataset_generator.generate_dataset()
        for dataset_item in dataset.dataset_items:
            argumentation_system = dataset_item.argumentation_system
            self.assertEqual(argumentation_system_generation_parameters.language_size,
                             len(argumentation_system.language))
            self.assertEqual(argumentation_system_generation_parameters.rule_size,
                             len(argumentation_system.rules))
            self.assertEqual(argumentation_system_generation_parameters.queryable_size,
                             len([q for q in argumentation_system.language.values() if q.is_observable]))
            for nr_antecedents, nr_rules in \
                    argumentation_system_generation_parameters.rule_antecedent_distribution.items():
                self.assertEqual(nr_rules, len([rule for rule in argumentation_system.rules
                                                if len(rule.antecedents) == nr_antecedents]))


if __name__ == '__main__':
    unittest.main()
