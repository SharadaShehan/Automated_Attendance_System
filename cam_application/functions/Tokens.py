from cryptography.fernet import Fernet

def create_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("bin/key.bin", "wb") as key_file:
        key_file.write(key)

    return True

def load_key():
    """
    Loads the key from the current directory named `key.bin`
    """
    return open("bin/key.bin", "rb").read()

def save_init_token(init_token):
    """
    Given init token, encrypts it and returns the encrypted token
    """
    create_key()
    key = load_key()
    encoded_token = init_token.encode('utf-8')
    cipher_suite = Fernet(key)
    encrypted_token = cipher_suite.encrypt(encoded_token)
    with open("bin/init_token.bin", "wb") as token_file:
        token_file.write(encrypted_token)
    return True

def get_init_token():
    """
    Reads the encrypted init token and returns the decrypted token
    """
    key = load_key()
    cipher_suite = Fernet(key)
    with open("bin/init_token.bin", "rb") as token_file:
        encrypted_token = token_file.read()
    decrypted_token = cipher_suite.decrypt(encrypted_token)
    return decrypted_token.decode('utf-8')

def save_access_token(access_token):
    """
    Given access token, encrypts it and returns the encrypted token
    """
    key = load_key()
    encoded_token = access_token.encode('utf-8')
    cipher_suite = Fernet(key)
    encrypted_token = cipher_suite.encrypt(encoded_token)
    with open("bin/access_token.bin", "wb") as token_file:
        token_file.write(encrypted_token)
    return True

def get_access_token():
    """
    Reads the encrypted access token and returns the decrypted token
    """
    key = load_key()
    cipher_suite = Fernet(key)
    with open("bin/access_token.bin", "rb") as token_file:
        encrypted_token = token_file.read()
    decrypted_token = cipher_suite.decrypt(encrypted_token)
    return decrypted_token.decode('utf-8')
