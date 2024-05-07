import unittest
from stream import Stream
from collectors import (
    ToListCollector,
    GroupingByCollector,
    CountingCollector,
    MaxByCollector,
)


class Test(unittest.TestCase):
    def setUp(self) -> None:
        self.stream1 = Stream(
            [
                {"student": "A", "score": 100, "class": "A"},
                {"student": "A", "score": 99, "class": "B"},
                {"student": "B", "score": 80, "class": "A"},
                {"student": "B", "score": 79, "class": "B"},
                {"student": "C", "score": 60, "class": "A"},
                {"student": "C", "score": 69, "class": "B"},
            ]
        )
        return super().setUp()

    def test_map(self):
        self.assertEqual(
            self.stream1.map(lambda x: x["score"]).collect(ToListCollector()),
            [100, 99, 80, 79, 60, 69],
        )

    # def test_filter(self):
    #     self.assertEqual(
    #         self.stream1.filter(lambda x: x["score"] > 80)
    #         .map(lambda x: x["student"])
    #         .collect(ToSetCollector()),
    #         {"A"},
    #     )

    def test_sum(self):
        self.assertEqual(
            self.stream1.filter(lambda x: x["score"] > 80).map(lambda x: x["score"]).sum(),
            199,
        )

    def test_groupby(self):
        mapping = self.stream1.collect(
            GroupingByCollector(lambda x: x["class"], GroupingByCollector(lambda x: x["student"]))
        )
        print("test groupby:", mapping)
        self.assertEqual(["A", "B"], list(mapping.keys()))
        self.assertEqual(["A", "B", "C"], list(mapping["A"].keys()))

    def test_counting_collector(self):
        assert self.stream1.collect(CountingCollector()) == 6

        count_mapping = self.stream1.collect(GroupingByCollector(lambda x: x["class"], CountingCollector()))
        print("Count mapping:", count_mapping)
        assert count_mapping == {"A": 3, "B": 3}


if __name__ == "__main__":
    unittest.main()
