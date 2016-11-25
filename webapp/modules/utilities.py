
import sys
import random
import hashlib

def print_log(out, verbose=True):
    if verbose:
        sys.stdout.write(str(out))
    sys.stdout.flush()


def get_hexdigest(str1, str2):
    return hashlib.sha1('%s%s' % (str1, str2)).hexdigest()

def hash_password(raw_password):
    salt = get_hexdigest(str(random.random()), str(random.random()))[:5]
    hsh = get_hexdigest(salt, raw_password)
    return '%s$%s' % (salt, hsh)

def check_password(raw_password, enc_password):
    salt, hsh = enc_password.split('$')
    return hsh == get_hexdigest(salt, raw_password)
'''
def auth_user(username, password):
	user = User.query.filter_by(username=username).first()
	print user
	print check_password(password, user.password)
	return check_password(password, user.password)
'''
