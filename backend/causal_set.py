# backend/causal_set.py

from typing import Dict, List


class CausalSet:
    """
    Minimal causal set structure:
    - events: list of event IDs (ints)
    - relations: event -> list of future events (a -> b means a precedes b)

    Provides:
    - add_event()
    - add_relation(a, b)
    - past_of(e)
    - future_of(e)
    - is_chain(subset)
    - is_antichain(subset)
    """

    def __init__(self) -> None:
        self.events: List[int] = []
        self.relations: Dict[int, List[int]] = {}

    def add_event(self) -> int:
        eid = len(self.events)
        self.events.append(eid)
        self.relations[eid] = []
        return eid

    def add_relation(self, a: int, b: int) -> None:
        """
        Add a causal arrow a -> b (a precedes b).
        """
        if a not in self.relations:
            self.relations[a] = []
        if b not in self.relations[a]:
            self.relations[a].append(b)

    def future_of(self, e: int) -> List[int]:
        return self.relations.get(e, [])

    def past_of(self, e: int) -> List[int]:
        return [x for x in self.events if e in self.relations.get(x, [])]

    def is_chain(self, subset: List[int]) -> bool:
        """
        A chain: every pair is comparable by the causal order.
        """
        for i in range(len(subset)):
            for j in range(i + 1, len(subset)):
                a, b = subset[i], subset[j]
                if not (
                    b in self.relations.get(a, [])
                    or a in self.relations.get(b, [])
                ):
                    return False
        return True

    def is_antichain(self, subset: List[int]) -> bool:
        """
        An antichain: no two elements are comparable.
        """
        for i in range(len(subset)):
            for j in range(i + 1, len(subset)):
                a, b = subset[i], subset[j]
                if (
                    b in self.relations.get(a, [])
                    or a in self.relations.get(b, [])
                ):
                    return False
        return True