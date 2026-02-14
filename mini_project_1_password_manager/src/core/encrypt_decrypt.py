import json
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
from core.password_entries import Passwords
from cryptography.exceptions import InvalidTag

#Class to store the key
class KeySafe():
    def __init__(self, key):
        self.key = key

    def getKey(self):
        return self.key
    

def encrypt(keySafe, password_list):
    FILE_PATH = os.path.abspath(__file__)
    CORE_DIR = os.path.dirname(FILE_PATH) 
    SRC_DIR = os.path.dirname(CORE_DIR)  
    BASE_DIR = os.path.dirname(SRC_DIR) 

    DATA_DIR = os.path.join(BASE_DIR, "data")
    DB_PATH = os.path.join(DATA_DIR, "passwords.bin")

    #Convert to a json suitable format
    list = []
    for i in range(len(password_list)):
        list.append(password_list[i].toDict())

    #Save in a json String
    unencrypted_list = json.dumps(list).encode('utf-8')

    #Encrypt
    nonce = os.urandom(12)
    AES = AESGCM(keySafe.getKey())
    encrypted_list = AES.encrypt(nonce, unencrypted_list, None)

    #Save the data
    with open(DB_PATH, "wb") as f:
        f.write(nonce + encrypted_list)

def decrypt(key, encrypted_list):
    #Split it back into Nonce + Data
    nonce = encrypted_list[:12]
    encrypted_list = encrypted_list[12:]

    if len(nonce) < 12:
        return []
    #Decrypt it
    AES = AESGCM(key)

    try:
        unencrypted_list = json.loads(AES.decrypt(nonce, encrypted_list, None).decode())

        #Reformat
        password_list = []
        for i in range(len(unencrypted_list)):
            service = unencrypted_list[i]["service"]
            username = unencrypted_list[i]["username"]
            password = unencrypted_list[i]["password"]
            password_list.append(Passwords(service, username, password))

        return password_list
    
    except InvalidTag:
        return []
    
    except Exception as e:
        # Für alle anderen unvorhergesehenen Fehler
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
        return []
