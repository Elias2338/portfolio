import unittest
import os
import sys
import json
import tempfile
import shutil

# Füge den 'src' Ordner zum Pfad hinzu, damit wir die Module finden
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from core.password_entries import Passwords
from core.derive_key import deriveKey
from core.encrypt_decrypt import KeySafe, encrypt, decrypt

class TestPasswordManagerCore(unittest.TestCase):

    def setUp(self):
        """Wird vor jedem Test ausgeführt: Erstellt eine Test-Umgebung."""
        self.test_dir = tempfile.mkdtemp()
        # Wir müssen den Pfad in encrypt_decrypt kurz "umbiegen" für Tests
        # Da wir das nicht einfach können, nutzen wir Mock-Daten
        self.sample_passwords = [
            Passwords("Amazon", "elias", "geheim123"),
            Passwords("Google", "user@gmail.com", "passwort456")
        ]
        self.master_pw = "master123"
        self.salt = os.urandom(16)
        self.key = deriveKey(self.salt, self.master_pw)

    def tearDown(self):
        """Wird nach jedem Test ausgeführt: Räumt auf."""
        shutil.rmtree(self.test_dir)

    # --- Tests für Password Entries ---
    def test_password_to_dict(self):
        """Prüft, ob die Konvertierung in ein Dictionary funktioniert."""
        entry = Passwords("Test", "User", "Pass")
        d = entry.toDict()
        self.assertEqual(d["service"], "Test")
        self.assertEqual(d["username"], "User")
        self.assertEqual(d["password"], "Pass")

    # --- Tests für Key Derivation ---
    def test_key_derivation_consistency(self):
        """Prüft, ob gleiches PW + gleicher Salt den gleichen Key ergibt."""
        key1 = deriveKey(self.salt, self.master_pw)
        key2 = deriveKey(self.salt, self.master_pw)
        self.assertEqual(key1, key2)

    def test_key_derivation_uniqueness(self):
        """Prüft, ob unterschiedliche PWs unterschiedliche Keys ergeben."""
        key1 = deriveKey(self.salt, "passwort1")
        key2 = deriveKey(self.salt, "passwort2")
        self.assertNotEqual(key1, key2)

    # --- Tests für KeySafe ---
    def test_keysafe_storage(self):
        """Prüft, ob der KeySafe den Key korrekt speichert und zurückgibt."""
        safe = KeySafe(self.key)
        self.assertEqual(safe.getKey(), self.key)

    # --- Integration Test: Encryption/Decryption ---
    def test_encryption_roundtrip(self):
        """Der wichtigste Test: Liste -> Encrypt -> Decrypt -> Gleiche Liste."""
        # 1. Wir nutzen eine temporäre Datei für den Test
        test_file = os.path.join(self.test_dir, "test_vault.bin")
        
        # Da wir die Pfade in deiner encrypt_decrypt fest verdrahtet haben,
        # testen wir hier die Logik der Verschlüsselung manuell:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        
        # Simuliere ENCRYPT
        dict_list = [p.toDict() for p in self.sample_passwords]
        unencrypted_bytes = json.dumps(dict_list).encode('utf-8')
        nonce = os.urandom(12)
        aes = AESGCM(self.key)
        ciphertext = aes.encrypt(nonce, unencrypted_bytes, None)
        full_data = nonce + ciphertext
        
        # Simuliere DECRYPT
        decrypted_list = decrypt(self.key, full_data)
        
        # Check
        self.assertEqual(len(decrypted_list), 2)
        self.assertEqual(decrypted_list[0].service, "Amazon")
        self.assertEqual(decrypted_list[1].username, "user@gmail.com")

    def test_decryption_failure(self):
        """Prüft, ob die Entschlüsselung bei falschem Key scheitert."""
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        
        # 1. Korrekt verschlüsseln
        dict_list = [p.toDict() for p in self.sample_passwords]
        unencrypted_bytes = json.dumps(dict_list).encode('utf-8')
        nonce = os.urandom(12)
        aes = AESGCM(self.key)
        ciphertext = aes.encrypt(nonce, unencrypted_bytes, None)
        full_data = nonce + ciphertext
        
        # 2. Mit FALSCHEM Key entschlüsseln
        wrong_key = os.urandom(32)
        
        # Deine decrypt-Funktion sollte hier eine leere Liste liefern oder None
        result = decrypt(wrong_key, full_data)
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()