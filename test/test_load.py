""" test_load_result.py
"""
import unittest
import cnparser

class TestLoader(unittest.TestCase):
    """ Test Loader
    """
    @classmethod
    def setUpClass(cls):
        # Load Staygload who has overseas race history and abort race history
        cls.success_case = cnparser.bulk_load("Shimane")

    def test_success_case_count(self):
        """ testing success case counts
        """
        self.assertGreater(len(self.success_case.show), 10000)

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
            'name_image_id': '',
            'kind': '101',
            'prefecture_name': '島根県',
            'city_name': '邑智郡川本町',
            'street_number': '大字川本３４０',
            'address_image_id': '',
            'prefecture_code': '32',
            'city_code': '441',
            'post_code': '6960001',
            'address_outside': '',
            'address_outside_image_id': '',
            'close_date': '',
            'close_cause': '',
            'successor_corporate_number': '',
            'change_cause': '',
            'assignment_date': '2015-10-05',
            'latest': '1',
            'en_name': 'Kawamoto Summary Court',
            'en_prefecture_name': 'Shimane',
            'en_city_name': '340, Oaza Kawamoto, Kawamoto machi, Ochi gun',
            'en_address_outside': '',
            'furigana': 'カワモトカンイサイバンショ',
            'hihyoji': '0'
        }
        self.assertDictEqual(self.success_case.show[0], expect)

if __name__ == '__main__':
    unittest.main()
