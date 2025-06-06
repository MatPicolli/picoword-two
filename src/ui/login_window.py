import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QMessageBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

class LoginWindow(QWidget):
    # Signal emitido quando login é bem-sucedido
    login_successful = Signal(str)  # passa a senha mestre
    
    def __init__(self, storage_manager):
        super().__init__()
        self.storage_manager = storage_manager
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Picoword Two - Login")
        self.setFixedSize(350, 200)
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: white;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #444;
                border-radius: 4px;
                background-color: #3c3c3c;
                color: white;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #0078d4;
            }
            QPushButton {
                background-color: #0078d4;
                border: none;
                padding: 10px;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Título
        title = QLabel("Picoword Two")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(title)
        
        # Espaçamento
        layout.addSpacing(20)
        
        # Campo senha mestre
        layout.addWidget(QLabel("Senha Mestre:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.returnPressed.connect(self.handle_login)
        layout.addWidget(self.password_input)
        
        # Botões
        button_layout = QHBoxLayout()
        
        self.login_button = QPushButton("Entrar")
        self.login_button.clicked.connect(self.handle_login)
        button_layout.addWidget(self.login_button)
        
        # Só mostra "Criar" se não existe database
        if not self.storage_manager.database_exists():
            self.create_button = QPushButton("Criar Nova")
            self.create_button.clicked.connect(self.handle_create)
            button_layout.addWidget(self.create_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Foco no campo de senha
        self.password_input.setFocus()
    
    def handle_login(self):
        password = self.password_input.text().strip()
        
        if not password:
            QMessageBox.warning(self, "Erro", "Digite a senha mestre")
            return
        
        # Tentar carregar database
        database = self.storage_manager.load_database(password)
        
        if database is None:
            QMessageBox.critical(self, "Erro", "Senha incorreta ou arquivo corrompido")
            self.password_input.clear()
            self.password_input.setFocus()
            return
        
        # Login bem-sucedido
        self.login_successful.emit(password)
        self.close()
    
    def handle_create(self):
        password = self.password_input.text().strip()
        
        if not password:
            QMessageBox.warning(self, "Erro", "Digite uma senha mestre")
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, "Erro", "Senha deve ter pelo menos 6 caracteres")
            return
        
        # Confirmar criação
        reply = QMessageBox.question(self, "Confirmar", 
                                   f"Criar novo cofre com esta senha?\n\nAVISO: Se esquecer esta senha, perderá todos os dados!",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Criar database vazio
            from src.models.password_model import PasswordDatabase
            empty_db = PasswordDatabase()
            
            success = self.storage_manager.save_database(empty_db, password)
            
            if success:
                QMessageBox.information(self, "Sucesso", "Cofre criado com sucesso!")
                self.login_successful.emit(password)
                self.close()
            else:
                QMessageBox.critical(self, "Erro", "Falha ao criar cofre")

if __name__ == "__main__":
    # Teste da tela de login
    app = QApplication(sys.argv)
    
    from src.storage.storage_manager import StorageManager
    storage = StorageManager("test_data")
    
    window = LoginWindow(storage)
    window.show()
    
    sys.exit(app.exec())
