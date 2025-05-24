import unittest

from search import search, SearchConfiguration, Predicate


class SearchTestCase(unittest.TestCase):

    def test_search_and_show_line(self):
        configuration = SearchConfiguration(Predicate("text to search", None), show_content=True)
        actual = search(['./resources/component', './resources/module'], configuration)
        expected = [{"identifier": './resources/component/test_java.java', "content": 'java component text to search'},
                    {"identifier": './resources/component/test_txt.txt', "content": 'txt component text to search'},
                    {"identifier": './resources/module/test_java.java', "content": 'java module text to search'}]
        self.assertEqual(expected, actual)

    def test_search_all_files(self):
        configuration = SearchConfiguration(Predicate("text to search", None))
        actual = search(['./resources/component', './resources/module'], configuration)
        expected = [{"identifier": './resources/component/test_java.java', "content": None},
                    {"identifier": './resources/component/test_txt.txt', "content": None},
                    {"identifier": './resources/module/test_java.java', "content": None}]
        self.assertEqual(expected, actual)

    def test_search_regexp(self):
        configuration = SearchConfiguration(Predicate(None, ".*to.*"))
        actual = search(['./resources/component', './resources/module'], configuration)
        expected = [{"identifier": './resources/component/test_java.java', "content": None},
                    {"identifier": './resources/component/test_txt.txt', "content": None},
                    {"identifier": './resources/module/test_java.java', "content": None}]
        self.assertEqual(expected, actual)

    def test_search_only_java(self):
        configuration = SearchConfiguration(Predicate("text to search", None), Predicate(".java", None))
        actual = search(['./resources/component', './resources/module'], configuration)
        expected = [{"identifier": './resources/component/test_java.java', "content": None},
                    {"identifier": './resources/module/test_java.java', "content": None}]
        self.assertEqual(expected, actual)

    def test_not_found_text(self):
        configuration = SearchConfiguration(Predicate("not found", None))
        actual = search(['./resources/component', './resources/module'], configuration)
        expected = []
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
