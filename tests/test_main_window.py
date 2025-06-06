import sys
import os
import uuid
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.storage.storage_manager import StorageManager
from src.models.password_model import PasswordDatabase, PasswordEntry

def test_main_window():
    app = QApplication(sys.argv)
    
    # Criar dados de teste
    storage = StorageManager("test_data")
    master_password = "teste123"
    
    # Criar database com dados de exemplo
    db = PasswordDatabase()
    db.entries.append(PasswordEntry(
        id=str(uuid.uuid4()),
        title="Gmail",
        username="teste@gmail.com",
        password="senha123",
        url="https://gmail.com"
    ))
    db.entries.append(PasswordEntry(
        id=str(uuid.uuid4()),
        title="Facebook",
        username="meuuser",
        password="minhasenha",
        url="https://facebook.com"
    ))
    
    storage.save_database(db, master_password)
    
    window = MainWindow(storage, master_password)
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    test_main_window()
