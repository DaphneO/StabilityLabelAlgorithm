from .labels import Labels
from .stability_label import StabilityLabel
from .labeler_interface import LabelerInterface
from ..argumentation_theory.argumentation_theory import ArgumentationTheory


class FQASLabeler(LabelerInterface):
    """
    This is an initial labeler for stability, as presented at FQAS 2019. The FQASLabeler only assigns a single label
    (here modelled as the "stable" StabilityLabels) corresponding to stable justification statuses or some unknown
    label (here modelled as StableLabel(True, True, True, True)) for Literals and Rules that are not recognised as
    being stable. Note that this algorithm recognises less stable situations than the FourBoolLabeler.
    """

    def __init__(self):
        super().__init__()
        self.literal_labeling = {}
        self.rule_labeling = {}
        self.rules_visited = dict()

    def label(self, argumentation_theory: ArgumentationTheory) -> Labels:
        self.literal_labeling = {literal: StabilityLabel(True, True, True, True)
                                 for literal in argumentation_theory.argumentation_system.language.values()}
        self.rule_labeling = {rule: StabilityLabel(True, True, True, True)
                              for rule in argumentation_theory.argumentation_system.rules}
        self.rules_visited = {rule: False for rule in argumentation_theory.argumentation_system.rules}

        # Start by coloring leaves (literals for which there is no rule) and observables (O(|L|))
        leaves_and_observables = [literal for literal in argumentation_theory.argumentation_system.language.values()
                                  if not literal.children or literal.is_observable]
        rules_to_reconsider = set()
        for literal in leaves_and_observables:  # Max |L| iterations
            self.color_literal(argumentation_theory, literal)  # Max |L||R_l/-l| executions in total = c*|R|
            rules_to_reconsider = rules_to_reconsider | set(literal.parents)

        # Color rules and (contraries of) their conclusions
        while rules_to_reconsider:
            # Each rule r is considered (i.e. added to rules_to_reconsider) at most 4*|ants(r)| times.
            rule = rules_to_reconsider.pop()

            # Store old label so we can check if the label changed.
            old_rule_label = self.rule_labeling[rule].__copy__()

            # This takes c*|ants(r)| steps for each consideration of r. So in total O(|R|^2|L|) steps.
            self.color_rule(rule)

            # If this was the first time the rule was considered or if its label changed, it may influence others.
            if not self.rules_visited[rule] or self.rule_labeling[rule] != old_rule_label:
                # Considering a literal l takes c*|R| steps. It only happens after initially considering or changing the
                # label of a rule for l/-l, so at most 4*|R_l/-l| times. So in total considering all literals all times
                # takes O(|R|^2) steps.
                old_literal_label = self.literal_labeling[rule.consequent].__copy__()
                self.color_literal(argumentation_theory, rule.consequent)
                if self.literal_labeling[rule.consequent] != old_literal_label:
                    rules_to_reconsider = rules_to_reconsider | set(rule.consequent.parents)
                for contrary_literal in rule.consequent.contraries:
                    old_contrary_literal_label = self.literal_labeling[contrary_literal].__copy__()
                    self.color_literal(argumentation_theory, contrary_literal)
                    if self.literal_labeling[contrary_literal] != old_contrary_literal_label:
                        rules_to_reconsider = rules_to_reconsider | set(contrary_literal.parents)
                self.rules_visited[rule] = True

        return Labels(self.literal_labeling, self.rule_labeling)

    def color_literal(self, argumentation_theory, literal):
        """
        Color the Literal, that is: check, based on observations/rules for this literal/rules for its contraries, if
        this Literal can still become unsatisfiable/defended/out/blocked.
        """
        if literal.is_observable:
            if literal in argumentation_theory.knowledge_base:
                # D literal A
                self.literal_labeling[literal] = StabilityLabel(False, True, False, False)
            elif any([contrary_literal in argumentation_theory.knowledge_base
                      for contrary_literal in literal.contraries]):
                if all([self.rule_labeling[rule] == StabilityLabel(True, False, False, False)
                        for rule in literal.children]):
                    # U literal A/B
                    self.literal_labeling[literal] = StabilityLabel(True, False, False, False)
                elif any([self.rule_labeling[rule] == StabilityLabel(False, True, False, False) or
                          self.rule_labeling[rule] == StabilityLabel(False, False, True, False) or
                          self.rule_labeling[rule] == StabilityLabel(False, False, False, True)
                          for rule in literal.children]):
                    # O literal A
                    self.literal_labeling[literal] = StabilityLabel(False, False, True, False)
        else:
            if all([self.rule_labeling[rule] == StabilityLabel(True, False, False, False)
                    for rule in literal.children]):
                # U literal A/B
                self.literal_labeling[literal] = StabilityLabel(True, False, False, False)
            elif any([self.rule_labeling[rule] == StabilityLabel(False, True, False, False)
                      for rule in literal.children]) and \
                    all([self.rule_labeling[contrary_rule] == StabilityLabel(True, False, False, False) or
                         self.rule_labeling[contrary_rule] == StabilityLabel(False, False, True, False)
                         for contrary_literal in literal.contraries
                         for contrary_rule in contrary_literal.children]):
                # D literal B/C
                self.literal_labeling[literal] = StabilityLabel(False, True, False, False)
            elif any([self.rule_labeling[rule] == StabilityLabel(False, False, True, False)
                      for rule in literal.children]) and \
                    all([self.rule_labeling[rule] == StabilityLabel(True, False, False, False) or
                         self.rule_labeling[rule] == StabilityLabel(False, False, True, False)
                         for rule in literal.children]):
                # O literal B
                self.literal_labeling[literal] = StabilityLabel(False, False, True, False)
            elif any([self.rule_labeling[rule] == StabilityLabel(False, True, False, False) or
                      self.rule_labeling[rule] == StabilityLabel(False, False, False, True)
                      for rule in literal.children]) and \
                    any([self.rule_labeling[contrary_rule] == StabilityLabel(False, True, False, False) or
                         self.rule_labeling[contrary_rule] == StabilityLabel(False, False, False, True)
                         for contrary_literal in literal.contraries
                         for contrary_rule in contrary_literal.children]):
                # B literal A
                self.literal_labeling[literal] = StabilityLabel(False, False, False, True)
            elif any([self.rule_labeling[rule] == StabilityLabel(False, False, False, True)
                      for rule in literal.children]) and \
                    all([self.rule_labeling[rule] == StabilityLabel(True, False, False, False) or
                         self.rule_labeling[rule] == StabilityLabel(False, False, True, False) or
                         self.rule_labeling[rule] == StabilityLabel(False, False, False, True)
                         for rule in literal.children]):
                # B literal B
                self.literal_labeling[literal] = StabilityLabel(False, False, False, True)

    def color_rule(self, rule):
        """
        Color the Rule, that is: check, based on is antecedents, if this Rule can still become
        unsatisfiable/defended/out/blocked.
        """
        if any([self.literal_labeling[literal] == StabilityLabel(True, False, False, False)
                for literal in rule.antecedents]):
            # U rule
            self.rule_labeling[rule] = StabilityLabel(True, False, False, False)
        elif all([self.literal_labeling[literal] == StabilityLabel(False, True, False, False)
                  for literal in rule.antecedents]):
            # D rule
            self.rule_labeling[rule] = StabilityLabel(False, True, False, False)
        elif any([self.literal_labeling[literal] == StabilityLabel(False, False, True, False)
                  for literal in rule.antecedents]) and \
                all([self.literal_labeling[literal] == StabilityLabel(False, True, False, False) or
                     self.literal_labeling[literal] == StabilityLabel(False, False, True, False) or
                     self.literal_labeling[literal] == StabilityLabel(False, False, False, True)
                     for literal in rule.antecedents]):
            # O rule
            self.rule_labeling[rule] = StabilityLabel(False, False, True, False)
        elif any([self.literal_labeling[literal] == StabilityLabel(False, False, False, True)
                  for literal in rule.antecedents]) and \
                all([self.literal_labeling[literal] == StabilityLabel(False, True, False, False) or
                     self.literal_labeling[literal] == StabilityLabel(False, False, False, True)
                     for literal in rule.antecedents]):
            # B rule
            self.rule_labeling[rule] = StabilityLabel(False, False, False, True)
