""" test_enrich.py
"""
import pandas as pd
import unittest
from cnparser.enrich import enrich, enrich_kana, enrich_kind, enrich_post_code
from cnparser.load import read_csv

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

    def test_enrich_kind(self):
        """Test the enrich_kind function to ensure it correctly maps 'kind' to 'std_legal_entity'."""
        result = enrich_kind(self.df.copy())
        self.assertIn('std_legal_entity', result.columns)
        expected_entities = ['National Agency', 'K.K.', 'K.K.', 'K.K.', 'Y.K.']
        for i, entity in enumerate(expected_entities):
            self.assertEqual(result.iloc[i]['std_legal_entity'], entity)

    def test_enrich_postcode(self):
        """Test the enrich_kind function to ensure it correctly maps 'kind' to 'std_legal_entity'."""
        result = enrich_post_code(self.df.copy())
        self.assertIn('std_post_code', result.columns)
        expected_entities = ['680-0011', None, '692-0011', '699-0101', '693-0005']
        for i, entity in enumerate(expected_entities):
            self.assertEqual(result.iloc[i]['std_post_code'], entity)

    def test_enrich_all_processes(self):
        """Test the enrich function with all processes to ensure it processes correctly."""
        result = enrich(self.df.copy())
        self.assertIn('std_furigana', result.columns)
        self.assertIn('std_legal_entity', result.columns)
        self.assertIn('std_post_code', result.columns)

    def test_enrich_with_invalid_process(self):
        """Test the enrich function with an invalid process name to ensure it returns the original DataFrame unchanged and raises a warning."""
        with self.assertWarns(Warning) as warning:
            result = enrich(self.df.copy(), 'enrich_error')
            self.assertEqual(str(warning.warnings[0].message), "No valid function name enrich_error. Skip enrich_error processing.")

if __name__ == '__main__':
    unittest.main()
