
import unittest
from webapp.modules.utilities import hash_password, check_password

class TestUtilities(unittest.TestCase):

    def test_password1(self):
        hsh = hash_password("password")
        self.assertTrue(
            check_password("password", hsh)
        )

    def test_password2(self):
        hsh = hash_password("password")
        self.assertFalse(
            check_password("drowssap", hsh)
        )

if __name__ == '__main__':
    unittest.main()
