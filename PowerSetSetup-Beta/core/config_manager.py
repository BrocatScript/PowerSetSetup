import os
import json
from typing import Any, Optional

class ConfigManager:
    """Управление конфигурационным файлом приложения."""

    DEFAULT_CONFIG = {
        "description": "settings for PowerSetSetup",
        "language": "System",
        "version": "1.0.2",
        "version_extension": "beta",
        "build": 3,
        "preliminary_versions": True,
        "check_for_updates_on_startup": True,
        "auto_update": False,
        "theme": "System",
        "last_modified": "2026-08-17 00:00:00",
        "send_error_reports": False
    }

    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self._load()

    def _load(self) -> dict:
        """Загружает конфиг из файла. Если файла нет или он повреждён – создаёт дефолтный."""
        if not os.path.exists(self.config_path):
            self._ensure_dir()
            self._write_default()
            return self.DEFAULT_CONFIG.copy()

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            # гарантируем наличие всех ключей
            for key in self.DEFAULT_CONFIG:
                if key not in loaded:
                    loaded[key] = self.DEFAULT_CONFIG[key]
            return loaded
        except (json.JSONDecodeError, IOError):
            self._write_default()
            return self.DEFAULT_CONFIG.copy()

    def _write_default(self):
        """Записывает дефолтный конфиг в файл."""
        self._ensure_dir()
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.DEFAULT_CONFIG, f, indent=4, ensure_ascii=False)

    def _ensure_dir(self):
        """Создаёт папку для конфига, если её нет."""
        directory = os.path.dirname(self.config_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

    def save(self):
        """Сохраняет текущий конфиг в файл с отладочным выводом."""
        try:
            self._ensure_dir()
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            print(f"[ConfigManager] Saved to {self.config_path}")
        except Exception as e:
            print(f"[ConfigManager] ERROR saving config: {e}")
            raise

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Возвращает значение по ключу."""
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        """Устанавливает значение и сохраняет конфиг."""
        self.config[key] = value
        self.save()