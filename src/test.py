import unittest, os
from tests import test_jsonparser, test_http, test_filemanager




if __name__ == '__main__':
    test_classes_to_run = [test_jsonparser.JsonParser, test_http.HttpTest, test_filemanager.FileManagerTest]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)


    # Cleanup test files&folders

    # for i in os.listdir(os.path.join('tests')):
    #     folders = ['testFolder']
    #     files = ['testFile.txt', 'test.json']
    #
    #     print(i)
    #     if i in files:
    #         os.remove(os.path.abspath(i))
    #     elif i in folders:
    #         os.removedirs(os.path.abspath(i))
