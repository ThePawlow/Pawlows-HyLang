import re

import yaml
from pathlib import Path
from typing import Union
from dataclasses import dataclass

TranslationValue = Union[str, dict[str, "TranslationValue"]]
Translations = dict[str, TranslationValue]


@dataclass
class HyLangFile:
    """Handles conversion between YAML and .lang formats."""

    path: Path

    def __post_init__(self):
        self.path = Path(self.path)

    def load_yaml(self) -> Translations:
        if not self.path.exists():
            raise FileNotFoundError(f"File not found: {self.path}")
        with open(self.path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if data is None:
            raise ValueError("File is empty or not found")

        if type(data) is not dict:
            raise ValueError("File contains no valid data")

        return data or {}

    def save_yaml(self, data: Translations) -> None:
        with open(self.path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False,
                      allow_unicode=True, sort_keys=True)

    def load_lang(self) -> Translations:
        entries = {}
        with open(self.path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and '=' in line:
                    key, value = line.split('=', 1)
                    entries[key.strip()] = value
        return entries

    @staticmethod
    def save_lang(path, flat_data: Translations) -> None:
        with open(path, 'w', encoding='utf-8') as f:
            for key in sorted(flat_data.keys()):
                f.write(f"{key}={flat_data[key]}\n")

    @staticmethod
    def convert_yamldict_to_langdict(data: Translations, prefix: str = "") -> Translations:
        """Convert nested YAML structure to flat key=value pairs."""

        if data is None or data == {}:
            raise ValueError("Data is empty or invalid")

        result = {}
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key

            if isinstance(value, dict):
                result.update(HyLangFile.convert_yamldict_to_langdict(value, full_key))
            else:
                if value is None:
                    raise ValueError("Value is empty or invalid")
                result[full_key] = str(value) if value is not None else ""
        return result

    @staticmethod
    def is_valid_prefix(prefix: str) -> bool:
        """Validate that key contains only alphanumeric chars, underscores, and dots."""
        if (not prefix or
                prefix.startswith('.') or
                prefix.endswith('.') or
                '..' in prefix or
                not all(c.isalnum() or c in '._' for c in prefix)):
            return False
        return True

    @staticmethod
    def convert_langdict_to_yamldict(data: Translations) -> Translations:
        """Convert flat key=value pairs to nested structure."""
        if data is None or data == {}:
            raise ValueError("Data is empty or invalid")

        result: dict = {}
        for key, value in data.items():
            if not HyLangFile.is_valid_prefix(key):
                raise ValueError(f"'{key}' contains invalid characters")

            parts = key.split('.')
            current = result
            for part in parts[:-1]:
                current = current.setdefault(part, {})
            current[parts[-1]] = value
        return result
