import os
from time import sleep

import subprocess

cmd = ["cmd.exe", "/c", "start", "chrome.exe"]


def main():
    p = subprocess.Popen(
        cmd,
        creationflags=subprocess.CREATE_NO_WINDOW  # или 0x08000000
        )

def kill():
    os.system("taskkill /f /im cmd.exe")

if __name__ == "__main__":
    main()
    kill()