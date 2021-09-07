from distutils.util import strtobool

from parse import parse


class StabilityLabel:
    """
    A StabilityLabel consists of four booleans, corresponding to the statuses unsatisfiable, defended, out and blocked.
    """
    def __init__(self, unsatisfiable: bool, defended: bool, out: bool, blocked: bool):
        self.unsatisfiable = unsatisfiable
        self.defended = defended
        self.out = out
        self.blocked = blocked

    def __str__(self):
        s1 = '(U:{0}, D:{1}, O:{2}, B:{3})'.format(str(self.unsatisfiable), str(self.defended), str(self.out),
                                                   str(self.blocked))
        return s1

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.unsatisfiable == other.unsatisfiable and self.defended == other.defended and \
               self.out == other.out and self.blocked == other.blocked

    def __copy__(self):
        return StabilityLabel(self.unsatisfiable, self.defended, self.out, self.blocked)

    def __add__(self, other: 'StabilityLabel'):
        unsatisfiable = self.unsatisfiable or other.unsatisfiable
        defended = self.defended or other.defended
        out = self.out or other.out
        blocked = self.blocked or other.blocked
        return StabilityLabel(unsatisfiable, defended, out, blocked)

    @property
    def is_stable(self) -> bool:
        """
        Is the StabilityLabel stable? This is the case if only one of the booleans is True.

        :return: Boolean indicating if the StabilityLabel is stable.

        >>> StabilityLabel(True, False, False, False).is_stable
        True
        >>> StabilityLabel(True, True, False, False).is_stable
        False
        """
        return sum([self.unsatisfiable, self.defended, self.out, self.blocked]) == 1

    @property
    def is_contested_stable(self):
        """
        Is the StabilityLabel contested-stable? This is the case if either the StabilityLabel is stable-defended or
        if the defended-boolean is False.

        :return: Boolean indicating if the StabilityLabel is contested-stable.

        >>> StabilityLabel(False, True, False, False).is_contested_stable
        True
        >>> StabilityLabel(True, True, False, False).is_contested_stable
        False
        >>> StabilityLabel(True, False, True, False).is_contested_stable
        True
        """
        if self.defended and (self.unsatisfiable or self.out or self.blocked):
            return False
        return True

    @classmethod
    def from_str(cls, label_str: str):
        """
        Read the label from a string.

        :param label_str: String containing the information on the StabilityLabel.
        :return: StabilityLabel read from the string.
        """
        parse_result_str_list = parse('(U:{0}, D:{1}, O:{2}, B:{3})', label_str).fixed
        parse_result_bool_list = [strtobool(s) for s in parse_result_str_list]
        return StabilityLabel(*parse_result_bool_list)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
