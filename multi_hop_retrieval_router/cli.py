"""CLI for multi-hop-retrieval-router."""
import sys
import argparse
from .router import MultiHopRouter, HopStep


def dummy_retrieval(query: str) -> str:
    if "company" in query.lower():
        return "Adobe announced intention to acquire Figma."
    elif "ceo" in query.lower():
        return "Shantanu Narayen serves as CEO of Adobe."
    return "No records found."


def dummy_decompose(original: str, history: list) -> str:
    if len(history) == 1:
        return "Who is the CEO of Adobe?"
    return ""


def main():
    parser = argparse.ArgumentParser(description="Multi-Hop Retrieval Router CLI")
    parser.add_argument("--demo", action="store_true", help="Run multi-hop retrieval demo")
    args = parser.parse_args()

    if args.demo:
        router = MultiHopRouter(max_hops=3)
        hops = router.execute_multi_hop_plan(
            "Who is the CEO of the company acquiring Figma?",
            retrieval_fn=dummy_retrieval,
            decompose_fn=dummy_decompose,
            is_sufficient_fn=lambda h: len(h) >= 2
        )
        print(f"Multi-Hop Execution Finished in {len(hops)} hops:")
        for h in hops:
            print(f"  [Hop {h.hop_index}] Query: {h.sub_query}")
            print(f"    Evidence: {h.retrieved_evidence}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
