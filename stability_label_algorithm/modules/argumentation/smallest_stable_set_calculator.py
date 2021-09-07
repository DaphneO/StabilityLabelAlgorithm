import itertools
from typing import List, Tuple, Callable, TypeVar
from .argumentation_theory.queryable import Queryable
from .argumentation_theory.literal import Literal
from .argumentation_theory.argumentation_system import ArgumentationSystem
from .argumentation_theory.argumentation_theory import ArgumentationTheory
from .labelers.stability_label import StabilityLabel
from .labelers.labeler_interface import LabelerInterface


T = TypeVar('T')


def join_step(item_sets: List[Tuple[T, ...]]) -> List[Tuple[T, ...]]:
    """
    Join k length item_sets into k + 1 length item_sets.

    This algorithm assumes that the list of item_sets are sorted, and that the item_sets themselves are sorted tuples.
    Instead of always enumerating all n^2 combinations, the algorithm only has n^2 runtime for each block of
    item_sets with the first k - 1 items equal.

    :param item_sets: A list of item sets of length k, to be joined to k + 1 length item sets
    :return: A list of k + 1 length item sets

    >>> # This is an example from the 1994 paper by Agrawal et al.
    >>> example_item_sets = [(1, 2, 3), (1, 2, 4), (1, 3, 4), (1, 3, 5), (2, 3, 4)]
    >>> join_step(example_item_sets)
    [(1, 2, 3, 4), (1, 3, 4, 5)]
    """
    result = []

    i = 0
    # Iterate over every item set in the item_sets
    while i < len(item_sets):

        # The number of rows to skip in the while-loop, initially set to 1
        skip = 1

        # Get all but the last item in the item set, and the last item
        *item_set_first, item_set_last = item_sets[i]

        # We now iterate over every item set following this one, stopping if the first k - 1 items are not equal.
        # If we're at (1, 2, 3), we'll consider (1, 2, 4) and (1, 2, 7), but not (1, 3, 1)

        # Keep a list of all last elements, i.e. tail elements, to perform 2-combinations on later on
        tail_items = [item_set_last]
        tail_items_append = tail_items.append  # Micro-optimization

        # Iterate over ever item set following this item set
        for j in range(i + 1, len(item_sets)):

            # Get all but the last item in the item set, and the last item
            *item_set_n_first, item_set_n_last = item_sets[j]

            # If it's the same, append and skip this item set in while-loop
            if item_set_first == item_set_n_first:

                # Micro-optimization
                tail_items_append(item_set_n_last)
                skip += 1

            # If it's not the same, break out of the for-loop
            else:
                break

        # For every 2-combination in the tail items, yield a new candidate item set, which is sorted.
        item_set_first_tuple = tuple(item_set_first)
        for a, b in sorted(itertools.combinations(tail_items, 2)):
            result.append(item_set_first_tuple + (a,) + (b,))

        # Increment the while-loop counter
        i += skip

    return result


def prune_step(item_sets: List[Tuple[T, ...]], possible_item_sets: List[Tuple[T, ...]]) -> List[Tuple[T, ...]]:
    """
    Prune possible item_sets whose subsets are not in the list of item_sets.

    :param item_sets: A list of item_sets of length k.
    :param possible_item_sets: A list of possible item_sets of length k + 1 to be pruned.
    :return: A pruned list of item_sets of length k + 1

    >>> example_item_sets = [('a', 'b', 'c'), ('a', 'b', 'd'),
    ...             ('b', 'c', 'd'), ('a', 'c', 'd')]
    >>> example_possible_item_sets = join_step(example_item_sets)
    >>> prune_step(example_item_sets, example_possible_item_sets)
    [('a', 'b', 'c', 'd')]
    """
    result = []

    # For faster lookups
    hash_codes = set(hash(item) for item in item_sets)

    # Go through every possible item set
    for possible_item_set in possible_item_sets:
        # Remove 1 from the combination, same as k-1 combinations. The item_sets created by removing the last two
        # items in the possible item_sets must be part of the item_sets by definition, due to the way the `join_step`
        # function merges the sorted item_sets

        for i in range(len(possible_item_set) - 2):
            removed = possible_item_set[:i] + possible_item_set[i + 1:]
            hash_code = hash(removed)

            # If every k combination exists in the set of item_sets, yield the possible item set. If it does not
            # exist, then its support cannot be large enough, since supp(A) >= supp(AB) for all B, and if supp(S) is
            # large enough, then supp(s) must be large enough for every s which is a subset of S.
            # This is the downward-closure property of the support function.
            # if removed not in item_sets:
            if hash_code not in hash_codes:
                break

        # If there is no break yet
        else:
            result.append(possible_item_set)

    return result


def apriori_gen(item_sets: List[Tuple[T, ...]]) -> List[Tuple[T, ...]]:
    """
    Generate a list of (k + 1) length candidate item_sets based on a SORTED list of k length item sets.

    :param item_sets: A list of item sets of length k, to be joined to k + 1 length candidate item sets
    :return: A list of (k + 1) length candidate item sets
    """
    possible_extensions = join_step(item_sets)
    return prune_step(item_sets, possible_extensions)


def join_and_prune_step(argumentation_system: ArgumentationSystem,
                        topics: List[Literal],
                        stability_labeler: LabelerInterface,
                        stability_function: Callable[[StabilityLabel], bool],
                        obs_set_k: Tuple[Queryable, ...], verbose=True) -> \
        Tuple[List[List[Queryable]], List[Tuple[Queryable]]]:
    smallest_stable_sets_k = []
    observable_set_k_unstable = []

    if all([not o1.is_contrary_of(o2) for (o1, o2) in itertools.combinations(obs_set_k, 2)]):
        # obs_set_k is consistent
        argumentation_theory = ArgumentationTheory(argumentation_system, list(obs_set_k))
        labels = stability_labeler.label(argumentation_theory)
        if all([stability_function(labels.literal_labeling[topic]) for topic in topics]):
            smallest_stable_sets_k.append(list(obs_set_k))
            if verbose:
                print([str(o) for o in obs_set_k])
                for literal_str, literal in argumentation_system.language.items():
                    if literal in topics and labels.literal_labeling[literal].defended:
                        print(literal_str)
        else:
            observable_set_k_unstable.append(obs_set_k)

    return smallest_stable_sets_k, observable_set_k_unstable


def smallest_stable_sets(argumentation_system: ArgumentationSystem,
                         topics: List[Literal],
                         stability_labeler: LabelerInterface,
                         stability_function: Callable[[StabilityLabel], bool] = lambda x: x.is_contested_stable,
                         verbose: bool = False) -> List[List[Queryable]]:
    """
    Finds all smallest sets of observations for which each topic is stable.

    :param argumentation_system: Argumentation theory for which we compute the smallest stable sets
    :param topics: Topics that need to be stable in order to form a smallest_stable_set
    :param stability_labeler: Stability labelling object (e.g. FourBoolStabilityLabeler)
    :param stability_function: Function that checks if a given label is stable
    :param verbose: Boolean indicating if intermediate results should be printed to the console
    :return: All smallest sets of observations for which each topic is stable
    """

    # First check edge case: are all topics table in case we have no observations at all?
    initial_labels = stability_labeler.label(ArgumentationTheory(argumentation_system, []))
    if all([stability_function(initial_labels.literal_labeling[topic]) for topic in topics]):
        return [[]]

    # We will iteratively fill the smallest_stable_sets list
    smallest_stable_set_list: List[List[Queryable]] = []

    # Generate all unstable observable sets of size 1 (int representation). NB: (obs,) is a 1-tuple in Python.
    observables = sorted([q for q in argumentation_system.queryables])
    observable_sets_k_min_1_candidates = [(obs,) for obs in observables]
    observable_sets_k_min_1_unstable = []
    for obs_set in observable_sets_k_min_1_candidates:
        argumentation_theory = ArgumentationTheory(argumentation_system, list(obs_set))
        labels = stability_labeler.label(argumentation_theory)
        if all([stability_function(labels.literal_labeling[topic]) for topic in topics]):
            smallest_stable_set_list.append(list(obs_set))
            if verbose:
                print([str(o) for o in obs_set])
                for literal_str, literal in argumentation_system.language.items():
                    if literal in topics and labels.literal_labeling[literal].defended:
                        print(literal_str)
        else:
            observable_sets_k_min_1_unstable.append(obs_set)

    # Given all unstable observable sets of size (k - 1), generate all unstable observable sets of size k.
    while observable_sets_k_min_1_unstable:
        observable_sets_k_candidates = apriori_gen(observable_sets_k_min_1_unstable)
        observable_sets_k_unstable = []

        res = [join_and_prune_step(argumentation_system, topics, stability_labeler, stability_function, c, verbose)
               for c in observable_sets_k_candidates]

        for stable, unstable in res:
            smallest_stable_set_list = smallest_stable_set_list + stable
            observable_sets_k_unstable = observable_sets_k_unstable + unstable

        observable_sets_k_min_1_unstable = observable_sets_k_unstable

    return smallest_stable_set_list
