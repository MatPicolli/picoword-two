import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.password_model import PasswordEntry, PasswordDatabase
import uuid

def test_model():
    # Criar entrada
    entry = PasswordEntry(
        id=str(uuid.uuid4()),
        title="Gmail",
        username="meu@email.com",
        password="senha123",
        url="https://gmail.com"
    )
    
    print(f"Entrada criada: {entry.title}")
    print(f"ID: {entry.id}")
    print(f"Criado em: {entry.created_at}")
    
    # Testar serialização
    entry_dict = entry.to_dict()
    entry_restored = PasswordEntry.from_dict(entry_dict)
    
    assert entry.title == entry_restored.title
    print("✓ Serialização funcionando")
    
    # Testar database
    db = PasswordDatabase()
    db.entries.append(entry)
    
    json_str = db.to_json()
    db_restored = PasswordDatabase.from_json(json_str)
    
    assert len(db_restored.entries) == 1
    assert db_restored.entries[0].title == "Gmail"
    print("✓ Database funcionando")

if __name__ == "__main__":
    test_model()
