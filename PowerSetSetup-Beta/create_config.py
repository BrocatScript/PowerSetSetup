from datetime import datetime
import json
import os

print("Запуск")
target_dir = r"C:/Users/PC/OneDrive/Desktop/Dev PowerSetSetup/GUI_PowerSetSetup/PowerSetSetup/data/config"
os.chdir(target_dir)
print("Текущая папка:", os.getcwd())

def create_default_config():
    default_config = {
        "language": "en",
        "auto_language": True,
        "allow_beta": True,
        "auto_download_install": False,
        "version": "1.0.2-beta",
        "build": 2,
        "theme": "System",
        "checkForUpdatesOnStartup": True,
        "last_modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "description": "settings for PowerSetSetup"
    }

    try:
        with open("config.json", "w") as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)
        print("Файл config.json успешно записан")
    except Exception as e:
        print(f"Ошибка: {e}")

create_default_config()
os.system("pause")