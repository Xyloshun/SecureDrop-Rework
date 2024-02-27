import crypt
import os
salt = crypt.mksalt(crypt.METHOD_SHA512)

def hash_passwd (_password):
    hashed_password = crypt.crypt(_password, salt)
    return hashed_password
