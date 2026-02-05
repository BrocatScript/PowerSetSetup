import requests
import json
import os
import subprocess
from pathlib import Path
from packaging import version
import time
import platform

# Конфигурация
CONFIG_PATH = "data/config/config.json"
GITHUB_RELEASES_URL = "https://api.github.com/repos/BrocatScript/PowerSetSetup/releases/latest"

def clear():
    os.system('cls')

def load_config() -> dict:
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        config = normalize_config_types(config)
        
        defaults = {
            "allow_beta": False,
            "check_on_startup": True,
            "auto_download_install": False,
            "version": "0.0.0",
            "last_modified": time.strftime("%Y-%m-%d %H:%M:%S"),
            "description": "settings for PowerSetSetup"
        }
        
        for key, value in defaults.items():
            config.setdefault(key, value)
        
        return config
        
    except FileNotFoundError:
        return create_default_config()
    except (json.JSONDecodeError, Exception) as e:
        print(f"Ошибка загрузки конфига: {e}")
        return None

def normalize_config_types(config: dict) -> dict:
    if "allow_beta" in config:
        if isinstance(config["allow_beta"], str):
            config["allow_beta"] = config["allow_beta"].strip() == "1"
    
    if "auto_download_install" in config:
        if isinstance(config["auto_download_install"], str):
            config["auto_download_install"] = config["auto_download_install"].lower() in ["true", "1", "yes"]
    
    return config

def create_default_config() -> dict:
    default_config = {
        "language": "en",
        "auto_language": True,
        "allow_beta": False,
        "check_on_startup": True,
        "auto_download_install": False,
        "version": "0.0.0",
        "last_modified": time.strftime("%Y-%m-%d %H:%M:%S"),
        "description": "settings for PowerSetSetup"
    }
    
    try:
        Path(CONFIG_PATH).parent.mkdir(parents=True, exist_ok=True)
        
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        
        return default_config
        
    except Exception as e:
        print(f"Ошибка создания конфига: {e}")
        return None

def format_version_for_display(version_str: str) -> str:
    if not version_str:
        return "0.0.0"
    
    version_str = version_str.lstrip('vV')
    
    modifiers = ['beta', 'fix', 'hotfix', 'alpha', 'rc', 'dev', 'patch', 'update']
    
    version_lower = version_str.lower()
    
    for modifier in modifiers:
        if modifier in version_lower:
            pos = version_lower.find(modifier)
            
            if pos > 0 and version_str[pos-1] != ' ':
                version_str = version_str[:pos] + ' ' + version_str[pos:]
                pos += 1
            
            end_pos = pos + len(modifier)
            modifier_part = version_str[pos:end_pos]
            capitalized_modifier = modifier_part.capitalize()
            version_str = version_str[:pos] + capitalized_modifier + version_str[end_pos:]
            break
    
    return version_str

def normalize_version(version_str: str) -> str:
    if not version_str:
        return "0.0.0"
    
    version_str = version_str.lstrip('vV').lower().replace(' ', '')
    
    if 'beta' in version_str:
        version_str = version_str.replace('beta', 'b')
    elif 'fix' in version_str:
        version_str = version_str.replace('fix', '.post')
    elif 'hotfix' in version_str:
        version_str = version_str.replace('hotfix', '.post')
    elif 'alpha' in version_str:
        version_str = version_str.replace('alpha', 'a')
    elif 'rc' in version_str:
        version_str = version_str.replace('rc', 'rc')
    
    return version_str

def get_remote_version() -> str:
    try:
        response = requests.get(GITHUB_RELEASES_URL, timeout=10)
        response.raise_for_status()
        tag_name = response.json().get('tag_name', '').lstrip('vV')
        return tag_name
    except Exception as e:
        print(f"Ошибка получения версии: {e}")
        return ""

def check_update_needed(local_ver: str, remote_ver: str, allow_beta: bool) -> tuple:
    if not remote_ver:
        return False, "Не удалось получить удаленную версию"
    
    local_normalized = normalize_version(local_ver)
    remote_normalized = normalize_version(remote_ver)
    
    if 'b' in remote_normalized and not allow_beta:
        return False, "Бета-версия доступна, но allow_beta=False"
    
    try:
        local_norm = version.parse(local_normalized)
        remote_norm = version.parse(remote_normalized)
        
        if local_norm < remote_norm:
            local_display = format_version_for_display(local_ver)
            remote_display = format_version_for_display(remote_ver)
            return True, f"Доступно обновление: {local_display} → {remote_display}"
        elif local_norm > remote_norm:
            local_display = format_version_for_display(local_ver)
            remote_display = format_version_for_display(remote_ver)
            return False, f"Локальная версия новее ({local_display} > {remote_display})"
        return False, "Версии идентичны"
    except Exception as e:
        print(f"Ошибка сравнения версий: {e}")
        return False, "Ошибка сравнения версий"

def find_installer(release_info: dict) -> dict:
    if not release_info or 'assets' not in release_info:
        print("Нет файлов в релизе")
        return None
    
    for asset in release_info['assets']:
        if asset['name'].lower().endswith('.exe'):
            name_lower = asset['name'].lower()
            if any(keyword in name_lower for keyword in ['installer', 'setup', 'install']):
                return asset
    
    for asset in release_info['assets']:
        if asset['name'].lower().endswith('.exe'):
            return asset
    
    return None

def download_file(url: str, filename: str) -> bool:
    try:
        print(f"Скачивание: {filename}")
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\rПрогресс: {percent:.1f}%", end='')
        
        print(f"\nФайл сохранен: {filename}")
        return True
        
    except Exception as e:
        print(f"\nОшибка скачивания: {e}")
        return False

def run_and_delete_installer(filename: str):
    try:
        print(f"Запуск установщика: {filename}")
        
        if platform.system() != 'Windows':
            print("Установка .exe файлов поддерживается только на Windows")
            return False
        
        process = subprocess.Popen([filename])
        process.wait()
        
        time.sleep(1)
        if os.path.exists(filename):
            os.remove(filename)
            print(f"Файл {filename} удален")
        
        return True
        
    except Exception as e:
        print(f"Ошибка при работе с установщиком: {e}")
        if os.path.exists(filename):
            os.remove(filename)
        return False

def update_config_version(config: dict, new_version: str) -> bool:
    try:
        formatted_version = format_version_for_display(new_version)
        config["version"] = formatted_version
        config["last_modified"] = time.strftime("%Y-%m-%d")
        
        Path(CONFIG_PATH).parent.mkdir(parents=True, exist_ok=True)
        
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"Версия в конфиге обновлена: {formatted_version}")
        return True
        
    except Exception as e:
        print(f"Ошибка обновления конфига: {e}")
        return False

def check_for_updates(config: dict, auto_start_check: bool = False, show_prompt: bool = True) -> bool:
    if not auto_start_check and not config.get("check_on_startup", False):
        return False

    clear()
    print("PowerSetSetup Updater")
    
    local_version = config["version"]
    
    print("Проверка обновлений...")
    remote_version = get_remote_version()
    
    if not remote_version:
        print("Не удалось проверить обновления")
        return False
    
    update_needed, message = check_update_needed(
        local_version, 
        remote_version, 
        config.get("allow_beta", False)
    )
    
    print(message)
    
    if not update_needed:
        print("\nОбновление не требуется.")
        time.sleep(2)
        return False
    
    auto_download_install = config.get("auto_download_install", False)
    
    if not auto_download_install and show_prompt:
        choice = input("\nСкачать и установить обновление? (y/n): ")
        if choice.lower() != 'y':
            print("Обновление отменено")
            time.sleep(2)
            return False
    elif auto_download_install:
        print("\nАвтоустановка включена. Начинаем процесс обновления...")
    else:
        print("Обновление отменено (автоустановка выключена)")
        time.sleep(2)
        return False
    
    print("\nПолучение информации о релизе...")
    try:
        response = requests.get(GITHUB_RELEASES_URL, timeout=10)
        release_info = response.json()
    except Exception as e:
        print(f"Ошибка получения релиза: {e}")
        return False
    
    installer = find_installer(release_info)
    if not installer:
        print("Установщик не найден")
        return False
    
    print(f"\nРелиз: {release_info.get('name', 'Без названия')}")
    print(f"Файл: {installer['name']} ({installer['size'] / 1024 / 1024:.2f} МБ)")
    
    filename = installer['name']
    
    if not download_file(installer['browser_download_url'], filename):
        print("Ошибка скачивания")
        return False
    
    update_config_version(config, remote_version)
    
    print("ОБНОВЛЕНИЕ УСПЕШНО СКАЧАНО!")
    
    if auto_download_install:
        print("\nАвтоустановка включена. Запускаем установщик...")
        if run_and_delete_installer(filename):
            print("Установщик успешно выполнен")
            return True
        else:
            print("Ошибка при работе установщика")
            return False
    elif show_prompt:
        if input("Запустить установщик сейчас? (y/n): ").lower() == 'y':
            if run_and_delete_installer(filename):
                print("Установщик успешно выполнен")
                return True
            else:
                print("Ошибка при работе установщика")
                return False
        else:
            print(f"Установщик сохранен как: {filename}")
            print("Вы можете запустить его вручную позже.")
            return False
    
    return False

def standalone_update_check():
    clear()
    print('Проверка обновлений.')
    
    try:
        config = load_config()
        if config is None:
            print("Не удалось загрузить конфигурацию. Используются настройки по умолчанию.")
            config = create_default_config()
            if config is None:
                print("Не удалось создать конфигурацию по умолчанию.")
                return
        
        current_version = config.get('version', 'неизвестно')
        formatted_current = format_version_for_display(current_version)
        print(f"Текущая версия: {formatted_current}")
        
        clear()
        print("\nПроверка обновлений..")
        print(f"Текущая версия: {formatted_current}")
        remote_version = get_remote_version()
        
        if not remote_version:
            print("Не удалось проверить обновления. Проверьте подключение к интернету.")
            return
        
        formatted_remote = format_version_for_display(remote_version)
        print(f"Последняя версия на GitHub: {formatted_remote}")
        
        update_needed, message = check_update_needed(
            config.get("version", "0.0.0"), 
            remote_version, 
            config.get("allow_beta", False)
        )
        
        print(f"\n{message}")
        
        if not update_needed:
            print("\nВаша версия актуальна!")
            return
        
        choice = input("\nСкачать и установить обновление? (y/n): ")
        if choice.lower() != 'y':
            print("Обновление отменено.")
            return
        
        print("\nПолучение информации о релизе...")
        try:
            response = requests.get(GITHUB_RELEASES_URL, timeout=10)
            release_info = response.json()
        except Exception as e:
            print(f"Ошибка получения релиза: {e}")
            return

        installer = find_installer(release_info)
        if not installer:
            print("Установщик не найден в релизе.")
            return
        
        print(f"\nРелиз: {release_info.get('name', 'Без названия')}")
        print(f"Файл: {installer['name']} ({installer['size'] / 1024 / 1024:.2f} МБ)")
        
        filename = installer['name']
        
        print("\n" + "=" * 50)
        if not download_file(installer['browser_download_url'], filename):
            print("Ошибка скачивания.")
            return

        update_config_version(config, remote_version)
        
        print("\n" + "=" * 50)
        print("ОБНОВЛЕНИЕ УСПЕШНО СКАЧАНО!")
        print("=" * 50)
        
        choice = input("\nЗапустить установщик сейчас? (y/n): ")
        if choice.lower() == 'y':
            if run_and_delete_installer(filename):
                print("\nУстановщик успешно выполнен!")
                print("Теперь можно запустить PowerSetSetup.exe для работы с программой.")
            else:
                print("\nОшибка при работе установщика.")
        else:
            print(f"\nУстановщик сохранен как: {filename}")
            print("Вы можете запустить его вручную позже.")
            
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")
        print("\nРекомендации:")
        print("1. Проверьте подключение к интернету")
        print("2. Убедитесь, что у вас есть права на запись в текущую директорию")
        print("3. Попробуйте запустить от имени администратора")

def main():
    clear()
    standalone_update_check()
    print(f"\n\n\n\n")
    os.system('pause')

if __name__ == "__main__":
    main()