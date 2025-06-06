import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.crypto.crypto_manager import CryptoManager

def test_crypto():
    crypto = CryptoManager()
    password = "minha_senha_mestre"
    data = "senha_secreta_123"
    
    # Gerar chave
    key = crypto.generate_key_from_password(password)
    print(f"Chave gerada: {len(key)} bytes")
    
    # Criptografar
    encrypted = crypto.encrypt_data(data)
    print(f"Dados criptografados: {len(encrypted)} bytes")
    
    # Descriptografar
    decrypted = crypto.decrypt_data(encrypted)
    print(f"Dados descriptografados: {decrypted}")
    
    assert data == decrypted
    print("✓ Criptografia funcionando")

if __name__ == "__main__":
    test_crypto()
