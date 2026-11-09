"""Core Multi-Hop Retrieval Router implementation."""
from typing import Dict, List, Optional, Tuple, Any, Callable


class HopStep:
    def __init__(self, hop_index: int, sub_query: str, retrieved_evidence: str, extracted_entities: List[str]):
        self.hop_index = hop_index
        self.sub_query = sub_query
        self.retrieved_evidence = retrieved_evidence
        self.extracted_entities = extracted_entities


class MultiHopRouter:
    def __init__(self, max_hops: int = 3):
        self.max_hops = max_hops

    def execute_multi_hop_plan(
        self,
        initial_query: str,
        retrieval_fn: Callable[[str], str],
        decompose_fn: Callable[[str, List[HopStep]], Optional[str]],
        is_sufficient_fn: Callable[[List[HopStep]], bool]
    ) -> List[HopStep]:
        hops: List[HopStep] = []
        current_query = initial_query

        for hop_idx in range(1, self.max_hops + 1):
            evidence = retrieval_fn(current_query)
            # Dummy entity extract (first capitalized words or keywords)
            entities = [w for w in evidence.split() if w.istitle()]
            step = HopStep(hop_idx, current_query, evidence, entities[:3])
            hops.append(step)

            if is_sufficient_fn(hops):
                break

            next_q = decompose_fn(initial_query, hops)
            if not next_q or next_q == current_query:
                break
            current_query = next_q

        return hops
