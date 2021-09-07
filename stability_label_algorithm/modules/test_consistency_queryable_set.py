from typing import List, Union

from stability_label_algorithm.modules.argumentation.argumentation_theory.literal import Literal
from stability_label_algorithm.modules.argumentation.argumentation_theory.queryable import Queryable


def queryable_set_is_consistent(queryable_list: List[Union[Literal, Queryable]]) -> bool:
    for i1 in range(len(queryable_list)):
        for i2 in range(i1 + 1, len(queryable_list)):
            if queryable_list[i1].is_contrary_of(queryable_list[i2]):
                return False
    return True
