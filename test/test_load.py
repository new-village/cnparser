""" test_load_result.py
"""
import unittest
import copy
import cnparser

class TestLoader(unittest.TestCase):
    """ Test Loader
    """
    @classmethod
    def setUpClass(cls):
        # Load Staygload who has overseas race history and abort race history
        cls.success_case = cnparser.bulk_load("Shimane")
        # Enrich success_case
        enriched = copy.deepcopy(cls.success_case)
        cls.enriched = cnparser.bulk_enrich(enriched[:200])

    def test_success_case_count(self):
        """ testing success case counts
        """
        self.assertGreater(len(self.success_case), 10000)

    def test_success_case_parse(self):
        """ testing success case parse
        """
        expect = {
            'sequence_number': '1',
            'corporate_number': '1000013050246',
            'process': '01',
            'correct': '1',
            'update_date': '2018-04-02',
            'change_date': '2015-10-05',
            'name': '川本簡易裁判所',
            'name_image_id': None,
            'kind': '101',
            'prefecture_name': '島根県',
            'city_name': '邑智郡川本町',
            'street_number': '大字川本３４０',
            'address_image_id': None,
            'prefecture_code': '32',
            'city_code': '441',
            'post_code': '6960001',
            'address_outside': None,
            'address_outside_image_id': None,
            'close_date': None,
            'close_cause': None,
            'successor_corporate_number': None,
            'change_cause': None,
            'assignment_date': '2015-10-05',
            'latest': '1',
            'en_name': 'Kawamoto Summary Court',
            'en_prefecture_name': 'Shimane',
            'en_city_name': '340, Oaza Kawamoto, Kawamoto machi, Ochi gun',
            'en_address_outside': None,
            'furigana': 'カワモトカンイサイバンショ',
            'hihyoji': '0'
        }
        self.assertDictEqual(self.success_case[0], expect)

    def test_enrichment(self):
        """ testing enrichment
        """
        expect = {
            'sequence_number': '1',
            'corporate_number': '1000013050246',
            'process': '01',
            'correct': '1',
            'update_date': '2018-04-02',
            'change_date': '2015-10-05',
            'name': '川本簡易裁判所',
            'name_image_id': None,
            'kind': '101',
            'prefecture_name': '島根県',
            'city_name': '邑智郡川本町',
            'street_number': '大字川本３４０',
            'address_image_id': None,
            'prefecture_code': '32',
            'city_code': '441',
            'post_code': '6960001',
            'address_outside': None,
            'address_outside_image_id': None,
            'close_date': None,
            'close_cause': None,
            'successor_corporate_number': None,
            'change_cause': None,
            'assignment_date': '2015-10-05',
            'latest': '1',
            'en_name': 'Kawamoto Summary Court',
            'en_prefecture_name': 'Shimane',
            'en_city_name': '340, Oaza Kawamoto, Kawamoto machi, Ochi gun',
            'en_address_outside': None,
            'furigana': 'カワモトカンイサイバンショ',
            'hihyoji': '0',
            'pref': '島根県', 
            'city': '邑智郡川本町', 
            'town': '大字川本', 
            'addr': '340', 
            'lat': 34.978982, 
            'lng': 132.525163, 
            'level': 3
        }
        self.assertDictEqual(self.enriched[0], expect)

    def test_bulk_enrich_count(self):
        """Load CSV into bulk_enrich and test if there are 1000 records
        """
        result = cnparser.bulk_enrich("test/data/31_tottori_test_20240329.csv")
        self.assertEqual(len(result), 10)

if __name__ == '__main__':
    unittest.main()
