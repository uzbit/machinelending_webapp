
import unittest
from webapp.modules.utilities import encrypt_data, decrypt_data

class TestUtilities(unittest.TestCase):

	def test_encrypt_decrypt(self):
		data = 'datadata'
		salt = 'salt'
		encrypted = encrypt_data(data, salt)
		decrypted = decrypt_data(encrypted, salt)
		self.assertEqual(data, decrypted)

	def _test_encrypt_decrypt_length(self):
		data = 'datadata'
		salt = 'salt'
		for i in range(1, 10):
			data = data*i
			print "before", len(data)
			print type(data[:100])
			encrypted = encrypt_data(data, salt)
			print "after", len(encrypted)
			print type(encrypted[:100])
			#print len(encrypted)
			#print decrypt_data(encrypted, salt)

if __name__ == '__main__':
	unittest.main()
