import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from src.ui.login_window import LoginWindow
from src.storage.storage_manager import StorageManager

def test_login():
    app = QApplication(sys.argv)
    
    storage = StorageManager("test_data")
    window = LoginWindow(storage)
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    test_login()
