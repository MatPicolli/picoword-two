import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.storage.storage_manager import StorageManager
from src.models.password_model import PasswordDatabase, PasswordEntry
import uuid
import shutil

def test_storage():
    # Limpar dados de teste
    if os.path.exists("test_data"):
        shutil.rmtree("test_data")
    
    storage = StorageManager("test_data")
    master_password = "senha_mestre_123"
    
    # Criar database de teste
    db = PasswordDatabase()
    entry = PasswordEntry(
        id=str(uuid.uuid4()),
        title="Teste",
        username="user@test.com",
        password="senha123"
    )
    db.entries.append(entry)
    
    # Salvar
    success = storage.save_database(db, master_password)
    print(f"Salvou: {success}")
    assert success
    
    # Carregar
    loaded_db = storage.load_database(master_password)
    print(f"Carregou: {loaded_db is not None}")
    assert loaded_db is not None
    assert len(loaded_db.entries) == 1
    assert loaded_db.entries[0].title == "Teste"
    
    # Testar senha errada
    wrong_db = storage.load_database("senha_errada")
    print(f"Senha errada: {wrong_db is None}")
    assert wrong_db is None
    
    print("✓ Storage funcionando")
    
    # Limpar
    shutil.rmtree("test_data")

if __name__ == "__main__":
    test_storage()
