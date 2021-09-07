import unittest

from stability_label_algorithm.modules.argumentation.importers.argumentation_system_xlsx_reader import \
    ArgumentationSystemXLSXReader
from stability_label_algorithm.modules.argumentation.argumentation_theory.argumentation_system import \
    ArgumentationSystem
from stability_label_algorithm.modules.argumentation.argumentation_engine import ArgumentationEngine
from stability_label_algorithm.modules.argumentation.labelers.fqas_labeler import FQASLabeler
from stability_label_algorithm.modules.argumentation.labelers.four_bool_labeler import FourBoolLabeler
from stability_label_algorithm.modules.argumentation.labelers.satisfiability_labeler import SatisfiabilityLabeler
from stability_label_algorithm.modules.argumentation.labelers.acceptability_labeler import JustificationLabeler

from tests.utils import path_to_resources


class TestStability(unittest.TestCase):
    def test_fraud_mini_test(self):
        asr = ArgumentationSystemXLSXReader(path_to_resources('03_2019_FQAS_Paper_Example'))
        arg_system = ArgumentationSystem(asr.language, asr.rules, asr.topic_literals)
        arg_engine_four_bool = ArgumentationEngine(arg_system, FourBoolLabeler())
        arg_engine_fqas = ArgumentationEngine(arg_system, FQASLabeler())
        arg_engine_acceptability = ArgumentationEngine(arg_system, JustificationLabeler())
        arg_engine_satisfiablility = ArgumentationEngine(arg_system, SatisfiabilityLabeler())

        arg_engine_fqas_output = arg_engine_fqas.update(['wrong_product'])
        self.assertFalse(
            arg_engine_fqas_output.labels.literal_labeling[arg_system.language['fraud']].is_stable)
        self.assertFalse(
            arg_engine_fqas_output.labels.literal_labeling[arg_system.language['fraud']].is_contested_stable)

        arg_engine_fqas_output = arg_engine_fqas.update(['wrong_product', 'counter_party_delivered'])
        self.assertTrue(
            arg_engine_fqas_output.labels.literal_labeling[arg_system.language['fraud']].is_stable)

        arg_engine_fqas_output = arg_engine_fqas.update(['counter_party_delivered'])
        self.assertTrue(
            arg_engine_fqas_output.labels.literal_labeling[arg_system.language['fraud']].is_contested_stable)

        arg_engine_four_bool_output = arg_engine_four_bool.update(['wrong_product'])
        self.assertFalse(
            arg_engine_four_bool_output.labels.literal_labeling[arg_system.language['fraud']].is_stable)
        self.assertTrue(
            arg_engine_four_bool_output.labels.literal_labeling[arg_system.language['fraud']].is_contested_stable)

        arg_engine_four_bool_output = arg_engine_four_bool.update(['wrong_product', 'counter_party_delivered'])
        self.assertTrue(
            arg_engine_four_bool_output.labels.literal_labeling[arg_system.language['fraud']].is_stable)

        arg_engine_four_bool_output = arg_engine_four_bool.update(['counter_party_delivered'])
        self.assertTrue(
            arg_engine_four_bool_output.labels.literal_labeling[arg_system.language['fraud']].is_contested_stable)

        arg_engine_satisfiability_output = arg_engine_satisfiablility.update([])
        self.assertFalse(
            arg_engine_satisfiability_output.labels.literal_labeling[arg_system.language['fraud']].is_stable)

        arg_engine_acceptability_output = arg_engine_acceptability.update([])
        fraud_acc_label = arg_engine_acceptability_output.labels.literal_labeling[arg_system.language['fraud']]
        self.assertTrue(fraud_acc_label.is_stable and fraud_acc_label.unsatisfiable)

        arg_engine_acceptability_output = arg_engine_acceptability.update(['paid', '~sent', '~counter_party_delivered'])
        fraud_acc_label = arg_engine_acceptability_output.labels.literal_labeling[arg_system.language['fraud']]
        self.assertTrue(fraud_acc_label.is_stable and fraud_acc_label.defended)

        arg_engine_acceptability_output = arg_engine_acceptability.update(['paid', '~sent', '~counter_party_delivered',
                                                                           'wrong_product'])
        fraud_acc_label = arg_engine_acceptability_output.labels.literal_labeling[arg_system.language['fraud']]
        self.assertTrue(fraud_acc_label.is_stable and fraud_acc_label.blocked)
        cp_acc_label = \
            arg_engine_acceptability_output.labels.literal_labeling[arg_system.language['counter_party_delivered']]
        self.assertTrue(fraud_acc_label.is_stable and cp_acc_label.out)

    def test_inconsistent_premise_test(self):
        asr = ArgumentationSystemXLSXReader(path_to_resources('counter01_inconsistent_premises'))
        arg_system = ArgumentationSystem(asr.language, asr.rules, asr.topic_literals)
        arg_engine_four_bool = ArgumentationEngine(arg_system, FourBoolLabeler())
        arg_engine_fqas = ArgumentationEngine(arg_system, FQASLabeler())
        arg_engine_acceptability = ArgumentationEngine(arg_system, JustificationLabeler())
        arg_engine_satisfiablility = ArgumentationEngine(arg_system, SatisfiabilityLabeler())

        arg_engine_fqas_output = arg_engine_fqas.update([])
        self.assertFalse(arg_engine_fqas_output.labels.literal_labeling[arg_system.language['t']].is_stable)

        arg_engine_four_bool_output = arg_engine_four_bool.update([])
        self.assertFalse(arg_engine_four_bool_output.labels.literal_labeling[arg_system.language['t']].is_stable)

        arg_engine_satisfiability_output = arg_engine_satisfiablility.update([])
        self.assertFalse(arg_engine_satisfiability_output.labels.literal_labeling[arg_system.language['t']].is_stable)

        arg_engine_acceptability_output = arg_engine_acceptability.update([])
        t_acc_label = arg_engine_acceptability_output.labels.literal_labeling[arg_system.language['t']]
        self.assertTrue(t_acc_label.is_stable and t_acc_label.unsatisfiable)
        arg_engine_acceptability_output = arg_engine_acceptability.update(['a'])
        t_acc_label = arg_engine_acceptability_output.labels.literal_labeling[arg_system.language['t']]
        self.assertTrue(t_acc_label.is_stable and t_acc_label.unsatisfiable)
        arg_engine_acceptability_output = arg_engine_acceptability.update(['~a'])
        t_acc_label = arg_engine_acceptability_output.labels.literal_labeling[arg_system.language['t']]
        self.assertTrue(t_acc_label.is_stable and t_acc_label.unsatisfiable)

    def test_support_cycle(self):
        asr = ArgumentationSystemXLSXReader(path_to_resources('counter02_support_cycle'))
        arg_system = ArgumentationSystem(asr.language, asr.rules, asr.topic_literals)
        arg_engine_four_bool = ArgumentationEngine(arg_system, FourBoolLabeler())
        arg_engine_fqas = ArgumentationEngine(arg_system, FQASLabeler())
        arg_engine_satisfiablility = ArgumentationEngine(arg_system, SatisfiabilityLabeler())

        arg_engine_fqas_output = arg_engine_fqas.update([])
        self.assertFalse(arg_engine_fqas_output.labels.literal_labeling[arg_system.language['t']].is_stable)

        arg_engine_four_bool_output = arg_engine_four_bool.update([])
        self.assertTrue(arg_engine_four_bool_output.labels.literal_labeling[arg_system.language['t']].is_stable)

        arg_engine_satisfiability_output = arg_engine_satisfiablility.update([])
        self.assertTrue(arg_engine_satisfiability_output.labels.literal_labeling[arg_system.language['t']].is_stable)

    def test_attack_cycle(self):
        asr = ArgumentationSystemXLSXReader(path_to_resources('counter03_attack_cycle'))
        arg_system = ArgumentationSystem(asr.language, asr.rules, asr.topic_literals)
        arg_engine_four_bool = ArgumentationEngine(arg_system, FourBoolLabeler())
        arg_engine_fqas = ArgumentationEngine(arg_system, FQASLabeler())
        arg_engine_acceptability = ArgumentationEngine(arg_system, JustificationLabeler())

        arg_engine_fqas_output = arg_engine_fqas.update(['o1', 'o2'])
        self.assertFalse(arg_engine_fqas_output.labels.literal_labeling[arg_system.language['t']].is_stable)

        arg_engine_four_bool_output = arg_engine_four_bool.update(['o1', 'o2'])
        self.assertTrue(arg_engine_four_bool_output.labels.literal_labeling[arg_system.language['t']].is_stable)

        arg_engine_acceptability_output = arg_engine_acceptability.update(['o1', 'o2'])
        t_acc_label = arg_engine_acceptability_output.labels.literal_labeling[arg_system.language['t']]
        self.assertTrue(t_acc_label.is_stable and t_acc_label.blocked)

    def test_ou_irrelevant_d_lit_c(self):
        asr = ArgumentationSystemXLSXReader(path_to_resources('counter04_OU_irrelevant_in_D_lit_c'))
        arg_system = ArgumentationSystem(asr.language, asr.rules, asr.topic_literals)
        arg_engine_four_bool = ArgumentationEngine(arg_system, FourBoolLabeler())
        arg_engine_fqas = ArgumentationEngine(arg_system, FQASLabeler())

        arg_engine_fqas_output = arg_engine_fqas.update(['o1', 'o2'])
        self.assertFalse(arg_engine_fqas_output.labels.literal_labeling[arg_system.language['t']].is_stable)

        arg_engine_four_bool_output = arg_engine_four_bool.update(['o1', 'o2'])
        self.assertTrue(arg_engine_four_bool_output.labels.literal_labeling[arg_system.language['t']].is_stable)

    def test_bou_irrelevant_b_lit_b(self):
        asr = ArgumentationSystemXLSXReader(path_to_resources('counter05_BOU_irrelevant_in_B_lit_b'))
        arg_system = ArgumentationSystem(asr.language, asr.rules, asr.topic_literals)
        arg_engine_four_bool = ArgumentationEngine(arg_system, FourBoolLabeler())
        arg_engine_fqas = ArgumentationEngine(arg_system, FQASLabeler())

        arg_engine_fqas_output = arg_engine_fqas.update(['o1', 'o2', 'o5'])
        self.assertFalse(arg_engine_fqas_output.labels.literal_labeling[arg_system.language['t']].is_stable)

        arg_engine_four_bool_output = arg_engine_four_bool.update(['o1', 'o2', 'o5'])
        self.assertTrue(arg_engine_four_bool_output.labels.literal_labeling[arg_system.language['t']].is_stable)

    def test_db_irrelevant_b_lit_a(self):
        asr = ArgumentationSystemXLSXReader(path_to_resources('counter06_DB_irrelevant_in_B_lit_a'))
        arg_system = ArgumentationSystem(asr.language, asr.rules, asr.topic_literals)
        arg_engine_four_bool = ArgumentationEngine(arg_system, FourBoolLabeler())
        arg_engine_fqas = ArgumentationEngine(arg_system, FQASLabeler())

        arg_engine_fqas_output = arg_engine_fqas.update(['o1'])
        self.assertFalse(arg_engine_fqas_output.labels.literal_labeling[arg_system.language['t']].is_stable)

        arg_engine_four_bool_output = arg_engine_four_bool.update(['o1'])
        self.assertTrue(arg_engine_four_bool_output.labels.literal_labeling[arg_system.language['t']].is_stable)

    def test_dbo_irrelevant_o_lit_a(self):
        asr = ArgumentationSystemXLSXReader(path_to_resources('counter07_DBO_irrelevant_in_O_lit_a'))
        arg_system = ArgumentationSystem(asr.language, asr.rules, asr.topic_literals)
        arg_engine_four_bool = ArgumentationEngine(arg_system, FourBoolLabeler())
        arg_engine_fqas = ArgumentationEngine(arg_system, FQASLabeler())

        arg_engine_fqas_output = arg_engine_fqas.update(['o1', '~t'])
        self.assertFalse(arg_engine_fqas_output.labels.literal_labeling[arg_system.language['t']].is_stable)

        arg_engine_four_bool_output = arg_engine_four_bool.update(['o1', '~t'])
        self.assertTrue(arg_engine_four_bool_output.labels.literal_labeling[arg_system.language['t']].is_stable)

    def test_uo_irrelevant_o_lit_b(self):
        asr = ArgumentationSystemXLSXReader(path_to_resources('counter08_UO_irrelevant_in_O_lit_b'))
        arg_system = ArgumentationSystem(asr.language, asr.rules, asr.topic_literals)
        arg_engine_four_bool = ArgumentationEngine(arg_system, FourBoolLabeler())
        arg_engine_fqas = ArgumentationEngine(arg_system, FQASLabeler())

        arg_engine_fqas_output = arg_engine_fqas.update(['o1', 'o2', 'o3'])
        self.assertFalse(arg_engine_fqas_output.labels.literal_labeling[arg_system.language['t']].is_stable)

        arg_engine_four_bool_output = arg_engine_four_bool.update(['o1', 'o2', 'o3'])
        self.assertTrue(arg_engine_four_bool_output.labels.literal_labeling[arg_system.language['t']].is_stable)

    def test_dbo_irrelevant_o_rule(self):
        asr = ArgumentationSystemXLSXReader(path_to_resources('counter09_DBO_irrelevant_in_O_rule'))
        arg_system = ArgumentationSystem(asr.language, asr.rules, asr.topic_literals)
        arg_engine_four_bool = ArgumentationEngine(arg_system, FourBoolLabeler())
        arg_engine_fqas = ArgumentationEngine(arg_system, FQASLabeler())

        arg_engine_fqas_output = arg_engine_fqas.update(['o3', 'o4', 'o5'])
        self.assertFalse(arg_engine_fqas_output.labels.literal_labeling[arg_system.language['t']].is_stable)

        arg_engine_four_bool_output = arg_engine_four_bool.update(['o3', 'o4', 'o5'])
        self.assertTrue(arg_engine_four_bool_output.labels.literal_labeling[arg_system.language['t']].is_stable)

    def test_db_irrelevant_b_rule(self):
        asr = ArgumentationSystemXLSXReader(path_to_resources('counter10_DB_irrelevant_in_B_rule'))
        arg_system = ArgumentationSystem(asr.language, asr.rules, asr.topic_literals)
        arg_engine_four_bool = ArgumentationEngine(arg_system, FourBoolLabeler())
        arg_engine_fqas = ArgumentationEngine(arg_system, FQASLabeler())

        arg_engine_fqas_output = arg_engine_fqas.update(['o2', 'o3', 'o4'])
        self.assertFalse(arg_engine_fqas_output.labels.literal_labeling[arg_system.language['t']].is_stable)

        arg_engine_four_bool_output = arg_engine_four_bool.update(['o2', 'o3', 'o4'])
        self.assertTrue(arg_engine_four_bool_output.labels.literal_labeling[arg_system.language['t']].is_stable)

    def test_support_cycle_attacker(self):
        asr = ArgumentationSystemXLSXReader(path_to_resources('counter11_support_cycle_attacker'))
        arg_system = ArgumentationSystem(asr.language, asr.rules, asr.topic_literals)
        arg_engine_four_bool = ArgumentationEngine(arg_system, FourBoolLabeler())
        arg_engine_fqas = ArgumentationEngine(arg_system, FQASLabeler())

        arg_engine_fqas_output = arg_engine_fqas.update(['o'])
        self.assertFalse(arg_engine_fqas_output.labels.literal_labeling[arg_system.language['t']].is_stable)

        arg_engine_four_bool_output = arg_engine_four_bool.update(['o'])
        self.assertTrue(arg_engine_four_bool_output.labels.literal_labeling[arg_system.language['t']].is_stable)

    def test_support_cycle_attacker_q(self):
        asr = ArgumentationSystemXLSXReader(path_to_resources('counter12_support_cycle_attacker_q'))
        arg_system = ArgumentationSystem(asr.language, asr.rules, asr.topic_literals)
        arg_engine_four_bool = ArgumentationEngine(arg_system, FourBoolLabeler())
        arg_engine_fqas = ArgumentationEngine(arg_system, FQASLabeler())

        arg_engine_fqas_output = arg_engine_fqas.update(['o'])
        self.assertFalse(arg_engine_fqas_output.labels.literal_labeling[arg_system.language['t']].is_stable)

        arg_engine_four_bool_output = arg_engine_four_bool.update(['o'])
        self.assertFalse(arg_engine_four_bool_output.labels.literal_labeling[arg_system.language['t']].is_stable)


if __name__ == '__main__':
    unittest.main()
