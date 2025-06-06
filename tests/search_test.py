import unittest

from commons.countable_processor import ExceptionStrategy
from search import search, SearchConfiguration, regexp_predicate, text_predicate


class SearchTestCase(unittest.TestCase):

    def test_search_and_show_line(self):
        configuration = SearchConfiguration(text_predicate("text to search"), show_content=True)
        actual = search([
            {"namespace": './resources', "name": "component"},
            {"namespace": './resources', "name": "module"}
        ],
            "./", configuration)
        expected = [
            {"location": "component", "identifier": 'test_java.java', "content": 'java component text to search'},
            {"location": "component", "identifier": 'test_kotlin.kt', "content": 'kotlin component text to search'},
            {"location": "component", "identifier": 'test_txt.txt', "content": 'txt component text to search'},
            {"location": "module", "identifier": 'test_java.java', "content": 'java module text to search'}]
        self.assertEqual(expected, actual)

    def test_search_all_files(self):
        configuration = SearchConfiguration(text_predicate("text to search"))
        actual = search([
            {"namespace": './resources', "name": "component"},
            {"namespace": './resources', "name": "module"}
        ], "./", configuration)
        expected = [
            {"location": "component", "identifier": 'test_java.java', "content": None},
            {"location": "component", "identifier": 'test_kotlin.kt', "content": None},
            {"location": "component", "identifier": 'test_txt.txt', "content": None},
            {"location": "module", "identifier": 'test_java.java', "content": None}]
        self.assertEqual(expected, actual)

    def test_search_regexp(self):
        configuration = SearchConfiguration(regexp_predicate(".*to.*"))
        actual = search([
            {"namespace": './resources', "name": "component"},
            {"namespace": './resources', "name": "module"}
        ], "./", configuration)
        expected = [
            {"location": "component", "identifier": 'test_java.java', "content": None},
            {"location": "component", "identifier": 'test_kotlin.kt', "content": None},
            {"location": "component", "identifier": 'test_txt.txt', "content": None},
            {"location": "module", "identifier": 'test_java.java', "content": None}]
        self.assertEqual(expected, actual)

    def test_search_only_java(self):
        configuration = SearchConfiguration(text_predicate("text to search"), text_predicate(".java"))
        actual = search([
            {"namespace": './resources', "name": "component"},
            {"namespace": './resources', "name": "module"}
        ], "./", configuration)
        expected =   [
                {"location": "component", "identifier": 'test_java.java', "content": None},
                {"location": "module", "identifier": 'test_java.java', "content": None}]
        self.assertEqual(expected, actual)

    def test_search_multiple_file_predicate(self):
        configuration = SearchConfiguration(text_predicate("text to search"), text_predicate([".java", ".kt"]))
        actual = search([
            {"namespace": './resources', "name": "component"},
            {"namespace": './resources', "name": "module"}
        ], "./", configuration)
        expected = [
            {"location": "component", "identifier": 'test_java.java', "content": None},
            {"location": "component", "identifier": 'test_kotlin.kt', "content": None},
            {"location": "module", "identifier": 'test_java.java', "content": None}]
        self.assertEqual(expected, actual)

    def test_not_found_text(self):
        configuration = SearchConfiguration(text_predicate("not found"))
        actual = search([
            {"namespace": './resources', "name": "component"},
            {"namespace": './resources', "name": "module"}
        ], "./", configuration)
        expected = []
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
