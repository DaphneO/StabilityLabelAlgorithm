from typing import Optional, List

from stability_label_algorithm.modules.argumentation.argumentation_theory.argumentation_theory import ArgumentationTheory
from stability_label_algorithm.modules.argumentation.argumentation_theory.literal import Literal
from stability_label_algorithm.modules.dataset_generator.argumentation_system_property_computer.potential_argument import \
    PotentialArgument
from stability_label_algorithm.modules.dataset_generator.argumentation_theory_property_computer.argument import Argument
from stability_label_algorithm.modules.dataset_generator.argumentation_theory_property_computer.argumentation_framework import \
    ArgumentationFramework
from stability_label_algorithm.modules.dataset_generator.argumentation_theory_property_computer.\
    incomplete_argumentation_framework import IncompleteArgumentationFramework


class ArgumentationTheoryProperties:
    def __init__(self,
                 knowledge_base_size: int = 0,
                 argumentation_framework: Optional[ArgumentationFramework] = None,
                 incomplete_argumentation_framework: Optional[IncompleteArgumentationFramework] = None,
                 future_argumentation_theories: Optional[List[ArgumentationTheory]] = None):
        self.knowledge_base_size = knowledge_base_size
        if argumentation_framework is None:
            self.argumentation_framework = ArgumentationFramework.create_empty()
        else:
            self.argumentation_framework = argumentation_framework
        if incomplete_argumentation_framework is None:
            self.incomplete_argumentation_framework = IncompleteArgumentationFramework.create_empty()
        else:
            self.incomplete_argumentation_framework = incomplete_argumentation_framework
        if future_argumentation_theories is None:
            self.future_argumentation_theories = []
        else:
            self.future_argumentation_theories = future_argumentation_theories

    @property
    def all_arguments(self) -> List[Argument]:
        return self.argumentation_framework.arguments

    @property
    def all_potential_arguments(self) -> List[PotentialArgument]:
        return self.incomplete_argumentation_framework.potential_arguments

    @property
    def all_attacks(self):
        return self.argumentation_framework.attacks

    @property
    def all_p_attacks(self):
        return self.incomplete_argumentation_framework.p_attacks

    @property
    def nr_of_arguments(self) -> int:
        return len(self.all_arguments)

    @property
    def nr_of_potential_arguments(self) -> int:
        return len(self.all_potential_arguments)

    @property
    def nr_of_inconsistent_potential_arguments(self) -> int:
        return len([pot_arg for pot_arg in self.all_potential_arguments if not pot_arg.is_consistent])

    @property
    def nr_of_attacks(self) -> int:
        return len(self.all_attacks)

    @property
    def nr_of_p_attacks(self) -> int:
        return len(self.all_p_attacks)

    def get_arguments_for(self, literal: Literal):
        return self.argumentation_framework.arguments_by_literal[literal]

    def get_potential_arguments_for(self, literal: Literal):
        return self.incomplete_argumentation_framework.potential_arguments_by_literal[literal]
