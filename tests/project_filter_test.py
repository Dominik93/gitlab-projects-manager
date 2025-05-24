import unittest

from project_filter import exclude_projects, include_projects


class ProjectFilterTestCase(unittest.TestCase):

    def test_include_project(self):
        projects = include_projects([
            {'archived': False, 'name': 'com-module'},
            {'archived': True, 'name': 'com-archived'}
        ], {"name": ["com-module"]})

        self.assertEqual(projects, [{'archived': False, 'name': 'com-module'}])

    def test_exclude_project(self):
        projects = exclude_projects([
            {'archived': False, 'name': 'com-module'},
            {'archived': True, 'name': 'com-archived'}
        ], {"archived": ["True"]})

        self.assertEqual(projects, [{'archived': False, 'name': 'com-module'}])


if __name__ == '__main__':
    unittest.main()
