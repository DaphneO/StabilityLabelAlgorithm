from typing import List

from ...argumentation.argumentation_theory.argumentation_theory import ArgumentationTheory
from ...argumentation.smallest_stable_set_calculator import apriori_gen
from .argumentation_framework import ArgumentationFramework
from .argumentation_theory_properties import ArgumentationTheoryProperties
from .incomplete_argumentation_framework import IncompleteArgumentationFramework
import stability_label_algorithm.modules.test_consistency_queryable_set


def compute_argumentation_theory_properties(argumentation_theory: ArgumentationTheory, verbose=False) -> \
        ArgumentationTheoryProperties:
    """
    Compute some properties of the given ArgumentationTheory, such as the corresponding incomplete argumentation
    framework or the number of future ArgumentationTheories.

    :param argumentation_theory: ArgumentationTheory for which properties are needed.
    :param verbose: Boolean indicating if information should be printed.
    :return: ArgumentationTheoryProperties of the ArgumentationTheory.
    """
    properties = ArgumentationTheoryProperties()
    properties.knowledge_base_size = len(argumentation_theory.knowledge_base)
    properties.argumentation_framework = ArgumentationFramework.from_argumentation_theory(argumentation_theory)
    properties.incomplete_argumentation_framework = \
        IncompleteArgumentationFramework.from_argumentation_theory(argumentation_theory)
    properties.future_argumentation_theories = enumerate_future_argumentation_theories(argumentation_theory, verbose)

    return properties


def enumerate_future_argumentation_theories(argumentation_theory: ArgumentationTheory,
                                            verbose: bool = False) -> List[ArgumentationTheory]:
    """
    Enumerate all future ArgumentationTheories of this ArgumentationTheory.

    :param argumentation_theory: ArgumentationTheory for which future ArgumentationTheories should be enumerated.
    :param verbose: Boolean indicating if information should be printed.
    :return: All future ArgumentationTheories of this ArgumentationTheory.
    """
    argumentation_system = argumentation_theory.argumentation_system
    original_knowledge_base = argumentation_theory.knowledge_base
    future_argumentation_theories = [argumentation_theory]
    candidates = sorted(argumentation_theory.future_knowledge_base_candidates)
    k_min_1_candidates = [(obs,) for obs in candidates]

    for obs_set in k_min_1_candidates:
        future_argumentation_theory = ArgumentationTheory(argumentation_system, original_knowledge_base + list(obs_set))
        future_argumentation_theories.append(future_argumentation_theory)

    while k_min_1_candidates:
        observable_sets_k_candidates = apriori_gen(k_min_1_candidates)
        k_min_1_candidates = []
        for observable_sets_k_candidate in observable_sets_k_candidates:
            new_knowledge_base = original_knowledge_base + list(observable_sets_k_candidate)
            if stability_label_algorithm.modules.test_consistency_queryable_set.queryable_set_is_consistent(
                    new_knowledge_base):
                future_argumentation_theories.append(ArgumentationTheory(argumentation_system, new_knowledge_base))
                if verbose:
                    print(str(new_knowledge_base))
                k_min_1_candidates.append(observable_sets_k_candidate)
    return future_argumentation_theories
