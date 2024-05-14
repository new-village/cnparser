""" test_load_result.py
"""
import unittest
import copy
import cnparser

class TestEnricher(unittest.TestCase):
    """ Test Enrich
    """
    @classmethod
    def setUpClass(cls):
        # Load Test Data
        cndata = cnparser.read_csv_file("test/data/31_tottori_test_20240329.csv")
        cls.enriched = cnparser.enrich_kana(cndata)

    def test_case_1(self):
        """ testing success case parse
        """
        expect = {
            'sequence_number': '127',
            'corporate_number': '1280001002413',
            'process': '21',
            'correct': '0',
            'update_date': '2018-01-10',
            'change_date': '2018-01-05',
            'name': '島田商事株式会社',
            'name_image_id': '',
            'kind': '301',
            'prefecture_name': '島根県',
            'city_name': '安来市',
            'street_number': '安来町１５７８番地',
            'address_image_id': '',
            'prefecture_code': '32',
            'city_code': '206',
            'post_code': '6920011',
            'address_outside': '',
            'address_outside_image_id': '',
            'close_date': '2018-01-05',
            'close_cause': '01',
            'successor_corporate_number': '',
            'change_cause': '',
            'assignment_date': '2015-10-05',
            'latest': '1',
            'en_name': '',
            'en_prefecture_name': '',
            'en_city_name': '',
            'en_address_outside': '',
            'furigana': '',
            'hihyoji': '0',
            'e_furigana': 'シマダショウジ'
        }
        self.assertDictEqual(self.enriched[10], expect)

    def test_case_2(self):
        """ testing enrichment
        """
        expect = {
            'sequence_number': '537',
            'corporate_number': '1280001007263',
            'process': '01',
            'correct': '0',
            'update_date': '2016-07-27',
            'change_date': '2016-07-22',
            'name': '株式会社ｓｏｕｖｅｎｉｒ',
            'name_image_id': '',
            'kind': '301',
            'prefecture_name': '島根県',
            'city_name': '安来市',
            'street_number': '安来町１１９３番地',
            'address_image_id': '',
            'prefecture_code': '32',
            'city_code': '206',
            'post_code': '6920011',
            'address_outside': '',
            'address_outside_image_id': '',
            'close_date': '',
            'close_cause': '',
            'successor_corporate_number': '',
            'change_cause': '',
            'assignment_date': '2016-07-22',
            'latest': '1',
            'en_name': '',
            'en_prefecture_name': '',
            'en_city_name': '',
            'en_address_outside': '',
            'furigana': '',
            'hihyoji': '0',
            'e_furigana': 'スーベニアー'
        }
        self.assertDictEqual(self.enriched[11], expect)

if __name__ == '__main__':
    unittest.main()
