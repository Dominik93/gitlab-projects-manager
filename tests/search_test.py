import unittest

from search import search


class SearchTestCase(unittest.TestCase):
    def test_search_all_files(self):
        actual = search("./resources", ['component', 'module'], "text to search")
        expected = ['./resources/component/test_java.java', './resources/component/test_txt.txt',
                    './resources/module/test_java.java']
        self.assertEqual(expected, actual)

    def test_search_regexp(self):
        actual = search("./resources", ['component', 'module'], ".*to.*")
        expected = ['./resources/component/test_java.java', './resources/component/test_txt.txt',
                    './resources/module/test_java.java']
        self.assertEqual(expected, actual)

    def test_search_only_java(self):
        actual = search("./resources", ['component', 'module'], "text to search", '.java')
        expected = ['./resources/component/test_java.java', './resources/module/test_java.java']
        self.assertEqual(expected, actual)

    def test_not_found_text(self):
        actual = search("./resources", ['component', 'module'], "not found")
        expected = []
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
