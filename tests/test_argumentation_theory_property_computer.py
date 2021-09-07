import unittest

from stability_label_algorithm.modules.argumentation.argumentation_theory.argumentation_system \
    import ArgumentationSystem
from stability_label_algorithm.modules.argumentation.argumentation_theory.argumentation_theory \
    import ArgumentationTheory
from stability_label_algorithm.modules.argumentation.importers.argumentation_system_xlsx_reader \
    import ArgumentationSystemXLSXReader
from stability_label_algorithm.modules.dataset_generator.argumentation_theory_property_computer import \
    argumentation_theory_property_computer
from tests.utils import path_to_resources


class TestArgumentationTheoryPropertyComputer(unittest.TestCase):
    def test_argumentation_theory_property_computer_comma_example(self):
        # Load argumentation system
        arg_sys_file_name = '02_2020_COMMA_Paper_Example'
        asr = ArgumentationSystemXLSXReader(path_to_resources(arg_sys_file_name))
        arg_system = ArgumentationSystem(asr.language, asr.rules, asr.topic_literals)

        fraud_literal = arg_system.language['fraud']

        kb_str = []
        at = ArgumentationTheory(arg_system, [arg_system.get_queryable(s) for s in kb_str])
        at_properties = argumentation_theory_property_computer.compute_argumentation_theory_properties(at)
        self.assertEqual(len(at_properties.get_potential_arguments_for(fraud_literal)), 8)
        self.assertEqual(at_properties.nr_of_arguments, 0)
        self.assertEqual(at_properties.nr_of_potential_arguments, 31)
        self.assertEqual(at_properties.nr_of_attacks, 0)
        self.assertEqual(at_properties.nr_of_p_attacks, 16)
        self.assertEqual(at_properties.nr_of_inconsistent_potential_arguments, 6)
        self.assertEqual(len(at_properties.future_argumentation_theories),
                         3 ** len(arg_system.positive_queryables))

        kb_str = ['citizen_tried_to_buy', 'citizen_sent_money', 'suspicious_url']
        at = ArgumentationTheory(arg_system, [arg_system.get_queryable(s) for s in kb_str])
        at_properties = argumentation_theory_property_computer.compute_argumentation_theory_properties(at)
        self.assertEqual(at_properties.get_arguments_for(fraud_literal), [])
        self.assertEqual(at_properties.nr_of_arguments, 5)
        self.assertEqual(at_properties.nr_of_potential_arguments, 18)
        self.assertEqual(at_properties.nr_of_attacks, 0)
        self.assertEqual(at_properties.nr_of_p_attacks, 2)
        self.assertEqual(at_properties.nr_of_inconsistent_potential_arguments, 0)
        self.assertEqual(len(at_properties.future_argumentation_theories),
                         3 ** (len(at.future_knowledge_base_candidates) / 2))

        kb_str = ['citizen_tried_to_buy', 'citizen_sent_money', '~citizen_received_product', 'suspicious_url']
        at = ArgumentationTheory(arg_system, [arg_system.get_queryable(s) for s in kb_str])
        at_properties = argumentation_theory_property_computer.compute_argumentation_theory_properties(at)
        self.assertNotEqual(at_properties.get_arguments_for(fraud_literal), [])
        self.assertEqual(at_properties.nr_of_arguments, 8)
        self.assertEqual(at_properties.nr_of_potential_arguments, 17)
        self.assertEqual(at_properties.nr_of_attacks, 0)
        self.assertEqual(at_properties.nr_of_p_attacks, 2)
        self.assertEqual(at_properties.nr_of_inconsistent_potential_arguments, 0)
        self.assertEqual(len(at_properties.future_argumentation_theories),
                         3 ** (len(at.future_knowledge_base_candidates) / 2))
