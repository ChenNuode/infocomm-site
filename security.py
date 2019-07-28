
import bcrypt
import string
import random

def generatehash(password):
	salt = bcrypt.gensalt()
	return bcrypt.hashpw(password.encode(), salt)

def checkpwd(password,hashlol):
	return bcrypt.checkpw(password.encode(),hashlol)


def linkgen(size=24, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
	return ''.join(random.choice(chars) for _ in range(size))
