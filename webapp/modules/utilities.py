
import sys
from simplecrypt import encrypt, decrypt

def print_log(out, verbose=True):
    if verbose:
        sys.stdout.write(str(out)+'\n')
    sys.stdout.flush()

def encrypt_data(data, salt):
	encoded = data.encode('utf-8')
	return encrypt(salt, data)

def decrypt_data(data, salt):
	return decrypt(salt, data)
