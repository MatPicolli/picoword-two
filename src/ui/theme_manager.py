from PySide6.QtCore import QObject, Signal

class ThemeManager(QObject):
    theme_changed = Signal(str)  # Emite "dark" ou "light"

    def __init__(self):
        super().__init__()
        self.current_theme = "dark"  # Padrão escuro

    def toggle_theme(self):
        """Alterna entre tema claro e escuro"""
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.theme_changed.emit(self.current_theme)
        return self.current_theme

    def set_theme(self, theme):
        """Define tema específico"""
        if theme in ["dark", "light"]:
            self.current_theme = theme
            self.theme_changed.emit(self.current_theme)

    def get_theme(self):
        """Retorna tema atual"""
        return self.current_theme

    def get_main_window_style(self, theme):
        """Retorna CSS para janela principal"""
        if theme == "dark":
            return """
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
                QMenuBar {
                    background-color: #3c3c3c;
                    color: white;
                    border-bottom: 1px solid #555;
                }
                QMenuBar::item {
                    background-color: transparent;
                    padding: 4px 8px;
                }
                QMenuBar::item:selected {
                    background-color: #0078d4;
                }
                QMenu {
                    background-color: #3c3c3c;
                    color: white;
                    border: 1px solid #555;
                }
                QMenu::item:selected {
                    background-color: #0078d4;
                }
            """
        else:  # light theme
            return """
                QMainWindow {
                    background-color: #ffffff;
                    color: #000000;
                }
                QLineEdit {
                    padding: 8px;
                    border: 2px solid #cccccc;
                    border-radius: 4px;
                    background-color: #ffffff;
                    color: #000000;
                }
                QListWidget {
                    background-color: #ffffff;
                    border: 2px solid #cccccc;
                    border-radius: 4px;
                    color: #000000;
                    font-size: 12px;
                }
                QListWidget::item {
                    padding: 8px;
                    border-bottom: 1px solid #eeeeee;
                }
                QListWidget::item:selected {
                    background-color: #0078d4;
                    color: white;
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
                QMenuBar {
                    background-color: #f5f5f5;
                    color: #000000;
                    border-bottom: 1px solid #cccccc;
                }
                QMenuBar::item {
                    background-color: transparent;
                    padding: 4px 8px;
                }
                QMenuBar::item:selected {
                    background-color: #0078d4;
                    color: white;
                }
                QMenu {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #cccccc;
                }
                QMenu::item:selected {
                    background-color: #0078d4;
                    color: white;
                }
            """

    def get_dialog_style(self, theme):
        """Retorna CSS para diálogos"""
        if theme == "dark":
            return """
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
                QLabel {
                    color: white;
                }
            """
        else:  # light theme
            return """
                QDialog {
                    background-color: #ffffff;
                    color: #000000;
                }
                QLineEdit, QTextEdit {
                    padding: 8px;
                    border: 2px solid #cccccc;
                    border-radius: 4px;
                    background-color: #ffffff;
                    color: #000000;
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
                QLabel {
                    color: #000000;
                }
            """

    def get_login_style(self, theme):
        """Retorna CSS para tela de login"""
        if theme == "dark":
            return """
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
            """
        else:  # light theme
            return """
                QWidget {
                    background-color: #ffffff;
                    color: #000000;
                }
                QLineEdit {
                    padding: 8px;
                    border: 2px solid #cccccc;
                    border-radius: 4px;
                    background-color: #ffffff;
                    color: #000000;
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
            """
