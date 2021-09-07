from ..argumentation_theory.argumentation_theory import ArgumentationTheory
from .labels import Labels


class LabelerInterface:
    """
    Interface for labelers. Actual Labeler-objects inherit from this class. They should all have a label method.
    """

    def label(self, argumentation_theory: ArgumentationTheory) -> Labels:
        """
        Assign Labels to each Literal and Rule in the ArgumentationTheory.

        :param argumentation_theory: ArgumentationTheory that should be labelled.
        :return: Labels for the ArgumentationTheory.
        """
        pass
