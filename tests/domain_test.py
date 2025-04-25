import unittest

from providers_implementation.providers_impl import find_domain

REGEXP = r"com\/sector\/(?:modules|components)\/([^\/]+)"


class MyTestCase(unittest.TestCase):
    def test_find_domain_when_last_item(self):
        domain = find_domain(REGEXP, "com/sector/modules/domain/common/api")
        self.assertEqual("domain", domain)

    def test_find_domain(self):
        domain = find_domain(REGEXP, "com/sector/modules/domain")
        self.assertEqual("domain", domain)

    def test_find_domain_when_different_namespace(self):
        domain = find_domain(REGEXP, "com/sector/components/domain")
        self.assertEqual("domain", domain)

    def test_find_domain_without_domain(self):
        domain = find_domain(REGEXP, "com/sector/components")
        self.assertEqual("", domain)


if __name__ == '__main__':
    unittest.main()



