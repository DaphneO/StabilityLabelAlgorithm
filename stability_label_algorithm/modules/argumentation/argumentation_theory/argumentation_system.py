from typing import Dict, List, Optional

from .literal import Literal
from .queryable import Queryable
from .rule import Rule


class ArgumentationSystem:
    """
    An ArgumentationSystem is a language of Literals (some of which are Queryable and/or a topic) and a list of Rules.
    """

    def __init__(self, language: Dict[str, Literal], rules: List[Rule],
                 topic_literals: Optional[List[Literal]] = None):
        self.language = language
        self.rules = rules

        if topic_literals is None:
            self.topic_literals = []
        else:
            self.topic_literals = topic_literals

    def __eq__(self, other):
        return self.language == other.language and self.rules == other.rules

    def update_literal_name(self, old_literal_name: str, new_literal_name: str) -> None:
        """
        Change the name of a Literal in this ArgumentationSystem. Make sure that all connections are still correct.

        :param old_literal_name: The old name of the Literal.
        :param new_literal_name: The new name of the Literal.
        """
        if old_literal_name not in self.language.keys():
            raise ValueError(old_literal_name + ' was not a literal.')
        if new_literal_name in self.language.keys():
            raise ValueError(new_literal_name + ' already exists. You cannot overwrite an existing literal.')
        if '~' in new_literal_name:
            raise ValueError('A new literal literal name cannot contain the \'~\' character.')

        old_literal = self.language[old_literal_name]
        old_literal_negation = old_literal.negation
        old_literal_negation_name = str(old_literal_negation)

        old_literal.update_literal_name(new_literal_name)
        old_literal_negation.update_literal_name('~' + new_literal_name)

        del self.language[old_literal_name]
        del self.language[old_literal_negation_name]
        self.language[str(old_literal)] = old_literal
        self.language[str(old_literal.negation)] = old_literal.negation

    def update_literal_information(self, literal_name: str, new_literal_nl_true_value: str,
                                   new_literal_nl_unknown_value: str, new_literal_nl_false_value: str) -> None:
        """
        Update the information of a Literal in the ArgumentationSystem.

        :param literal_name: Name of the Literal that should be changed.
        :param new_literal_nl_true_value: New text in natural language stating that the Literal is present (defended).
        :param new_literal_nl_unknown_value: New text in natural language stating that the Literal is unknown.
        :param new_literal_nl_false_value: New text in natural language stating that the Literal is absent.
        """
        if literal_name not in self.language.keys():
            raise ValueError(literal_name + ' was not a literal in the language.')
        literal = self.language[literal_name]
        literal.update_literal_information(new_literal_nl_true_value, new_literal_nl_unknown_value,
                                           new_literal_nl_false_value)

    def get_queryable(self, queryable_str: str) -> Queryable:
        """
        Obtain a specific Queryable from the ArgumentationSystem.

        :param queryable_str: Name of the Queryable.
        :return: The Queryable searched for.
        """
        if queryable_str not in self.language.keys():
            raise IndexError(f'{queryable_str} was not in the language.')
        requested_literal = self.language[queryable_str]
        if not isinstance(requested_literal, Queryable):
            raise IndexError(f'{queryable_str} is not a Queryable but a Literal.')
        return requested_literal

    def get_queryables(self, queryable_str_list: List[str]) -> List[Queryable]:
        """
        Obtain a specific list of Queryables from the ArgumentationSystem.

        :param queryable_str_list: Names of the Queryables.
        :return: The Queryables searched for.
        """
        return [self.get_queryable(obs_str) for obs_str in queryable_str_list]

    @property
    def queryables(self) -> List[Queryable]:
        """
        All Queryables in the ArgumentationSystem's language.

        :return: All Queryables.
        """
        return [literal for literal in self.language.values() if isinstance(literal, Queryable)]

    @property
    def positive_queryables(self) -> List[Queryable]:
        """
        All positive, that is, non-negated Queryables in the ArgumentationSystem's language.

        :return: All positive Queryables.
        """
        return [queryable for queryable in self.queryables if not queryable.negated]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
