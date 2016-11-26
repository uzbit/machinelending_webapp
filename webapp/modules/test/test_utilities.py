
import unittest
from webapp.modules.utilities import encrypt_data, decrypt_data

class TestUtilities(unittest.TestCase):

	def _test_encrypt_decrypt(self):
		data = 'datadata'
		salt = 'salt'
		encrypted = encrypt_data(data, salt)
		decrypted = decrypt_data(encrypted, salt)
		self.assertEqual(data, decrypted)

	def test_encrypt_decrypt_length(self):
		data = ('datadata'*100)[:100]
		salt = 'salt'
		for i in range(1, 10):
			salt = salt*i
			print "before", len(salt)
			#print type(data[:100])
			encrypted = encrypt_data(data, salt)
			print "after", len(encrypted)
			#print type(encrypted[:100])
			#print len(encrypted)
			#print decrypt_data(encrypted, salt)

if __name__ == '__main__':
	unittest.main()
