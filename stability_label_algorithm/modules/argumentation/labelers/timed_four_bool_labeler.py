from typing import Tuple

from .four_bool_labeler import FourBoolLabeler
from .labels import Labels
from .satisfiability_labeler import SatisfiabilityLabeler
from ..argumentation_theory.argumentation_theory import ArgumentationTheory


class TimedFourBoolLabeler(FourBoolLabeler):
    """
    This is a timed version of the regular FourBoolLabeler, which returns not only the Labels but only the number of
    calls to the methods for relabelling Literals and Rules.
    """
    def __init__(self):
        super().__init__()

    def label(self, argumentation_theory: ArgumentationTheory) -> Tuple[Labels, int, int]:
        """
        Assign Labels to each Literal and Rule in the ArgumentationTheory and record the number of calls to the methods
        for relabelling Literals and Rules.

        :param argumentation_theory: ArgumentationTheory that should be labelled.
        :return: Labels for the ArgumentationTheory, number of calls relabelling Literals and Rules.
        """
        relabel_literal_calls = 0
        relabel_rule_calls = 0

        # Preprocessing: take the initial labeling from the SatisfiabilityLabeler
        labels = SatisfiabilityLabeler().label(argumentation_theory)
        rules_visited = {rule: False for rule in argumentation_theory.argumentation_system.rules}

        # Start by coloring leaves (literals for which there is no rule) and observables (O(|L|))
        leaves_and_observables = [literal for literal in argumentation_theory.argumentation_system.language.values()
                                  if not literal.children or literal.is_observable]
        rules_to_reconsider = set()
        for literal in leaves_and_observables:  # Max |L| iterations
            self.color_literal(argumentation_theory, literal, labels)  # Max |L||R_l/-l| executions in total = c*|R|
            relabel_literal_calls += 1
            rules_to_reconsider = rules_to_reconsider | set(literal.parents)

        # Color rules and (contraries of) their conclusions
        while rules_to_reconsider:
            # Each rule r is considered (i.e. added to rules_to_reconsider) at most 4*|ants(r)| times.
            rule = rules_to_reconsider.pop()

            # Store old label so we can check if the label changed.
            old_rule_label = labels.rule_labeling[rule].__copy__()

            # This takes c*|ants(r)| steps for each consideration of r. So in total O(|R|^2|L|) steps.
            self.color_rule(rule, labels)
            relabel_rule_calls += 1

            # If this was the first time the rule was considered or if its label changed, it may influence others.
            if not rules_visited[rule] or labels.rule_labeling[rule] != old_rule_label:
                # Considering a literal l takes c*|R| steps. It only happens after initially considering or changing the
                # label of a rule for l/-l, so at most 4*|R_l/-l| times. So in total considering all literals all times
                # takes O(|R|^2) steps.
                old_literal_label = labels.literal_labeling[rule.consequent].__copy__()
                self.color_literal(argumentation_theory, rule.consequent, labels)
                relabel_literal_calls += 1
                if labels.literal_labeling[rule.consequent] != old_literal_label:
                    rules_to_reconsider = rules_to_reconsider | set(rule.consequent.parents)
                for contrary_literal in rule.consequent.contraries:
                    old_contrary_literal_label = labels.literal_labeling[contrary_literal].__copy__()
                    self.color_literal(argumentation_theory, contrary_literal, labels)
                    relabel_literal_calls += 1
                    if labels.literal_labeling[contrary_literal] != old_contrary_literal_label:
                        rules_to_reconsider = rules_to_reconsider | set(contrary_literal.parents)
                rules_visited[rule] = True

        return labels, relabel_literal_calls, relabel_rule_calls
