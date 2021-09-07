import unittest

from stability_label_algorithm.modules.argumentation.argumentation_theory.argumentation_theory import ArgumentationTheory
from stability_label_algorithm.modules.dataset_generator.argumentation_system_generator.layered.\
    layered_argumentation_system_generator import LayeredArgumentationSystemGenerator
from stability_label_algorithm.modules.dataset_generator.argumentation_system_generator.layered.\
    layered_argumentation_system_generator_parameters import LayeredArgumentationSystemGeneratorParameters
from stability_label_algorithm.modules.dataset_generator.argumentation_system_property_computer.\
    argumentation_system_property_computer import \
    compute_argumentation_system_properties
from stability_label_algorithm.modules.dataset_generator.argumentation_theory_property_computer.\
    incomplete_argumentation_framework import \
    IncompleteArgumentationFramework


class TestLayeredDatasetGenerator(unittest.TestCase):
    def test_layered_argumentation_system_generation(self):
        # LayeredArgumentationSystemGeneratorParameters
        literal_layer_distribution = {0: 3, 1: 2, 2: 1}
        nr_of_literals = 6
        nr_of_rules = 3
        rule_antecedent_distribution = {1: 2, 2: 1}
        argumentation_system_generation_parameters = \
            LayeredArgumentationSystemGeneratorParameters(nr_of_literals, nr_of_rules,
                                                          rule_antecedent_distribution, literal_layer_distribution)

        # Generate argumentation system
        argumentation_system_generator = LayeredArgumentationSystemGenerator(argumentation_system_generation_parameters)
        argumentation_system = argumentation_system_generator.generate()

        # Check number of literals and rules
        argumentation_system_properties = compute_argumentation_system_properties(argumentation_system)
        self.assertEqual(nr_of_literals, argumentation_system_properties.nr_of_literals)
        self.assertEqual(nr_of_rules, argumentation_system_properties.nr_of_rules)
        self.assertEqual(rule_antecedent_distribution, argumentation_system_properties.rule_antecedent_distribution)

        # Check layers
        empty_argumentation_theory = ArgumentationTheory(argumentation_system, [])
        inc_arg_fw = IncompleteArgumentationFramework.from_argumentation_theory(empty_argumentation_theory)
        actual_literal_layers = [max([pot_arg.height for pot_arg in pot_arg_list])
                                 for pot_arg_list in inc_arg_fw.potential_arguments_by_literal.values()]
        actual_literal_layer_distribution = {layer_nr: actual_literal_layers.count(layer_nr)
                                             for layer_nr in sorted(list(set(actual_literal_layers)))}
        self.assertEqual(literal_layer_distribution, actual_literal_layer_distribution)

    def test_impossible_rule_antecedent_distribution(self):
        literal_layer_distribution = {0: 4}
        nr_of_literals = 4
        nr_of_rules = 1
        rule_antecedent_distribution = {2: 1}
        argumentation_system_generation_parameters = \
            LayeredArgumentationSystemGeneratorParameters(nr_of_literals, nr_of_rules,
                                                          rule_antecedent_distribution, literal_layer_distribution)
        argumentation_system_generator = LayeredArgumentationSystemGenerator(argumentation_system_generation_parameters)

        with self.assertRaises(ValueError):
            argumentation_system_generator.generate()

    def test_two_layer_argumentation_system_generation(self):
        literal_layer_distribution = {0: 19, 1: 1}
        nr_of_literals = 20
        nr_of_rules = 25
        rule_antecedent_distribution = {3: 15, 2: 10}
        argumentation_system_generation_parameters = \
            LayeredArgumentationSystemGeneratorParameters(nr_of_literals, nr_of_rules,
                                                          rule_antecedent_distribution, literal_layer_distribution)

        # Generate argumentation system
        argumentation_system_generator = LayeredArgumentationSystemGenerator(argumentation_system_generation_parameters)
        argumentation_system = argumentation_system_generator.generate()

        # Check number of literals and rules
        argumentation_system_properties = compute_argumentation_system_properties(argumentation_system)
        self.assertEqual(nr_of_literals, argumentation_system_properties.nr_of_literals)
        self.assertEqual(nr_of_rules, argumentation_system_properties.nr_of_rules)
        self.assertEqual(rule_antecedent_distribution, argumentation_system_properties.rule_antecedent_distribution)

        # Check layers
        empty_argumentation_theory = ArgumentationTheory(argumentation_system, [])
        inc_arg_fw = IncompleteArgumentationFramework.from_argumentation_theory(empty_argumentation_theory)
        actual_literal_layers = [max([pot_arg.height for pot_arg in pot_arg_list])
                                 for pot_arg_list in inc_arg_fw.potential_arguments_by_literal.values()]
        actual_literal_layer_distribution = {layer_nr: actual_literal_layers.count(layer_nr)
                                             for layer_nr in sorted(list(set(actual_literal_layers)))}
        self.assertEqual(literal_layer_distribution, actual_literal_layer_distribution)


if __name__ == '__main__':
    unittest.main()
