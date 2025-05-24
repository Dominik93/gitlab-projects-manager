import unittest

from search import search, SearchConfiguration, regexp_predicate, text_predicate


class SearchTestCase(unittest.TestCase):

    def test_search_and_show_line(self):
        configuration = SearchConfiguration(text_predicate("text to search"), show_content=True)
        actual = search(['./resources/component', './resources/module'], configuration)
        expected = [{"identifier": './resources/component/test_java.java', "content": 'java component text to search'},
                    {"identifier": './resources/component/test_txt.txt', "content": 'txt component text to search'},
                    {"identifier": './resources/module/test_java.java', "content": 'java module text to search'}]
        self.assertEqual(expected, actual)

    def test_search_all_files(self):
        configuration = SearchConfiguration(text_predicate("text to search"))
        actual = search(['./resources/component', './resources/module'], configuration)
        expected = [{"identifier": './resources/component/test_java.java', "content": None},
                    {"identifier": './resources/component/test_txt.txt', "content": None},
                    {"identifier": './resources/module/test_java.java', "content": None}]
        self.assertEqual(expected, actual)

    def test_search_regexp(self):
        configuration = SearchConfiguration(regexp_predicate(".*to.*"))
        actual = search(['./resources/component', './resources/module'], configuration)
        expected = [{"identifier": './resources/component/test_java.java', "content": None},
                    {"identifier": './resources/component/test_txt.txt', "content": None},
                    {"identifier": './resources/module/test_java.java', "content": None}]
        self.assertEqual(expected, actual)

    def test_search_only_java(self):
        configuration = SearchConfiguration(text_predicate("text to search"), text_predicate(".java"))
        actual = search(['./resources/component', './resources/module'], configuration)
        expected = [{"identifier": './resources/component/test_java.java', "content": None},
                    {"identifier": './resources/module/test_java.java', "content": None}]
        self.assertEqual(expected, actual)

    def test_not_found_text(self):
        configuration = SearchConfiguration(text_predicate("not found"))
        actual = search(['./resources/component', './resources/module'], configuration)
        expected = []
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
