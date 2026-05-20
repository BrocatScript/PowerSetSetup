import psutil
import time
import os

def count_processes_by_name(name):
    """Возвращает количество процессов, содержащих name в имени."""
    count = 0
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and name.lower() in proc.info['name'].lower():
                count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return count

def main():
    target_name = "chrome.exe"  # Замените на нужное имя процесса
    refresh_interval = 1  # секунды

    try:
        while True:
            count = count_processes_by_name(target_name)
            if count > 0:
                # Очистка консоли
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"Отслеживание процессов, содержащих '{target_name}'. Для выхода нажмите Ctrl+C.")
                print(f"Количество процессов '{target_name}': {count}")
                time.sleep(refresh_interval)
            elif count <= 0:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"Отслеживание процессов, содержащих '{target_name}'. Для выхода нажмите Ctrl+C.")
                print(f"Процесс: '{target_name}' не запущен")
                time.sleep(refresh_interval)

    except KeyboardInterrupt:
        print("\nЗавершение.")

if __name__ == "__main__":
    main()