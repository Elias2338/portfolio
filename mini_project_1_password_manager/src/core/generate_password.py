import string
import secrets

def generate_password():
    length = 16
    characters = string.digits + string.ascii_letters + string.punctuation
    password = ""

    for i in range(length):
        password += secrets.choice(characters)

    return password