import bcrypt

def hasPass(pwd):
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(pwd, salt)
    return hashed