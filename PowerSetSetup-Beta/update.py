import os
import sys
import glob
import subprocess
import time
import shutil
import ctypes
import tempfile
import logging

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "update_logs.txt")
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

Name_Program = "PowerSetSetup Update"
version = "1.0.0 Dev"

logger = logging.getLogger()
logging.info(f"--- {Name_Program} {version} ---")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    try:
        cmd_line = subprocess.list2cmdline(sys.argv)
        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            sys.executable,
            cmd_line,
            None,
            1
        )
    except Exception as e:
        logging.error(f"Error code: 1x1001 ({e})")
        print("Error code: 1x1001")

def get_temp_dir():
    base_temp = tempfile.gettempdir()
    temp_dir = os.path.join(base_temp, "PowerSetSetup_temp_update")
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir

def find_installer():
    temp_dir = get_temp_dir()
    patterns = ["*.exe", "*.msi"]
    files = []
    for pattern in patterns:
        files.extend(glob.glob(os.path.join(temp_dir, pattern)))

    if not files:
        return None, temp_dir

    files.sort(key=os.path.getmtime, reverse=True)
    return files[0], temp_dir

def force_remove_dir(temp_dir, max_attempts=3, delay=2):
    def on_rm_error(func, path, exc_info):
        logging.error(f"Error code: 1x1002 ({path}) ({exc_info[1]})")
        print("ERROR: Error code: 1x1002")

    for attempt in range(1, max_attempts + 1):
        if not os.path.exists(temp_dir):
            logging.error(f"The {temp_dir} folder no longer exists. Error code: 1x1003")
            print(f"The {temp_dir} folder no longer exists.")
            return True

        try:
            shutil.rmtree(temp_dir, onerror=on_rm_error)
            if not os.path.exists(temp_dir):
                logging.info(f"Attempt ({attempt}): deletion via shutil.rmtree.")
                print(f"Attempt to delete: {attempt}")
                return True
            else:
                logging.error(f"ERROR: Error shutil.rmtree did not delete the folder completely. Error code: 1x1004")
                print(f"ERROR: Error shutil.rmtree did not delete the folder completely.")
        except Exception as e:
            logging.error(f"Attempt {attempt}: Error code: 1x1005 ({e})")
            print(f"ERROR: Attempt {attempt}: Error code: 1x1005 ({e})")

        try:
            subprocess.run(f'rmdir /s /q "{temp_dir}"', shell=True,
                           check=True, capture_output=True)
            if not os.path.exists(temp_dir):
                print(f"Attempt: {attempt}")
                return True
            else:
                logging.error(f"Attempt {attempt}: Error code: 1x1010")
                print(f"ERROR: Attempt {attempt}: Error code: 1x1010")
        except subprocess.CalledProcessError as e2:
            logging.error(f"Attempt {attempt}: Error code: 1x1011 ({e2})")
            print(f"ERROR: Attempt {attempt}: Error code: 1x1011 ({e2})")

        if attempt < max_attempts:
            time.sleep(delay)
            delay *= 2
    
    logging.error(f"Error: Couldn't be deleted: {temp_dir} ({max_attempts}) attempts")
    print(f"ERROR: Error: Couldn't be deleted: {temp_dir} ({max_attempts}) attempts")
    return False

def main():
    installer, temp_dir = find_installer()

    try:
        if installer is not None:
            logging.info(f"The installer was found: {installer}")
            print(f"The installer was found: {installer}")
            if installer.endswith('.msi'):
                cmd = ['msiexec', '/i', installer]
            else:
                cmd = [installer]

            logging.info(f"Launching the installer {installer}...")
            print(f"Launching: {installer}...")
            process = subprocess.run(cmd, capture_output=True, text=True)

            if process.returncode == 0:
                logging.info("The installation was successful.")
                print("The installation was successful.")
            else:
                logging.error(f"Error code 1x1006 ({process.returncode})")
                print(f"ERROR: Error code 1x1006 ({process.returncode})")
                if process.stderr:
                    logging.info(process.stderr)
                    print(process.stderr)

            time.sleep(2)

        else:
            logging.error("The installation file was not found in the temporary folder! Error code: 1x1007")
            print("The installation file was not found in the temporary folder!")
            if os.path.isdir(temp_dir):
                logging.error(f"The {temp_dir} folder exists, but it doesn't contain an installer.")
                print(f"The {temp_dir} folder exists, but it doesn't contain an installer.")
            else:
                logging.error(f"Error code 1x1008: {temp_dir}")
                print(f"ERROR: Error code 1x1008: {temp_dir}")

        if os.path.isdir(temp_dir):
            logging.info(f"Removal: {temp_dir}")
            print(f"Removal: {temp_dir}")
            force_remove_dir(temp_dir)
        else:
            logging.error("Error code: 1x1009")
            print("ERROR: Error code: 1x1009")

    except Exception as e:
        logging.error(f"Error in ({e})")
        print(f"Error in: ({e})")
        if os.path.isdir(temp_dir):
            force_remove_dir(temp_dir)
        sys.exit(1)

    sys.exit(2)

if __name__ == "__main__":
    if not is_admin():
        run_as_admin()
        sys.exit()
    else:
        logging.info("Admin mode: True")
        main()