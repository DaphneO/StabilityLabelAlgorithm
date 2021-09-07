from typing import List

from .argumentation_system import ArgumentationSystem
from .queryable import Queryable


class ArgumentationTheory:
    """
    An ArgumentationTheory consists of an ArgumentationSystem and a knowledge base (which is a list of Queryables).
    Arguments can be inferred on the basis of an ArgumentationTheory.
    """

    def __init__(self, argumentation_system: ArgumentationSystem, observations: List[Queryable]):
        self.argumentation_system = argumentation_system
        self.knowledge_base = observations

    @property
    def future_knowledge_base_candidates(self) -> List[Queryable]:
        """
        Obtain all Queryables that could be in the knowledge base of some future ArgumentationTheory.

        :return: List of queryables that could be in the knowledge base of some future ArgumentationTheory.
        """
        return [queryable for queryable in self.argumentation_system.queryables
                if queryable not in self.knowledge_base and
                all([contrary not in self.knowledge_base for contrary in queryable.contraries])]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
