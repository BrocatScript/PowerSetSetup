from colorama import init, Fore, Back, Style
import os

init(autoreset=True)

print(Fore.RED + "test")
print(Fore.GREEN + "test")
print(Fore.YELLOW + "test")
print(Fore.BLUE + "test")
print(Fore.MAGENTA + "test")
print(Fore.CYAN + "test")

print(Fore.RED + Back.YELLOW + "test")
print(Style.BRIGHT + Fore.GREEN + "test")
print(Style.DIM + Fore.BLUE + "test")

print(Fore.RED + "test" + Style.RESET_ALL)
print("test")

print(Fore.LIGHTRED_EX + "test")
print(Fore.LIGHTGREEN_EX + "test")
print(Fore.LIGHTYELLOW_EX + "test")
os.system('pause')