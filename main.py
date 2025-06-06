import sys
import os
from PySide6.QtWidgets import QApplication

# Adicionar src ao path para imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.storage.storage_manager import StorageManager
from src.ui.login_window import LoginWindow
from src.ui.main_window import MainWindow

class PasswordManagerApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.storage_manager = StorageManager()
        self.master_password = None
        self.main_window = None
    
    def run(self):
        """Executa aplicação"""
        # Mostrar tela de login
        login_window = LoginWindow(self.storage_manager)
        login_window.login_successful.connect(self.on_login_success)
        login_window.show()
        
        # Executar aplicação
        return self.app.exec()
    
    def on_login_success(self, master_password):
        """Callback quando login é bem-sucedido"""
        self.master_password = master_password
        
        # Abrir tela principal
        self.main_window = MainWindow(self.storage_manager, master_password)
        self.main_window.show()

if __name__ == "__main__":
    app = PasswordManagerApp()
    sys.exit(app.run())
