'''Deriving the key using PBKDF2'''

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

#Derive key funktion
def deriveKey(salt:bytes, master_password:str):
    #Create PBKDF2 Object
    pbkdf2 = PBKDF2HMAC(hashes.SHA256(), int(256/8), salt, 600000)

    #Derive the key and return
    return pbkdf2.derive(master_password.encode())