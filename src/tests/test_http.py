import unittest, helpers, os
from core.http import Http

test_url = 'http://www.ovh.net/files/1Mb.dat'
class HttpTest(unittest.TestCase):
    def test_download(self):
        parser = Http().download(test_url, 'dat')

        self.assertEqual(parser, True)

    def test_get(self):
        parser = Http().get(test_url)

        self.assertIsNotNone(parser)

    def test_post(self):
        parser = Http().post(test_url)

        self.assertIsNotNone(parser)

    def test_json(self):
        url = helpers.repo.repos()['programList']
        parser = Http().get(url).json()

        self.assertIsInstance(parser, dict)
