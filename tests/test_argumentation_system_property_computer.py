import unittest

from stability_label_algorithm.modules.argumentation.argumentation_theory.argumentation_system \
    import ArgumentationSystem
from stability_label_algorithm.modules.argumentation.importers.argumentation_system_xlsx_reader \
    import ArgumentationSystemXLSXReader
from stability_label_algorithm.modules.dataset_generator.argumentation_system_property_computer.\
    argumentation_system_property_computer import compute_argumentation_system_properties
from tests.utils import path_to_resources


class TestArgumentationSystemPropertyComputer(unittest.TestCase):
    def test_argumentation_system_property_computer_comma_example(self):
        # Load argumentation system
        arg_sys_file_name = '02_2020_COMMA_Paper_Example'
        asr = ArgumentationSystemXLSXReader(path_to_resources(arg_sys_file_name))
        arg_system = ArgumentationSystem(asr.language, asr.rules, asr.topic_literals)

        # Compute argumentation system properties
        arg_sys_properties = compute_argumentation_system_properties(arg_system)

        self.assertEqual(arg_sys_properties.nr_of_literals, 24)
        self.assertEqual(arg_sys_properties.nr_of_queryables, 16)
        self.assertEqual(arg_sys_properties.nr_of_rules, 8)
        self.assertEqual(arg_sys_properties.nr_of_topics, 1)
