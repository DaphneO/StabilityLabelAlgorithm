from stability_label_algorithm.modules.argumentation.argumentation_theory.argumentation_theory import ArgumentationTheory
from stability_label_algorithm.modules.argumentation.labelers.labels import Labels


class ArgumentationTheoryLatticeItem:
    def __init__(self, argumentation_theory: ArgumentationTheory, acceptability_labels: Labels):
        self.argumentation_theory = argumentation_theory
        self.acceptability_labels = acceptability_labels

        self.direct_future_theories = []
        self.direct_previous_theories = []
        self.stability_labels = \
            Labels({literal: acceptability_labels.literal_labeling[literal].__copy__()
                    for literal in acceptability_labels.literal_labeling.keys()}, {})

    def connect(self, other: 'ArgumentationTheoryLatticeItem'):
        if abs(len(self.argumentation_theory.knowledge_base) - len(other.argumentation_theory.knowledge_base)) == 1:
            if len(self.argumentation_theory.knowledge_base) > len(other.argumentation_theory.knowledge_base):
                longest, shortest = self, other
            else:
                longest, shortest = other, self
            if all([q in longest.argumentation_theory.knowledge_base
                    for q in shortest.argumentation_theory.knowledge_base]):
                shortest._add_direct_future_theory(longest)

    def _add_direct_future_theory(self, direct_future_theory: 'ArgumentationTheoryLatticeItem'):
        self.direct_future_theories.append(direct_future_theory)
        direct_future_theory.direct_previous_theories.append(self)

    def _add_direct_previous_theory(self, direct_previous_theory: 'ArgumentationTheoryLatticeItem'):
        self.direct_previous_theories.append(direct_previous_theory)
        direct_previous_theory.direct_future_theories.append(self)

    @property
    def is_largest(self):
        return self.direct_future_theories == []

    def update_possible_future_acceptability_statuses(self):
        for direct_future_theory in self.direct_future_theories:
            # Update literals
            for literal in self.argumentation_theory.argumentation_system.language.values():
                self.stability_labels.literal_labeling[literal] += \
                    direct_future_theory.stability_labels.literal_labeling[literal]

            # # Update rules
            # for rule in self.argumentation_theory.argumentation_system.rules:
            #     self.possible_future_acceptability_statuses.rule_labeling[rule] += \
            #         direct_future_theory.possible_future_acceptability_statuses.rule_labeling[rule]