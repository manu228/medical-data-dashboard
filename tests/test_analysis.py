import unittest
from analysis import get_data, summary, grouped_feature_stats

class TestAnalysis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = get_data()

    def test_dataset_shape_and_counts(self):
        self.assertEqual(self.data.shape, (569, 32))
        self.assertEqual(summary(self.data)["benign"], 357)
        self.assertEqual(summary(self.data)["malignant"], 212)
        self.assertEqual(len(set(self.data.sample_id)), 569)

    def test_no_missing_values(self):
        self.assertEqual(int(self.data.isna().sum().sum()), 0)

    def test_group_stats(self):
        g = grouped_feature_stats(self.data,"mean radius")
        self.assertEqual(g["count"].sum(),569)

if __name__ == "__main__":
    unittest.main()
