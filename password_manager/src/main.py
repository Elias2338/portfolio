'''main file of the Password Manager'''
from gui.gui import main_menu, Login_page
from core.derive_key import deriveKey
from core.encrypt_decrypt import KeySafe
from core.encrypt_decrypt import decrypt
import os

def check_password(password):
    key = deriveKey(salt, password)
    key = KeySafe(key)

    if os.path.exists(DB_PATH):
        with open(DB_PATH, "rb") as f:
            encrypted_list = f.read()

        try:
            decrypt(key.getKey(), encrypted_list)
            return True
        except:
            return False

    return True

salt = os.urandom(16)


if __name__ == "__main__":
    # Defining pathes
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.dirname(SCRIPT_DIR)

    SALT_PATH = os.path.join(BASE_DIR, "data", "salt.bin")
    DB_PATH = os.path.join(BASE_DIR, "data", "passwords.bin")


    # Check if new registry (no salt file) or log in (salt file exists)
    if not os.path.exists(SALT_PATH):
        # Create a random Salt and save in salt.bin
        with open(SALT_PATH, "wb") as f:
            f.write(os.urandom(16))

    # Load the Salt in
    with open(SALT_PATH, "rb") as f:
        salt = f.read()


    # Load Startpage and collect master password

    
    start = Login_page(check_password)
    start.login_page()

    master_password = start.password
    # Derive the key
    key = deriveKey(salt, master_password)
    key = KeySafe(key)

    # Load encrypted data
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "rb") as f:
            encrypted_list = f.read()

        try:
            password_list = decrypt(key.getKey(), encrypted_list)

        except Exception as e:
            print("Falsches Masterpasswort!")
            start.root.mainloop()


    else:
        password_list = []

    main_menu(password_list, key)