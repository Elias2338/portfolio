'''main file of the Password Manager'''
from cli.cli import main_menu, startpage
from core.derive_key import deriveKey
from core.encrypt_decrypt import KeySafe
from core.encrypt_decrypt import decrypt
import os

salt = os.urandom(16)


if __name__ == "__main__":
    # Findet den absoluten Pfad zur main.py
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    # Geht einen Ordner hoch zum Projekt-Hauptverzeichnis
    BASE_DIR = os.path.dirname(SCRIPT_DIR)

    # Jetzt definieren wir die Pfade absolut basierend auf dem Hauptverzeichnis
    SALT_PATH = os.path.join(BASE_DIR, "data", "salt.bin")
    DB_PATH = os.path.join(BASE_DIR, "data", "passwords.bin")


    #Check if new registry (no salt file) or log in (salt file exists)
    if not os.path.exists(SALT_PATH):
        #Create a random Salt and save in salt.bin
        with open(SALT_PATH, "wb") as f:
            f.write(os.urandom(16))

    #Load the Salt in
    with open(SALT_PATH, "rb") as f:
        salt = f.read()

    #Load Startpage and collect master password
    master_password = startpage()

    #Derive the key
    key = deriveKey(salt, master_password)
    key = KeySafe(key)

    #Load encrypted data
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "rb") as f:
            encrypted_list = f.read()

        password_list = decrypt(key.getKey(), encrypted_list)
    else:
        password_list = []

    main_menu(password_list, key)
