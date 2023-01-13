""" test_load_result.py
"""
import unittest
import cnparser

class TestLoader(unittest.TestCase):
    """ Test Loader
    """
    @classmethod
    def test_success_case_count(cls):
        """ testing success case counts
        """
        loader = cnparser.bulk_load()
        print(loader.data[0])
        cls.assertTrue(loader.data[0], "ALL")

if __name__ == '__main__':
    unittest.main()