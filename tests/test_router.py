"""Unit tests for multi-hop-retrieval-router."""
import unittest
from multi_hop_retrieval_router.router import MultiHopRouter


class TestMultiHopRouter(unittest.TestCase):
    def setUp(self):
        self.router = MultiHopRouter(max_hops=2)

    def test_multi_hop_execution(self):
        hops = self.router.execute_multi_hop_plan(
            "initial",
            lambda q: f"Evidence for {q}",
            lambda orig, h: "next_hop" if len(h) == 1 else None,
            lambda h: len(h) >= 2
        )
        self.assertEqual(len(hops), 2)
        self.assertEqual(hops[0].sub_query, "initial")
        self.assertEqual(hops[1].sub_query, "next_hop")
