import sys
import uuid
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLineEdit, QPushButton, QListWidget,
                               QListWidgetItem, QMessageBox, QDialog, QFormLayout,
                               QLabel, QTextEdit)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from src.models.password_model import PasswordEntry, PasswordDatabase

class PasswordDialog(QDialog):
    def __init__(self, entry=None, parent=None):
        super().__init__(parent)
        self.entry = entry
        self.is_edit = entry is not None
        self.setup_ui()

        if self.is_edit:
            self.load_entry_data()

    def setup_ui(self):
        title = "Editar Senha" if self.is_edit else "Nova Senha"
        self.setWindowTitle(title)
        self.setFixedSize(400, 350)
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: white;
            }
            QLineEdit, QTextEdit {
                padding: 8px;
                border: 2px solid #444;
                border-radius: 4px;
                background-color: #3c3c3c;
                color: white;
            }
            QPushButton {
                background-color: #0078d4;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
        """)

        layout = QFormLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Ex: Gmail, Facebook...")
        layout.addRow("Título:", self.title_input)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("usuário ou email")
        layout.addRow("Usuário:", self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("senha")
        layout.addRow("Senha:", self.password_input)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://...")
        layout.addRow("URL:", self.url_input)

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Anotações opcionais...")
        self.notes_input.setMaximumHeight(60)
        layout.addRow("Notas:", self.notes_input)

        # Botões
        button_layout = QHBoxLayout()

        # Botão deletar (só na edição)
        if self.is_edit:
            self.delete_button = QPushButton("🗑️ Deletar")
            self.delete_button.setStyleSheet("""
                QPushButton {
                    background-color: #d32f2f;
                    border: none;
                    padding: 8px 12px;
                    border-radius: 4px;
                    color: white;
                    font-weight: bold;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: #b71c1c;
                }
                QPushButton:pressed {
                    background-color: #8b0000;
                }
            """)
            self.delete_button.clicked.connect(self.delete_entry)
            button_layout.addWidget(self.delete_button)

        button_layout.addStretch()  # Espaço no meio

        self.save_button = QPushButton("Salvar")
        self.save_button.clicked.connect(self.accept)
        button_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addRow(button_layout)

        self.setLayout(layout)
        self.title_input.setFocus()

    def load_entry_data(self):
        """Carrega dados da entrada para edição"""
        self.title_input.setText(self.entry.title)
        self.username_input.setText(self.entry.username)
        self.password_input.setText(self.entry.password)
        self.url_input.setText(self.entry.url or "")
        self.notes_input.setText(self.entry.notes or "")

    def delete_entry(self):
        """Deletar entrada com confirmação"""
        reply = QMessageBox.question(
            self,
            "Confirmar Exclusão",
            f"Tem certeza que deseja deletar '{self.entry.title}'?\n\nEsta ação não pode ser desfeita!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No  # Botão padrão é "Não"
        )

        if reply == QMessageBox.Yes:
            # Sinalizar que deve deletar
            self.done(2)  # Código 2 = deletar (0=cancel, 1=accept, 2=delete)

    def get_entry_data(self):
        """Retorna dados do formulário"""
        title = self.title_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        url = self.url_input.text().strip() or None
        notes = self.notes_input.toPlainText().strip() or None

        if not title or not username or not password:
            QMessageBox.warning(self, "Erro", "Título, usuário e senha são obrigatórios")
            return None

        if self.is_edit:
            # Atualizar entrada existente
            self.entry.title = title
            self.entry.username = username
            self.entry.password = password
            self.entry.url = url
            self.entry.notes = notes
            self.entry.update_timestamp()
            return self.entry
        else:
            # Criar nova entrada
            return PasswordEntry(
                id=str(uuid.uuid4()),
                title=title,
                username=username,
                password=password,
                url=url,
                notes=notes
            )

class MainWindow(QMainWindow):
    def __init__(self, storage_manager, master_password):
        super().__init__()
        self.storage_manager = storage_manager
        self.master_password = master_password
        self.database = None
        self.filtered_entries = []

        self.load_database()
        self.setup_ui()
        self.filter_entries()  # Inicializar lista filtrada

    def setup_ui(self):
        self.setWindowTitle("Picoword Two - Gerenciador de Senhas")
        self.setMinimumSize(600, 400)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: white;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #444;
                border-radius: 4px;
                background-color: #3c3c3c;
                color: white;
            }
            QListWidget {
                background-color: #3c3c3c;
                border: 2px solid #444;
                border-radius: 4px;
                color: white;
                font-size: 12px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #555;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
            }
            QPushButton {
                background-color: #0078d4;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Barra de pesquisa
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Pesquisar senhas...")
        self.search_input.textChanged.connect(self.filter_entries)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Lista de senhas
        self.password_list = QListWidget()
        self.password_list.itemDoubleClicked.connect(self.edit_selected_entry)
        layout.addWidget(self.password_list)

        # Botões inferiores
        button_layout = QHBoxLayout()

        self.edit_button = QPushButton("Editar")
        self.edit_button.clicked.connect(self.edit_selected_entry)
        button_layout.addWidget(self.edit_button)

        button_layout.addStretch()  # Espaço no meio

        self.add_button = QPushButton("Adicionar")
        self.add_button.clicked.connect(self.add_new_entry)
        button_layout.addWidget(self.add_button)

        layout.addLayout(button_layout)

        central_widget.setLayout(layout)

    def load_database(self):
        """Carrega database do storage"""
        self.database = self.storage_manager.load_database(self.master_password)
        if self.database is None:
            QMessageBox.critical(self, "Erro", "Falha ao carregar database")
            sys.exit(1)

        # Inicializar lista filtrada
        self.filtered_entries = self.database.entries[:]

    def save_database(self):
        """Salva database no storage"""
        success = self.storage_manager.save_database(self.database, self.master_password)
        if not success:
            QMessageBox.critical(self, "Erro", "Falha ao salvar database")

    def refresh_list(self):
        """Atualiza lista de senhas"""
        self.password_list.clear()

        for entry in self.filtered_entries:
            item_text = f"{entry.title} ({entry.username})"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, entry.id)
            self.password_list.addItem(item)

    def filter_entries(self):
        """Filtra entradas baseado na pesquisa"""
        search_text = self.search_input.text().lower()

        if not search_text:
            self.filtered_entries = self.database.entries[:]
        else:
            self.filtered_entries = [
                entry for entry in self.database.entries
                if (search_text in entry.title.lower() or
                    search_text in entry.username.lower() or
                    (entry.url and search_text in entry.url.lower()))
            ]

        self.refresh_list()

    def get_selected_entry(self):
        """Retorna entrada selecionada"""
        current_item = self.password_list.currentItem()
        if not current_item:
            return None

        entry_id = current_item.data(Qt.UserRole)
        return next((entry for entry in self.database.entries if entry.id == entry_id), None)

    def add_new_entry(self):
        """Adiciona nova entrada"""
        dialog = PasswordDialog(parent=self)

        if dialog.exec() == QDialog.Accepted:
            new_entry = dialog.get_entry_data()
            if new_entry:
                self.database.entries.append(new_entry)
                self.save_database()
                self.filter_entries()  # Refresh

    def edit_selected_entry(self):
        """Edita entrada selecionada"""
        entry = self.get_selected_entry()
        if not entry:
            QMessageBox.information(self, "Info", "Selecione uma senha para editar")
            return

        dialog = PasswordDialog(entry, parent=self)
        result = dialog.exec()

        if result == QDialog.Accepted:
            # Salvar edição
            updated_entry = dialog.get_entry_data()
            if updated_entry:
                self.save_database()
                self.filter_entries()  # Refresh
        elif result == 2:  # Código de deletar
            # Remover entrada
            self.database.entries = [e for e in self.database.entries if e.id != entry.id]
            self.save_database()
            self.filter_entries()  # Refresh
            QMessageBox.information(self, "Sucesso", f"'{entry.title}' foi deletada")
