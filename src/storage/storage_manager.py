import os
import json
from typing import Optional
from src.crypto.crypto_manager import CryptoManager
from src.models.password_model import PasswordDatabase, PasswordEntry

class StorageManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.db_file = os.path.join(data_dir, "passwords.encrypted")
        self.salt_file = os.path.join(data_dir, "salt.bin")
        self.crypto = CryptoManager()
        
        # Criar diretório se não existir
        os.makedirs(data_dir, exist_ok=True)
    
    def save_database(self, database: PasswordDatabase, master_password: str) -> bool:
        """Salva database criptografado"""
        try:
            # Gerar/carregar salt
            salt = self._get_or_create_salt()
            
            # Gerar chave da senha mestre
            self.crypto.generate_key_from_password(master_password, salt)
            
            # Serializar e criptografar
            json_data = database.to_json()
            encrypted_data = self.crypto.encrypt_data(json_data)
            
            # Salvar arquivo
            with open(self.db_file, 'wb') as f:
                f.write(encrypted_data)
            
            return True
        except Exception as e:
            print(f"Erro ao salvar: {e}")
            return False
    
    def load_database(self, master_password: str) -> Optional[PasswordDatabase]:
        """Carrega database descriptografado"""
        try:
            # Verificar se arquivos existem
            if not os.path.exists(self.db_file) or not os.path.exists(self.salt_file):
                return PasswordDatabase()  # Database vazio
            
            # Carregar salt
            salt = self._load_salt()
            if not salt:
                return None
            
            # Gerar chave da senha mestre
            self.crypto.generate_key_from_password(master_password, salt)
            
            # Carregar e descriptografar
            with open(self.db_file, 'rb') as f:
                encrypted_data = f.read()
            
            json_data = self.crypto.decrypt_data(encrypted_data)
            database = PasswordDatabase.from_json(json_data)
            
            return database
        except Exception as e:
            print(f"Erro ao carregar: {e}")
            return None
    
    def _get_or_create_salt(self) -> bytes:
        """Obtém salt existente ou cria novo"""
        if os.path.exists(self.salt_file):
            return self._load_salt()
        else:
            return self._create_salt()
    
    def _create_salt(self) -> bytes:
        """Cria novo salt"""
        salt = os.urandom(16)
        with open(self.salt_file, 'wb') as f:
            f.write(salt)
        return salt
    
    def _load_salt(self) -> Optional[bytes]:
        """Carrega salt existente"""
        try:
            with open(self.salt_file, 'rb') as f:
                return f.read()
        except Exception:
            return None
    
    def database_exists(self) -> bool:
        """Verifica se já existe database"""
        return os.path.exists(self.db_file) and os.path.exists(self.salt_file)
