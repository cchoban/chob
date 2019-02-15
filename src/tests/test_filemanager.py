import unittest, helpers, os, tempfile
from core.FileManager import Manager

test_url = 'http://www.ovh.net/files/1Mb.dat'
fs = Manager()
class FileManagerTest(unittest.TestCase):

    def test_fileExists(self):
        parser = fs.fileExists(os.path.join('dat.exe'))

        self.assertEqual(parser, True)

    def test_createFolder(self):
        parser = fs.createFolder(os.path.join('tests', 'testFolder'))

        self.assertEqual(parser, True)

    def test_createFile(self):
        parser = fs.createFile(os.path.join('tests', 'testFile.txt'))

        self.assertEqual(parser, True)

    def test_deleteFile(self):
        parser = fs.deleteFile(os.path.join('tests', 'testFile.txt'))
        parser2 = fs.deleteFile(os.path.join('tests', 'testFolder'))
        self.assertEqual(parser, True)

    def test_createJsonfile(self):
        parser = fs.createJsonFile(os.path.join('tests'), {'testbreee': 'testbree'})

        self.assertEqual(parser, True)

    def test_removeDir(self):
        path = os.path.join('tests', 'testbea')
        createFolder = fs.createFolder(path)
        parser = fs.removeDir(path)

        self.assertEqual(parser, True)

    def test_moveFile(self):
        fs.createFile(os.path.join('tests', 'testbea'))
        fs.createFolder(os.path.join('tests', 'testbeaa'))
        parser = fs.moveFile(os.path.join('tests', 'testbea'), os.path.join('tests', 'testbeaa'))
        fs.removeDir(os.path.join('tests', 'testbeaa'))

        self.assertEqual(parser, True)


    def test_copyFile(self):
        fs.createFile(os.path.join('tests', 'testbea'))
        fs.createFolder(os.path.join('tests', 'testbeaa'))
        parser = fs.copyFile(os.path.join('tests', 'testbea'), os.path.join('tests', 'testbeaa'))
        fs.removeDir(os.path.join('tests', 'testbeaa'))

        self.assertEqual(parser, True)

    def test_renameFile(self):
        fs.createFile(os.path.join('tests', 'testbea'))
        parser = fs.renameFile(os.path.join('tests', 'testbea'), os.path.join('tests', 'testbea2'))

        self.assertEqual(parser, True)
        fs.deleteFile(os.path.join('tests', 'testbea2'))
