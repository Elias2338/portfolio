from core.encrypt_decrypt import encrypt

def save_data(password_list, keySafe):
    encrypt(keySafe, password_list)
    