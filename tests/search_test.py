import unittest

from search import search, SearchConfiguration


class SearchTestCase(unittest.TestCase):

    def test_search_and_show_line(self):
        configuration = SearchConfiguration(text="text to search", show_content=True)
        actual = search(['./resources/component', './resources/module'], configuration)
        expected = [{"file": './resources/component/test_java.java', "content": 'java component text to search'},
                    {"file": './resources/component/test_txt.txt', "content": 'txt component text to search'},
                    {"file": './resources/module/test_java.java', "content": 'java module text to search'}]
        self.assertEqual(expected, actual)

    def test_search_all_files(self):
        configuration = SearchConfiguration(text="text to search")
        actual = search(['./resources/component', './resources/module'], configuration)
        expected = [{"file": './resources/component/test_java.java', "content": None},
                    {"file": './resources/component/test_txt.txt', "content": None},
                    {"file": './resources/module/test_java.java', "content": None}]
        self.assertEqual(expected, actual)

    def test_search_regexp(self):
        configuration = SearchConfiguration(regexp=".*to.*")
        actual = search(['./resources/component', './resources/module'], configuration)
        expected = [{"file": './resources/component/test_java.java', "content": None},
                    {"file": './resources/component/test_txt.txt', "content": None},
                    {"file": './resources/module/test_java.java', "content": None}]
        self.assertEqual(expected, actual)

    def test_search_only_java(self):
        configuration = SearchConfiguration(text="text to search", file_extension='.java')
        actual = search(['./resources/component', './resources/module'], configuration)
        expected = [{"file": './resources/component/test_java.java', "content": None},
                    {"file": './resources/module/test_java.java', "content": None}]
        self.assertEqual(expected, actual)

    def test_not_found_text(self):
        configuration = SearchConfiguration(text="not found")
        actual = search(['./resources/component', './resources/module'], configuration)
        expected = []
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
