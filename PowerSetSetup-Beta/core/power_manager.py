from __future__ import annotations

import codecs
import ctypes
import re
import subprocess
import sys
from dataclasses import dataclass
from typing import Iterable


@dataclass(slots=True)
class PowerScheme:
    """Одна схема электропитания Windows."""

    guid: str
    name: str
    active: bool = False

    @property
    def is_standard(self) -> bool:
        return self.guid.lower() in PowerManager.STANDARD_GUIDS


class PowerManager:
    """
    Работа со схемами электропитания Windows через powercfg.

    UI не должен знать команды powercfg напрямую. Всё, что связано
    с Windows Power Plans, находится здесь.
    """

    BALANCED_GUID = "381b4222-f694-41f0-9685-ff5bb260df2e"
    HIGH_PERFORMANCE_GUID = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
    POWER_SAVER_GUID = "a1841308-3541-4fab-bc81-f71556f20b4a"
    ULTIMATE_PERFORMANCE_GUID = "e9a42b02-d5df-448d-aa00-03f14749eb61"

    STANDARD_GUIDS = {
        BALANCED_GUID,
        HIGH_PERFORMANCE_GUID,
        POWER_SAVER_GUID,
        ULTIMATE_PERFORMANCE_GUID,
    }

    _GUID_RE = re.compile(
        r"[0-9a-fA-F]{8}-"
        r"[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{12}"
    )

    def __init__(self):
        self._check_windows()

    @staticmethod
    def _check_windows():
        import os

        if os.name != "nt":
            raise RuntimeError("PowerSetSetup поддерживает только Windows.")

    @staticmethod
    def _run_powercfg(*args: str) -> str:
        """
        Выполнить powercfg и вернуть вывод.

        powercfg локализован, поэтому не полагаемся на русский/английский
        текст команд. GUID остаются одинаковыми на всех языках Windows.
        """
        command = ["powercfg", *args]

        try:
            completed = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                check=False,
            )
        except FileNotFoundError as exc:
            raise RuntimeError(
                "Не удалось найти powercfg.exe. Это стандартная команда Windows."
            ) from exc
        except OSError as exc:
            raise RuntimeError(f"Не удалось запустить powercfg: {exc}") from exc

        stdout = PowerManager._decode_output(completed.stdout)
        stderr = PowerManager._decode_output(completed.stderr)

        if completed.returncode != 0:
            message = stderr.strip() or stdout.strip() or (
                f"powercfg завершился с кодом {completed.returncode}"
            )
            raise RuntimeError(message)

        return stdout

    @staticmethod
    def _decode_output(data: bytes) -> str:
        """
        Декодировать вывод Windows-команд без привязки к языку системы.

        Важный момент: powercfg.exe — консольная Windows-утилита. При
        перенаправлении stdout она может отдавать текст в OEM-кодировке
        текущей системы (например, CP866 для русской Windows), а не в
        ANSI/UTF-8. Поэтому нельзя просто поставить ``mbcs`` первым: на
        русской Windows это часто превращает русский текст в «кракозябры».

        Сначала проверяем BOM/UTF-16, затем UTF-8, затем OEM-кодировку
        Windows, и только после этого ANSI. OEM/ANSI берём через WinAPI,
        поэтому код одинаково работает для русской, немецкой и других
        локалей Windows.
        """
        if not data:
            return ""

        # BOM — самый надёжный способ определить Unicode-вывод.
        if data.startswith(codecs.BOM_UTF16_LE):
            return data.decode("utf-16-le", errors="replace")
        if data.startswith(codecs.BOM_UTF16_BE):
            return data.decode("utf-16-be", errors="replace")
        if data.startswith(codecs.BOM_UTF8):
            return data.decode("utf-8-sig", errors="replace")

        encodings: list[str] = ["utf-8"]

        if sys.platform == "win32":
            try:
                kernel32 = ctypes.windll.kernel32
                kernel32.GetOEMCP.restype = ctypes.c_uint
                kernel32.GetACP.restype = ctypes.c_uint

                oem_cp = kernel32.GetOEMCP()
                acp = kernel32.GetACP()

                if oem_cp:
                    encodings.append(f"cp{oem_cp}")
                if acp and acp != oem_cp:
                    encodings.append(f"cp{acp}")
            except (AttributeError, OSError):
                pass

        # Запасные варианты для окружений, где WinAPI недоступен.
        encodings.extend(("cp866", "cp1251", "mbcs"))

        seen: set[str] = set()
        for encoding in encodings:
            if encoding in seen:
                continue
            seen.add(encoding)
            try:
                return data.decode(encoding)
            except (UnicodeDecodeError, LookupError):
                pass

        return data.decode(errors="replace")

    @classmethod
    def list_schemes(cls) -> list[PowerScheme]:
        """
        Получить все схемы электропитания.

        Не зависит от языка Windows: название извлекается из скобок,
        а GUID используется как основной идентификатор.
        """
        output = cls._run_powercfg("/list")
        schemes: list[PowerScheme] = []

        for line in output.splitlines():
            match = cls._GUID_RE.search(line)
            if not match:
                continue

            guid = match.group(0).lower()

            # Обычно powercfg выводит:
            # Power Scheme GUID: <GUID>  (Name) *
            # или локализованный аналог.
            tail = line[match.end():]
            name_match = re.search(r"\(([^()]*)\)", tail)

            if name_match:
                name = name_match.group(1).strip()
            else:
                # Запасной вариант, если формат вывода изменится.
                name = guid

            active = "*" in tail
            schemes.append(PowerScheme(guid, name, active))

        return schemes

    @classmethod
    def get_active_scheme(cls) -> PowerScheme | None:
        """Получить текущую активную схему."""
        output = cls._run_powercfg("/getactivescheme")
        match = cls._GUID_RE.search(output)

        if not match:
            return None

        guid = match.group(0).lower()

        for scheme in cls.list_schemes():
            if scheme.guid == guid:
                return scheme

        return PowerScheme(guid=guid, name=guid, active=True)

    @classmethod
    def activate_scheme(cls, guid: str):
        """Сделать указанную схему активной."""
        cls._validate_guid(guid)
        cls._run_powercfg("/setactive", guid)

    @classmethod
    def delete_scheme(cls, guid: str, allow_standard: bool = False):
        """
        Удалить схему.

        По умолчанию стандартные схемы защищены от удаления.
        Это пригодится для кнопки «Очистить лишние схемы».
        """
        cls._validate_guid(guid)

        if not allow_standard and guid.lower() in cls.STANDARD_GUIDS:
            raise RuntimeError(
                "Стандартную схему Windows нельзя удалить через очистку "
                "пользовательских схем."
            )

        active = cls.get_active_scheme()
        if active and active.guid.lower() == guid.lower():
            raise RuntimeError(
                "Нельзя удалить активную схему. Сначала переключитесь "
                "на другую схему электропитания."
            )

        cls._run_powercfg("/delete", guid)

    @classmethod
    def find_extra_schemes(cls) -> list[PowerScheme]:
        """
        Найти пользовательские схемы-кандидаты на очистку.

        Это именно анализ, а не удаление.
        Стандартные схемы Windows здесь не считаются лишними.
        """
        return [
            scheme
            for scheme in cls.list_schemes()
            if scheme.guid.lower() not in cls.STANDARD_GUIDS
        ]

    @classmethod
    def restore_default_schemes(cls):
        """
        Восстановить стандартные схемы Windows.

        ВАЖНО:
        powercfg -restoredefaultschemes может удалить пользовательские
        схемы. Вызывать этот метод нужно только после подтверждения пользователя.
        """
        cls._run_powercfg("-restoredefaultschemes")

    @classmethod
    def standard_schemes(cls) -> Iterable[PowerScheme]:
        """Стандартные GUID в виде объектов, если они существуют в системе."""
        return (
            scheme
            for scheme in cls.list_schemes()
            if scheme.guid.lower() in cls.STANDARD_GUIDS
        )

    @staticmethod
    def _validate_guid(guid: str):
        if not PowerManager._GUID_RE.fullmatch(guid.strip()):
            raise ValueError(f"Некорректный GUID схемы электропитания: {guid}")
