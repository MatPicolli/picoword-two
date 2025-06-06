from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class CryptoManager:
    def __init__(self):
        self.salt = None
        self.key = None
    
    def generate_key_from_password(self, password: str, salt: bytes = None) -> bytes:
        """Gera chave de criptografia a partir da senha mestre"""
        if salt is None:
            salt = os.urandom(16)
        
        self.salt = salt
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.key = key
        return key
    
    def encrypt_data(self, data: str) -> bytes:
        """Criptografa dados"""
        if not self.key:
            raise ValueError("Chave não foi gerada")
        
        fernet = Fernet(self.key)
        return fernet.encrypt(data.encode())
    
    def decrypt_data(self, encrypted_data: bytes) -> str:
        """Descriptografa dados"""
        if not self.key:
            raise ValueError("Chave não foi gerada")
        
        fernet = Fernet(self.key)
        return fernet.decrypt(encrypted_data).decode()
