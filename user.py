import hashlib, re

# Regex code from https://www.geeksforgeeks.org/password-validation-in-python/

def validate_new_pass(passw):

	reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    
	pat = re.compile(reg)

	if not re.search(pat, passw):
		return False

	return True


def hash_pass(passw):
	m = hashlib.sha256()

	m.update(passw.encode('utf-8'))

	return m.hexdigest()
