from dataclasses import dataclass
from typing import Optional
import json
from datetime import datetime

@dataclass
class PasswordEntry:
    """Modelo para uma entrada de senha"""
    id: str
    title: str
    username: str
    password: str
    url: Optional[str] = None
    notes: Optional[str] = None
    created_at: str = None
    updated_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.updated_at is None:
            self.updated_at = self.created_at
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'id': self.id,
            'title': self.title,
            'username': self.username,
            'password': self.password,
            'url': self.url,
            'notes': self.notes,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PasswordEntry':
        """Cria instância a partir de dicionário"""
        return cls(**data)
    
    def update_timestamp(self):
        """Atualiza timestamp de modificação"""
        self.updated_at = datetime.now().isoformat()

class PasswordDatabase:
    """Container para todas as senhas"""
    def __init__(self):
        self.entries: list[PasswordEntry] = []
    
    def to_json(self) -> str:
        """Serializa para JSON"""
        data = [entry.to_dict() for entry in self.entries]
        return json.dumps(data, indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'PasswordDatabase':
        """Deserializa do JSON"""
        db = cls()
        data = json.loads(json_str)
        db.entries = [PasswordEntry.from_dict(entry_data) for entry_data in data]
        return db
