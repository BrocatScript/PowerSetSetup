import requests
import time
import random
import os
import sys
import subprocess
import json
from packaging.version import parse as parse_version
import tempfile
import platform
import logging

sleep = time.sleep

CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.abspath(sys.argv[0])),
    "data", "config", "config.json"
)

Name_Program = "Check_update"
version = "Dev 1.0.0"

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "logs.txt")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, mode='w', encoding='utf-8'),
        # logging.StreamHandler()  # Вывод в консоль
    ]
)

logger = logging.getLogger()
logging.info(f"--- {Name_Program} {version} ---")

VERSION_URL = "https://raw.githubusercontent.com/BrocatScript/PowerSetSetup/main/version.json"

def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        error_os()

def error_os():
    try:
        clear()
        print(f"ERROR: YOU SYSTEM NOT WINDOWS! YOU SYSTEM {platform.system}")
        sys.exit(5)
    except Exception as e:
        clear()
        logging.error(f"Critical error in error_os: {e}, uninstall program please!")
        print(f"Critical error in error_os: {e}")
        sys.exit(5)

def load_config():
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: файл конфигурации не найден по пути {CONFIG_PATH}")
        sys.exit(2)
    except json.JSONDecodeError:
        print("Ошибка: не удалось разобрать config.json (некорректный JSON)")
        sys.exit(2)
    except Exception as e:
        print(f"Ошибка при чтении config.json: {e}")
        sys.exit(2)

def build_full_version(config):
    version = config.get("version")
    if not version:
        print("Ошибка: в файле config.json отсутствует поле 'version'")
        sys.exit(2)

    build = config.get("build")
    if build is not None:
        try:
            build_num = int(build)
            return f"{version}+build.{build_num}"
        except (ValueError, TypeError):
            return version
    return version

def check_for_updates():
    try:
        config = load_config()
        current_version_str = build_full_version(config)
        allow_beta = config.get("allow_beta", False)
        auto_download = config.get("auto_download_install", False)

        url = f"{VERSION_URL}?t={int(time.time())}&r={random.random()}"
        headers = {"Cache-Control": "no-cache", "Pragma": "no-cache"}
        resp = requests.get(url, timeout=5, headers=headers)
        resp.raise_for_status()
        data = resp.json()

        if not isinstance(data, dict):
            print(f"Ошибка: сервер вернул не объект JSON, а {type(data).__name__}")
            os.system("pause")
            return

        server_version_str = data.get("version")
        if not server_version_str:
            print("Ошибка: в JSON отсутствует поле 'version'")
            os.system("pause")
            return

        print(f"🌐: {server_version_str}")
        print(f"🖥️: {current_version_str}")

        server_version = parse_version(server_version_str)
        current_version = parse_version(current_version_str)

        if not allow_beta and server_version.is_prerelease:
            print("✅ Update beta: ❌ The beta version is not available (allow_beta = false).")
            print("🌐🤜 🤛🖥️👍")
            os.system("pause")
            return

        if server_version > current_version:
            print(f"✅ Update: {server_version_str}")
            download_url = data.get("download_url")
            if download_url:
                if auto_download:
                    download_and_update(download_url)
                else:
                    answer = input("Download the update?").lower()
                    if answer in ["y", "yes", "д", "да"]:
                        download_and_update(download_url)
                    else:
                        clear()
                        open_powersetsetup()
            else:
                print("ERROR: Error code: 1x1013")
        else:
            print("✅ 🖥️ = 🌐👍")
            open_powersetsetup()

    except Exception as e:
        print(f"❌ ERROR: {e}")
        os.system("pause")

def open_powersetsetup():
    try:
        base_path = os.path.dirname(sys.executable)
        exe_path = os.path.join(base_path, "PowerSetSetup.exe")
        subprocess.Popen([exe_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        sys.exit(0)
    except Exception as e:
        clear()
        logging.error("Error start PowerSetSetup")
        print("ERROR: Error start")
        sys.exit(2)

def download_and_update(url: str):
    try:
        temp_dir = os.path.join(tempfile.gettempdir(), "PowerSetSetup_temp_update")
        os.makedirs(temp_dir, exist_ok=True)

        filename = url.split('/')[-1]
        save_path = os.path.join(temp_dir, filename)

        print(f"\nInstall in {save_path}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192
        downloaded = 0
        print()
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=block_size):
                file.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = downloaded / total_size * 100
                    print(f"\r💾: {percent:.1f}%", end='')
        print("\n💾👍 = ✅")

        script_dir = os.path.dirname(sys.argv[0])
        update_exe = os.path.join(script_dir, "update.exe")

        if os.path.isfile(update_exe):
            print(f"\nStart {update_exe}...\n\n\n")
            subprocess.Popen([update_exe, temp_dir])
            sys.exit(0)
        else:
            print(f"ERROR: File {update_exe} not found. Please run the installer manually from the folder {temp_dir}.")
            sleep(2)
    except Exception as e:
        print(f"ERROR: Error code 0x0000: {e}")
        sleep(2)

def main():
    print("=== Update Check ===")
    check_for_updates()
    sleep(2)

if __name__ == "__main__":
    main()