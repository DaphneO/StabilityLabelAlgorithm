from functools import total_ordering


@total_ordering
class Literal:
    """
    A literal has an absolute literal string (abs_literal_str) and two description strings (present or not).
    Furthermore, a literal can be observable and/or a topic, indicated by boolean class variables.
    Also, a literal has a list of contraries.
    """

    def __init__(self, literal_str: str, description_if_present: str, description_if_not_present: str,
                 is_observable: bool):
        self.s1 = literal_str
        self.s1_hash = hash(self.s1)

        if literal_str[0] == '~':
            self.negated = True
            literal_str = literal_str[1:]
        else:
            self.negated = False

        self.abs_literal_str = literal_str
        self.description_if_present = description_if_present
        self.description_if_not_present = description_if_not_present

        self.is_observable = is_observable

        self.contraries = []
        self.negation = None
        self.parents = []
        self.children = []

        self.position = None

    def __str__(self):
        return self.s1

    def __eq__(self, other):
        return self.s1_hash == other.s1_hash

    def __lt__(self, other):
        return str(self) < str(other)

    def is_contrary_of(self, other) -> bool:
        """
        Boolean indicating if this Literal is a contrary of some other Literal.

        :param other: Some other Literal that might be contrary.
        """
        return other in self.contraries

    def __hash__(self):
        return self.s1_hash

    def update_literal_name(self, new_name: str) -> None:
        """
        Update the name of this Literal.

        :param new_name: Change the name of the Literal (and make sure that some naming requirements are met).
        """
        if self.negated:
            if not new_name.startswith('~'):
                raise ValueError('This literal is negated and should therefore start with \'~\'.')
            if '~' in new_name[1:]:
                raise ValueError('The \'~\' is only allowed as first character.')
            self.s1 = new_name
            self.abs_literal_str = new_name[1:]
        else:
            if '~' in new_name:
                raise ValueError('Literal names are not allowed to contain \'~\'.')
            self.s1 = new_name
            self.abs_literal_str = new_name

    def update_literal_information(self, new_literal_nl_true_value: str, new_literal_nl_unknown_value: str,
                                   new_literal_nl_false_value: str) -> None:
        """
        Update the natural language texts corresponding to this Literal.

        :param new_literal_nl_true_value: New text in natural language stating that the Literal is present (defended).
        :param new_literal_nl_unknown_value: New text in natural language stating that the Literal is unknown.
        :param new_literal_nl_false_value: New text in natural language stating that the Literal is absent.
        """
        self.description_if_not_present = new_literal_nl_unknown_value
        self.negation.description_if_not_present = new_literal_nl_unknown_value
        if not self.negated:
            self.description_if_present = new_literal_nl_true_value
            self.negation.description_if_present = new_literal_nl_false_value
        else:
            self.description_if_present = new_literal_nl_false_value
            self.description_if_not_present = new_literal_nl_true_value
