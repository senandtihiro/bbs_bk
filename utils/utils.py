import hashlib
import random


def generate_salt():
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars=[]
    for i in range(16):
        chars.append(random.choice(ALPHABET))
    return ''.join(chars)

def get_md5(s):
    md5 = hashlib.md5(s.encode('utf-8'))
    # hashlib.md5(str(random.getrandbits(256)).encode('utf-8')).hexdigest()
    # md5.
    return md5.hexdigest()

def encript_password(password, salt):
    return get_md5(password + str(salt))