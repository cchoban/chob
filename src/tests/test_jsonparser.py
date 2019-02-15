import unittest, helpers, os
from core.JsonParser import Parser


class JsonParser(unittest.TestCase):
    def test_fileToJson(self):
        try:
            convert = helpers.programList()

            self.assertIsInstance(convert, dict)
        except Exception as e:
            raise Exception

    def test_isValid(self):
        try:
            convert = Parser(helpers.repo.repos()["localProgramlist"]).isValid()

            self.assertEqual(convert, True)
        except Exception as e:
            raise Exception

    def test_getKey(self):
        repos = Parser().getKey('installedApps',
                                helpers.repo.repos()["localInstalledApps"])
        self.assertIsInstance(repos, dict)

    def test_addNewPackage(self):
        add = Parser().addNewPackage('test', {})
        self.assertEqual(add, True)

    def test_removePackage(self):
        remove = Parser().removePackage('test')

        self.assertEqual(remove, True)

    def test_keyExists(self):
        self.assertEqual(Parser().keyExists({'selam': 'aleykumselam'}, 'selam'), True)

    def test_is_json(self):
        parser = Parser().is_json('{"selam": "aleykumselam"}')
        self.assertEqual(parser, True)

    def test_change_value(self):
        parser = Parser(os.path.join('tests', 'test.json'))
        dict = parser.fileToJson()
        isTrue = parser.change_value('selam', 'aslm')

        self.assertEqual(isTrue, True)

    def test_dump_json(self):
        parser = Parser().dump_json({'selam': 'aleykumselam'}, True)

        self.assertIsInstance(parser, str)
