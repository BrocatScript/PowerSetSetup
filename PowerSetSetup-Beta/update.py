import os
import sys
import glob
import subprocess
import time
import shutil

def find_installer():
    base_dir = os.path.dirname(sys.argv[0])
    temp_dir = os.path.join(base_dir, "temp_update")
    if not os.path.isdir(temp_dir):
        return None, None

    patterns = ["*.exe", "*.msi"]
    files = []
    for pattern in patterns:
        files.extend(glob.glob(os.path.join(temp_dir, pattern)))

    if not files:
        return None, None

    files.sort(key=os.path.getmtime, reverse=True)
    return files[0], temp_dir

def main():
    installer, temp_dir = find_installer()
    if installer is None:
        print("Не найден установочный файл в папке temp_update.")
        input("Нажмите Enter для выхода...")
        sys.exit(1)

    print(f"Запуск установщика: {installer}")
    try:
        if installer.endswith('.msi'):
            cmd = ['msiexec', '/i', installer]
        else:
            cmd = [installer]

        process = subprocess.run(cmd, capture_output=True, text=True)
        if process.returncode == 0:
            print("Установка завершена успешно.")
        else:
            print(f"Установка завершилась с кодом ошибки {process.returncode}.")
            if process.stderr:
                print(process.stderr)

        time.sleep(2)

        if temp_dir and os.path.isdir(temp_dir):
            print(f"Удаление временной папки: {temp_dir}")
            shutil.rmtree(temp_dir, ignore_errors=True)
            if not os.path.exists(temp_dir):
                print("Папка успешно удалена.")
            else:
                print("Не удалось полностью удалить папку (возможно, некоторые файлы заняты).")

    except Exception as e:
        print(f"Ошибка при запуске установщика: {e}")
        input("Нажмите Enter для выхода...")
        sys.exit(1)

    print("Скрипт обновления завершит работу через 5 секунд...")
    time.sleep(5)

if __name__ == "__main__":
    main()