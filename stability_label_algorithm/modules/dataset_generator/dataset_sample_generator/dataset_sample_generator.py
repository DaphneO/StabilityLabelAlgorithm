import random
from typing import List, Dict

from stability_label_algorithm.modules.argumentation.argumentation_theory.argumentation_system import ArgumentationSystem
from stability_label_algorithm.modules.argumentation.argumentation_theory.queryable import Queryable


def generate_consistent_knowledge_base(argumentation_system: ArgumentationSystem, knowledge_base_size: int) -> \
        List[Queryable]:
    knowledge_base = []
    extra_knowledge_required = knowledge_base_size
    while extra_knowledge_required > 0:
        knowledge_base_candidates = [q for q in argumentation_system.queryables
                                     if all([not k.is_contrary_of(q) and k != q for k in knowledge_base])]
        if not knowledge_base_candidates:
            raise ValueError(f'Could not make knowledge base of size {str(knowledge_base)} for argumentation system.')
        new_knowledge_base_item = random.choice(knowledge_base_candidates)
        knowledge_base.append(new_knowledge_base_item)
        extra_knowledge_required -= 1

    return knowledge_base


def generate_dataset_sample(argumentation_system: ArgumentationSystem,
                            nr_of_ats_per_knowledge_base_size: Dict[int, int],
                            verbose: bool = False) -> List[List[Queryable]]:
    knowledge_bases = []
    for nr_of_k, nr_of_ats in nr_of_ats_per_knowledge_base_size.items():
        for at_i in range(nr_of_ats):
            knowledge_base = generate_consistent_knowledge_base(argumentation_system, nr_of_k)
            knowledge_bases.append(knowledge_base)
            if verbose:
                print(str(knowledge_base))
    return knowledge_bases
