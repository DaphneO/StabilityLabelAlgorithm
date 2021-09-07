from .labels import Labels
from .labeler_interface import LabelerInterface
from ..argumentation_theory.argumentation_theory import ArgumentationTheory
from .satisfiable_labeler import SatisfiableLabeler


class JustificationLabeler(LabelerInterface):
    """
    The JustificationLabeler labels literals according to their justification status. For example, if a literal is
    defended in the current ArgumentationTheory, then it is assigned the StabilityLabel(False, True, False, False).
    In order to do so, it uses the SatisfiableLabeler in the preprocessing step.
    """
    def __init__(self):
        super().__init__()

    def label(self, argumentation_theory: ArgumentationTheory) -> Labels:
        labels = SatisfiableLabeler().label(argumentation_theory)
        rules_visited = {rule: False for rule in argumentation_theory.argumentation_system.rules}

        # Start by coloring observed literals
        leaves_and_observables = [literal for literal in argumentation_theory.argumentation_system.language.values()
                                  if not literal.children or literal.is_observable]
        rules_to_reconsider = set()
        for literal in leaves_and_observables:
            self.color_literal(argumentation_theory, literal, labels)
            rules_to_reconsider = rules_to_reconsider | set(literal.parents)

        # Color rules and (contraries of) their conclusions
        while rules_to_reconsider:
            # Each rule r is considered (i.e. added to rules_to_reconsider) at most 4*|ants(r)| times.
            rule = rules_to_reconsider.pop()

            # Store old label so we can check if the label changed.
            old_rule_label = labels.rule_labeling[rule].__copy__()

            # This takes c*|ants(r)| steps for each consideration of r. So in total O(|R|^2|L|) steps.
            self.color_rule(rule, labels)

            # If this was the first time the rule was considered or if its label changed, it may influence others.
            if not rules_visited[rule] or labels.rule_labeling[rule] != old_rule_label:
                # Considering a literal l takes c*|R| steps. It only happens after initially considering or changing the
                # label of a rule for l/-l, so at most 4*|R_l/-l| times. So in total considering all literals all times
                # takes O(|R|^2) steps.
                old_literal_label = labels.literal_labeling[rule.consequent].__copy__()
                self.color_literal(argumentation_theory, rule.consequent, labels)
                if labels.literal_labeling[rule.consequent] != old_literal_label:
                    rules_to_reconsider = rules_to_reconsider | set(rule.consequent.parents)
                for contrary_literal in rule.consequent.contraries:
                    old_contrary_literal_label = labels.literal_labeling[contrary_literal].__copy__()
                    self.color_literal(argumentation_theory, contrary_literal, labels)
                    if labels.literal_labeling[contrary_literal] != old_contrary_literal_label:
                        rules_to_reconsider = rules_to_reconsider | set(contrary_literal.parents)
                rules_visited[rule] = True

        return labels

    @staticmethod
    def color_literal(argumentation_theory, literal, labels):
        """
        Color the Literal, that is: check, based on observations/Rules for this Literal/Rules for its contraries, if
        this Literal may be unsatisfiable, defended, out or blocked.
        """
        if literal.is_observable:
            if literal in argumentation_theory.knowledge_base:
                labels.literal_labeling[literal].blocked = False            # L-B-a
                labels.literal_labeling[literal].out = False                # L-O-a
            else:
                if any([contrary_literal in argumentation_theory.knowledge_base
                        for contrary_literal in literal.contraries]):
                    labels.literal_labeling[literal].blocked = False        # L-B-b
                    labels.literal_labeling[literal].defended = False       # L-D-a

        if literal not in argumentation_theory.knowledge_base:
            if all([not labels.rule_labeling[rule].defended for rule in literal.children]):
                labels.literal_labeling[literal].defended = False           # L-D-b
            if any([not labels.rule_labeling[contrary_rule].unsatisfiable and
                    not labels.rule_labeling[contrary_rule].out
                    for contrary_literal in literal.contraries
                    for contrary_rule in contrary_literal.children]):
                labels.literal_labeling[literal].defended = False           # L-D-c

        if all([contrary_literal not in argumentation_theory.knowledge_base
                for contrary_literal in literal.contraries]):
            if all([not labels.rule_labeling[rule].out for rule in literal.children]):
                labels.literal_labeling[literal].out = False                # L-O-b
            if any([not labels.rule_labeling[rule].unsatisfiable and not labels.rule_labeling[rule].out
                    for rule in literal.children]):
                labels.literal_labeling[literal].out = False                # L-O-c

        if all([not labels.rule_labeling[rule].defended and
                not labels.rule_labeling[rule].blocked for rule in literal.children]):
            labels.literal_labeling[literal].blocked = False                # L-B-c
        if all([not labels.rule_labeling[rule].blocked for rule in literal.children]) and \
                all([not labels.rule_labeling[contrary_rule].blocked and
                     not labels.rule_labeling[contrary_rule].defended
                     for contrary_literal in literal.contraries
                     for contrary_rule in contrary_literal.children]):
            labels.literal_labeling[literal].blocked = False                # L-B-d
        if any([not labels.rule_labeling[rule].unsatisfiable and not labels.rule_labeling[rule].out and
                not labels.rule_labeling[rule].blocked
                for rule in literal.children]) and \
                all([not labels.rule_labeling[contrary_rule].blocked and
                     not labels.rule_labeling[contrary_rule].defended
                     for contrary_literal in literal.contraries
                     for contrary_rule in contrary_literal.children]):
            labels.literal_labeling[literal].blocked = False                # L-B-e

    @staticmethod
    def color_rule(rule, labels):
        """
        Color the Rule, that is: check, based on its antecedents, if this Rule can still become unsatisfiable, defended,
        out or blocked.
        """
        if any([not labels.literal_labeling[literal].defended for literal in rule.antecedents]):
            labels.rule_labeling[rule].defended = False                     # R-D-a

        if all([not labels.literal_labeling[literal].out for literal in rule.antecedents]):
            labels.rule_labeling[rule].out = False                          # R-O-a

        if all([not labels.literal_labeling[literal].blocked for literal in rule.antecedents]):
            labels.rule_labeling[rule].blocked = False                      # R-B-a
        if any([not labels.literal_labeling[literal].blocked and
                not labels.literal_labeling[literal].defended for literal in rule.antecedents]):
            labels.rule_labeling[rule].blocked = False                      # R-B-b
