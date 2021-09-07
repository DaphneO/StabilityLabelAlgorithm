from .labels import Labels
from .labeler_interface import LabelerInterface
from .satisfiability_labeler import SatisfiabilityLabeler
from ..argumentation_theory.argumentation_theory import ArgumentationTheory


class FourBoolLabeler(LabelerInterface):
    """
    The FourBoolLabeler is the labeler presented at COMMA 2020 (version with classical negation) and submitted to ESwA.
    This Labeler uses the SatisfiabilityLabeler as preprocessing step and subsequently iteratively checks which of the
    four booleans in the StabilityLabels can be turned from True to False.
    """

    def __init__(self):
        super().__init__()

    def label(self, argumentation_theory: ArgumentationTheory) -> Labels:
        # Preprocessing: take the initial labeling from the SatisfiabilityLabeler
        labels = SatisfiabilityLabeler().label(argumentation_theory)
        rules_visited = {rule: False for rule in argumentation_theory.argumentation_system.rules}

        # Start by coloring leaves (literals for which there is no rule) and observables
        leaves_and_observables = [literal for literal in argumentation_theory.argumentation_system.language.values()
                                  if not literal.children or literal.is_observable]
        rules_to_reconsider = set()
        for literal in leaves_and_observables:
            self.color_literal(argumentation_theory, literal, labels)
            rules_to_reconsider = rules_to_reconsider | set(literal.parents)

        # Color rules and (contraries of) their conclusions
        while rules_to_reconsider:
            rule = rules_to_reconsider.pop()

            # Store old label so we can check if the label changed.
            old_rule_label = labels.rule_labeling[rule].__copy__()

            self.color_rule(rule, labels)

            # If this was the first time the rule was considered or if its label changed, it may influence others.
            if not rules_visited[rule] or labels.rule_labeling[rule] != old_rule_label:
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
        Color the Literal, that is: check, based on observations/rules for this literal/rules for its contraries, if
        this Literal can still become unsatisfiable/defended/out/blocked.
        """
        if literal.is_observable and literal in argumentation_theory.knowledge_base:
            # L-U-a: The literal is observed, so it cannot be unsatisfiable.
            labels.literal_labeling[literal].unsatisfiable = False
        elif any([not labels.rule_labeling[rule].unsatisfiable for rule in literal.children]):
            # L-U-b: There is a rule-based argument for the literal, so it cannot be unsatisfiable.
            labels.literal_labeling[literal].unsatisfiable = False

        if literal.is_observable:
            if any([contrary_literal in argumentation_theory.knowledge_base
                    for contrary_literal in literal.contraries]):
                # L-D-a: A contrary of the literal is observed, so the literal cannot be in the grounded extension.
                labels.literal_labeling[literal].defended = False
        else:
            if all([not labels.rule_labeling[rule].defended for rule in literal.children]):
                # L-D-b: The literal is not observable and there is no defended rule, so the literal cannot be defended.
                labels.literal_labeling[literal].defended = False
            elif any([not labels.rule_labeling[contrary_rule].unsatisfiable and
                      not labels.rule_labeling[contrary_rule].out
                      for contrary_literal in literal.contraries
                      for contrary_rule in contrary_literal.children]):
                # L-D-c: The literal is not observable and there is a defended or blocked rule for a contrary, so the
                # literal cannot be defended.
                labels.literal_labeling[literal].defended = False

        if literal.is_observable:
            if literal in argumentation_theory.knowledge_base:
                # L-O-a: Observed literals cannot be out.
                labels.literal_labeling[literal].out = False
            elif all([any([contrary_contrary_literal in argumentation_theory.knowledge_base
                           for contrary_contrary_literal in contrary_literal.contraries])
                      for contrary_literal in literal.contraries]):
                if all([not labels.rule_labeling[rule].out for rule in literal.children]):
                    # L-O-b
                    labels.literal_labeling[literal].out = False
                elif any([not labels.rule_labeling[rule].unsatisfiable and not labels.rule_labeling[rule].out
                          for rule in literal.children]):
                    # L-O-c
                    labels.literal_labeling[literal].out = False
        else:
            if all([not labels.rule_labeling[rule].out for rule in literal.children]):
                # L-O-d
                labels.literal_labeling[literal].out = False
            elif any([not labels.rule_labeling[rule].unsatisfiable and not labels.rule_labeling[rule].out
                      for rule in literal.children]):
                # L-O-e
                labels.literal_labeling[literal].out = False
        if all([not labels.rule_labeling[rule].defended and not labels.rule_labeling[rule].out and
                not labels.rule_labeling[rule].blocked for rule in literal.children]):
            # L-O-f: There is no rule-based argument for the literal, so the literal cannot be out.
            labels.literal_labeling[literal].out = False

        if literal.is_observable:
            # L-B-a: Observable literals cannot be blocked (only defended or unsatisfiable).
            labels.literal_labeling[literal].blocked = False
        elif all([not labels.rule_labeling[rule].defended and
                  not labels.rule_labeling[rule].blocked for rule in literal.children]):
            # L-B-b: There is no defended or blocked rule-based argument for the literal, so it cannot be blocked.
            labels.literal_labeling[literal].blocked = False
        elif all([not labels.rule_labeling[contrary_rule].blocked and
                  not labels.rule_labeling[contrary_rule].defended
                  for contrary_literal in literal.contraries
                  for contrary_rule in contrary_literal.children]):
            if all([not labels.rule_labeling[rule].blocked for rule in literal.children]):
                # L-B-c: There is no rule-based counterargument that is strong enough.
                labels.literal_labeling[literal].blocked = False
            elif any([not labels.rule_labeling[rule].unsatisfiable and not labels.rule_labeling[rule].out and
                      not labels.rule_labeling[rule].blocked
                      for rule in literal.children]):
                # L-B-d: There is a rule-based argument in the grounded extension.
                labels.literal_labeling[literal].blocked = False
            
    @staticmethod
    def color_rule(rule, labels):
        """
        Color the Rule, that is: check, based on is children, if this Rule can still become
        unsatisfiable/defended/out/blocked.
        """
        if all([not labels.literal_labeling[literal].unsatisfiable for literal in rule.antecedents]):
            # R-U-a: None of the antecedents can become unsatisfiable, so the rule cannot be unsatisfiable.
            labels.rule_labeling[rule].unsatisfiable = False

        if any([not labels.literal_labeling[literal].defended for literal in rule.antecedents]):
            # R-D-a: At least one of the antecedents cannot become defended, so the rule cannot be defended.
            labels.rule_labeling[rule].defended = False

        if all([not labels.literal_labeling[literal].out for literal in rule.antecedents]):
            # R-O-a: None of the antecedents can become out, so the rule cannot be out.
            labels.rule_labeling[rule].out = False

        if all([not labels.literal_labeling[literal].blocked for literal in rule.antecedents]):
            # R-B-a: None of the antecedents can become blocked, so the rule cannot be blocked.
            labels.rule_labeling[rule].blocked = False
        if any([not labels.literal_labeling[literal].blocked and
                not labels.literal_labeling[literal].defended for literal in rule.antecedents]):
            # R-B-b: At least one of the antecedents cannot become defended or blocked, so the rule cannot be blocked.
            labels.rule_labeling[rule].blocked = False
