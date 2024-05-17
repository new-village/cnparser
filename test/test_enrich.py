""" test_enrich.py
"""
import unittest
import pandas as pd
from cnparser.load import read_csv
from cnparser.enrich import enrich, enrich_kana

class TestEnrich(unittest.TestCase):
    def setUp(self):
        """Set up the test environment by loading test data from a CSV file."""
        self.df = read_csv('./test/data/31_tottori_test_20240329.csv')

    def test_enrich_kana(self):
        """Test the enrich_kana function to ensure it correctly adds the 'std_furigana' column."""
        result = enrich_kana(self.df.copy())
        self.assertIn('std_furigana', result.columns)
        expected_furigana = ['トットリカンイサイバンショ', 'シマダショウジ', 'souvenir', 'T&Mコンサルティング', 'HAPカンコウ']
        for i, furigana in enumerate(expected_furigana):
            self.assertEqual(result.iloc[i]['std_furigana'], furigana)

    def test_enrich_all_processes(self):
        """Test the enrich function with all processes to ensure it processes correctly."""
        result = enrich(self.df.copy())
        self.assertIn('std_furigana', result.columns)

    def test_enrich_with_invalid_process(self):
        """Test the enrich function with an invalid process name to ensure it returns the original DataFrame unchanged and raises a warning."""
        with self.assertWarns(Warning) as warning:
            result = enrich(self.df.copy(), 'enrich_error')
            self.assertEqual(str(warning.warnings[0].message), "No valid processing functions specified in ('enrich_error',). Returning the original DataFrame unchanged.")
        pd.testing.assert_frame_equal(self.df, result)

if __name__ == '__main__':
    unittest.main()
