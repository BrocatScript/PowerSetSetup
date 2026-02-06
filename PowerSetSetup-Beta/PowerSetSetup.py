import sys
import subprocess
import os
import json
from colorama import init, Fore, Back, Style
import gettext
import time
import platform
import logging
import locale
import webbrowser
from datetime import datetime

sleep = time.sleep

try:
    from update_checker import check_for_updates, load_config as load_update_config
    UPDATE_CHECKER_AVAILABLE = True
except ImportError as e:
    logging.error(f"The update verification module is unavailable: ({e})")
    UPDATE_CHECKER_AVAILABLE = False

Name_Program = "PowerSetSetup"
version = "Dev 1.0.2"

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

def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        error_os()

try:
    logging.debug("Launching UTF-8 encoding")
    os.system('chcp 65001 > nul')
    logging.debug('The UTF-8 encoder has been applied!')
except Exception as e:
    logging.error(f"Couldn't apply UTF-8 encoder: ({e})")
    clear()
    print('Error: UTF-8 not activate!')
    print('Program close')
    print('3')
    sleep(1)
    clear()
    print('Error: UTF-8 not activate!')
    print('Program close')
    print('2')
    sleep(1)
    clear()
    print('Error: UTF-8 not activate!')
    print('Program close')
    print('1')
    sys.exit(1)

init(autoreset=True)

# Перевод
LOCALE_DIR = 'data/config/locale'
DOMAIN = 'messages'

_ = None

def cheack_os():
    logging.info('Checking the system')
    if platform.system() == "Windows":
        logging.info('The system is recognized as Windows')
        Main_Menu.main_menu()
    else:
        logging.error(f'The system is recognized as {platform.system()}')
        error_os()

def get_system_lang():
    try:
        lang_tuple = locale.getlocale()
        if not lang_tuple[0]:
            lang_code = locale.getdefaultlocale()[0] if hasattr(locale, 'getdefaultlocale') else None
            if not lang_code:
                lang_code = os.environ.get('LANG', 'en_US')
        else:
            lang_code = lang_tuple[0]
            
        if lang_code:
            parts = lang_code.replace('.', '_').split('_')
            lang_part = parts[0].lower()
            
            lang_map = {
                'russian': 'ru',
                'english': 'en',
                'русский': 'ru',
                'английский': 'en',
            }
            
            return lang_map.get(lang_part, lang_part[:2])
        return 'en'
    except Exception as e:
        logging.error(f"Ошибка при определении языка системы: {e}")
        return 'en'

def read_config():
    config_path = os.path.join('data', 'config', 'config.json')
    default_config = {
        "language": "en",
        "auto_language": True,
        "allow_beta": False,
        "auto_download_install": False,
        "auto_download_install": False,
        "version": "1.0.2 beta",
        "last_modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "description": "settings for PowerSetSetup"
    }
    
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                logging.info(f"The configuration file is uploaded: {config_path}")
                return config
        else:
            logging.warning(f"The configuration file was not found. The default settings are used. File ({config_path})")
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=4, ensure_ascii=False)
            logging.info(f"A configuration file with default settings has been created: {config_path}")
            return default_config
    except Exception as e:
        logging.error(f"Error when reading the configuration file: {e}")
        return default_config

def save_config(config):
    config_path = os.path.join('data', 'config', 'config.json')
    try:
        config["last_modified"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        logging.info(f"{log_configuration_file_saved} {config_path}")
        return True
    except Exception as e:
        logging.error(f"{log_error_configuration_file_saved} {e}")
        return False

def setup_localization(lang_code):
    global _
    try:
        translation = gettext.translation(DOMAIN, LOCALE_DIR, languages=[lang_code], fallback=True)
        translation.install()
        _ = translation.gettext
        logging.info(f"The language is set: {lang_code}")
    except Exception as e:
        logging.error(f"Error when setting the language: {lang_code}: {e}")
        _ = gettext.gettext

def apply_language_from_config():
    config = read_config()
    
    if config.get("auto_language", True):
        system_lang = get_system_lang()
        logging.info(f"Automatic language detection: system language = {system_lang}")
        setup_localization(system_lang)
    else:
        saved_lang = config.get("language", "en")
        logging.info(f"{log_saved_language_used} {saved_lang}")
        setup_localization(saved_lang)
    
    return config


def language_setting(new_lang):
    config = read_config()
    config["language"] = new_lang
    config["auto_language"] = False
    if save_config(config):
        logging.info(f"{log_configuration_file_saved}")
    
    setup_localization(new_lang)

config = apply_language_from_config()
current_lang = config.get("language", "en")
setup_localization(current_lang)

id_power_sh_send = "None"

def update_text_variables():
    global lang_addPowerPlanInfo, lang_scheme_warning, lang_fix_update
    global lang_choice, lang_back_main_menu, lang_back_advancedsettings, lang_exit
    global lang_max_performance, lang_performance, lang_balanced, lang_powersave
    global lang_change_language, lang_current_language, lang_select_language
    global lang_russian, lang_english, lang_settings_menu, lang_language_settings
    global lang_menu_title, lang_advancedSettings, lang_autoConfiguration
    global lang_system_show_info, lang_test_pc, lang_check_update_main
    global lang_check_update, lang_info, lang_system_info, lang_settings_saved
    global lang_test_perf, lang_about, lang_author, lang_supportdeveloper
    global lang_version, lang_latest_version, lang_new_release, lang_download_update
    global lang_skip_update, lang_system_latest_version, lang_open_page
    global lang_choice_required_mode, lang_max_power_consumption
    global lang_balans_consumption, lang_low_power, lang_result_before
    global lang_result_after, lang_result, lang_delete_scheme, lang_reset_scheme
    global lang_add_scheme, lang_activate_scheme, lang_list_scheme, lang_manual_input
    global lang_back, lang_balanced_scheme_activated, lang_what_delet_scheme 
    global lang_performance_scheme_activated, lang_settings_timeout_disk
    global lang_max_performance_scheme_activated, lang_beta_update
    global lang_low_power_scheme_activated, lang_settings_menu_scheme
    global lang_enter_id_power_scheme, lang_balanced_scheme_deleted
    global lang_max_power_scheme_added, lang_max_performance_scheme_deleted
    global lang_performance_scheme_deleted, lang_scheme_succesfull_deleted
    global lang_low_power_scheme_deleted, lang_beta_disabled
    global lang_settings_succesfull, lang_successfully, lang_disable_beta
    global lang_minutes, lang_settings_time_sleep, lang_enable_beta
    global lang_settings_timeout_monitor, lang_beta_enabled
    global lang_config_power_plan, lang_beta_settings, lang_auto_language_setting
    global lang_auto_language_enabled, lang_auto_language_disabled, lang_enable_auto_language
    global lang_disable_auto_language, lang_automatic_check_updates, lang_program_closed_install_update
    global lang_run_program_again_install, lang_automatic_check_updates_completed
    
    # errors
    global lang_error_os, lang_error_reset_scheme, lang_error_id_power_scheme, lang_error_timeout_20_minutes, lang_error_input
    global lang_error_timeout_15_minutes, lang_enter_timeout_minutes, lang_error_timeout_0_minutes, lang_error_timeout_10_minutes
    global lang_error_back_main_menu, lang_back_select_delet_scheme, lang_error_add_max_power_scheme, lang_error_low_power_scheme_not_found
    global lang_error_max_performance_scheme_not_found, lang_error_performance_scheme_not_found, lang_error_balanced_scheme_not_found
    global lang_error_check_update, lang_error_automode

    # logs
    global log_select_delete_sh, log_select_add_sh, log_select_activate_sh, log_language_changed, log_configuration_file_uploaded
    global log_exit_program, log_progress, log_select_automode, log_activate_sh, log_create_configuration_file, log_language_set
    global log_configuration_file_saved, log_automatic_language_detection, log_saved_language_used, log_automatic_language_disabled
    global log_automatic_check_updates, log_update_ready_install, log_automatic_update_disabled

    # logs errors
    global log_error_input, log_error_activate_sh, log_error_automode, log_configuration_file_not_found, log_error_language_set
    global log_error_reading_configuration_file, log_error_configuration_file_saved, log_error_executing, log_error_update_module
    global log_error_auto_update_configuration_file, log_error_auto_update
    
    # Определение всех языковых строк lang
    lang_addPowerPlanInfo = _(f'{Fore.RED}WARNING: Available to add: only{Fore.CYAN}"Ultimate Performance"!')
    lang_scheme_warning = _(f"{Fore.RED}WARNING: All other power plans will be deleted after you select one!")
    lang_choice = _("Enter the number: ")
    lang_back_main_menu = _("Back to main menu")
    lang_back_advancedsettings = _("Back to Advanced Settings")
    lang_exit = _("Exit")
    lang_max_performance = _("Maximum performance")
    lang_performance = _("High performance")
    lang_balanced = _("Balanced")
    lang_powersave = _("Power saving")
    lang_change_language = _("Change language")
    lang_current_language = _(f"Current language: {'Русский' if current_lang == 'ru' else 'English'}")
    lang_select_language = _("Select language:")
    lang_russian = _("Русский")
    lang_english = _("English")
    lang_settings_menu = _("Settings")
    lang_language_settings = _("Language settings")
    lang_menu_title = _("Main Menu")
    lang_advancedSettings = _("Advanced settings")
    lang_autoConfiguration = _("Automatic configuration")
    lang_system_show_info = _("Show system information")
    lang_test_pc = _("Performance test")
    lang_check_update_main = _("Check for updates")
    lang_check_update = _("Update check")
    lang_info = _("About")
    lang_system_info = _("System information")
    lang_test_perf = _("Performance test")
    lang_about = _("About")
    lang_author = _("Author: BrocatScript")
    lang_supportdeveloper = _("Support the author")
    lang_version = _("Current version:")
    lang_latest_version = _("Latest version:")
    lang_new_release = _("New version available:")
    lang_download_update = _("Download update")
    lang_skip_update = _("Skip update")
    lang_system_latest_version = _(f"You have the {Fore.GREEN}latest{Fore.RESET} version!")
    lang_open_page = _("Opening the page")
    lang_choice_required_mode = _("Choose the required mode")
    lang_max_power_consumption = _("Maximum power consumption")
    lang_balans_consumption = _("Power consumption balance")
    lang_low_power = _("Lowers battery consumption")
    lang_result_before = _(f"{Fore.CYAN}Result before:")
    lang_result_after = _(f"{Fore.CYAN}Result after:")
    lang_result = _(f"{Fore.CYAN}Result:")
    lang_delete_scheme = _("Delete the scheme")
    lang_reset_scheme = _("Reset the schemes")
    lang_add_scheme = _("Add a scheme")
    lang_activate_scheme = _("Activate the scheme")
    lang_list_scheme = _("List all schemes")
    lang_manual_input = _("Manual input")
    lang_back = _("Go back")
    lang_balanced_scheme_activated = _('Scheme "Balanced" activated!')
    lang_performance_scheme_activated = _('Scheme "High performance" activated!')
    lang_max_performance_scheme_activated = _('Scheme "Maximum performance" activated!')
    lang_low_power_scheme_activated = _('Scheme "Power saving" activated!')
    lang_enter_id_power_scheme = _("Enter the power scheme ID: ")
    lang_max_power_scheme_added = _('Scheme "Maximum Performance" successfully added!')
    lang_what_delet_scheme = _("What do you want to delete?")
    lang_balanced_scheme_deleted = _('Scheme "Balanced" successfully deleted!')
    lang_performance_scheme_deleted = _('Scheme "High performance" successfully deleted!')
    lang_max_performance_scheme_deleted = _('Scheme "Maximum performance" successfully deleted!')
    lang_low_power_scheme_deleted = _('Scheme "Power saving" successfully deleted!')
    lang_scheme_succesfull_deleted = _("Scheme successfully deleted!")
    lang_back_select_delet_scheme = _("Go back to select which scheme to delete?")
    lang_settings_succesfull = _("Changes saved!")
    lang_successfully = _("Operation completed successfully!")
    lang_enter_timeout_minutes = _("Set the display turn‑off time: ")
    lang_minutes = _("minutes")
    lang_settings_menu_scheme = _("Advanced scheme settings")
    lang_settings_timeout_monitor = _("Display off time")
    lang_settings_time_sleep = _("Time to enter sleep mode")
    lang_settings_timeout_disk = _("Hard disk shutdown time")
    lang_config_power_plan = _("Current power supply circuit settings")
    lang_beta_settings = _("Beta Version Settings")
    lang_beta_enabled = _(f"Beta updates {Fore.CYAN}enabled")
    lang_beta_disabled = _(f"Beta updates {Fore.CYAN}disabled")
    lang_enable_beta = _(f"{Fore.CYAN}Enable {Fore.RESET}beta updates")
    lang_disable_beta = _(f"{Fore.CYAN}Disable{Fore.RESET} beta updates")
    lang_settings_saved = _("Settings saved")
    lang_fix_update = _("A fix for the update is available:")
    lang_beta_update = _("Beta update available:")
    lang_auto_language_setting = _("Auto language detection")
    lang_auto_language_enabled = _(f"Auto language detection {Fore.GREEN}enabled")
    lang_auto_language_disabled = _(f"Auto language detection {Fore.RED}disabled")
    lang_enable_auto_language = _(f"{Fore.CYAN}Enable{Fore.RESET} auto language detection")
    lang_disable_auto_language = _(f"{Fore.CYAN}Disable{Fore.RESET} auto language detection")
    lang_automatic_check_updates = _("Automatic check for updates")
    lang_program_closed_install_update = _("The program will be closed to install the update.")
    lang_run_program_again_install = _("Run the program again after installation.")
    lang_automatic_check_updates_completed = _("The automatic update check is completed.")

    # errors
    lang_error_os = _(f"{Fore.RED}YOUR SYSTEM IS NOT WINDOWS, THE PROGRAM IS TERMINATING!")
    lang_error_id_power_scheme = _(f"{Fore.RED}ERROR: Scheme with ID {Fore.WHITE}{id_power_sh_send}{Fore.RED} not found!")
    lang_error_reset_scheme = _("ERROR: couldn't restore schemas to default settings")
    lang_error_timeout_0_minutes = _(f"{Fore.RED}Error: Cannot set {Fore.CYAN}0 minutes!")
    lang_error_timeout_10_minutes = _(f"{Fore.RED}Error: Cannot set {Fore.CYAN}10 minutes!")
    lang_error_timeout_15_minutes = _(f"{Fore.RED}Error: Cannot set {Fore.CYAN}15 minutes!")
    lang_error_timeout_20_minutes = _(f"{Fore.RED}Error: Cannot set {Fore.CYAN}20 minutes!")
    lang_error_back_main_menu = _(f"{Fore.RED}ERROR! You cannot go back because this is the main menu.")
    lang_error_add_max_power_scheme = _(f'{Fore.RED}ERROR: Failed to add the power scheme {Fore.WHITE}"Maximum Performance"!')
    lang_error_low_power_scheme_not_found = _(f"{Fore.RED}Scheme \"Power saving\" not found!")
    lang_error_max_performance_scheme_not_found = _(f'{Fore.RED}ERROR: Scheme "Maximum performance" not found!')
    lang_error_performance_scheme_not_found = _(f'{Fore.RED}ERROR: Scheme "High performance" not found!')
    lang_error_balanced_scheme_not_found = _(f'{Fore.RED}ERROR: Scheme "Balanced" not found!')
    lang_error_check_update = _(f"{Fore.RED}ERROR: Update check failed!")
    lang_error_input = _(f"{Fore.RED}ERROR: The message is written incorrectly or it is empty! {Fore.WHITE}Try again!")
    lang_error_automode = _(f"{Fore.RED}ERROR: An error occurred during the automatic configuration!")
    
    # logs
    log_language_changed = _("Language changed to")
    log_exit_program = _("Completion of the program...")
    log_select_delete_sh = _("Selected: deleting the scheme")
    log_select_add_sh = _("Selected: add the scheme")
    log_select_activate_sh = _("Selected: activate the scheme")
    log_activate_sh = _("The scheme has been successfully activated. Activated scheme:")
    log_select_automode = _("In the automatic menu, the following was selected:")
    log_progress = _("In progress:")
    log_configuration_file_uploaded = _("The configuration file is uploaded:")
    log_create_configuration_file = _("A configuration file with default settings has been created:")
    log_configuration_file_saved = _("The configuration file is saved:")
    log_language_set = _("The language is set:")
    log_automatic_language_detection = _("Automatic language detection: system language =")
    log_saved_language_used = _("The saved language is used:")
    log_automatic_language_disabled = _("Automatic language verification is disabled")
    log_automatic_update_disabled = _("Automatic update checking is disabled")
    log_automatic_check_updates = _("Launching an automatic update check")
    log_update_ready_install = _("The update has been downloaded and is ready for installation. Completion of the program...")

    # logs errors
    log_error_input = _("Input error in")
    log_error_activate_sh = _("A critical error occurred when activating the scheme:")
    log_error_automode = _("An error occurred during the automatic configuration:")
    log_configuration_file_not_found = _("The configuration file was not found. The default settings are used.")
    log_error_reading_configuration_file = _("Error when reading the configuration file:")
    log_error_configuration_file_saved = _("Error saving the configuration file:")
    log_error_language_set = _("Error when setting the language:")
    log_error_executing = _("Error when executing")
    log_error_update_module = _("The update verification module is unavailable")
    log_error_auto_update_configuration_file = _("Couldn't download the configuration to check for updates")
    log_error_auto_update = _("Error when checking for updates automatically:")

# update text
update_text_variables()

def error_os():
    try:
        print(lang_error_os)
        sys.exit(2)
    except Exception as e:
        logging.error(f"Critical error in error_os: {e}, uninstall program please!")
        print(f"{Fore.RED}Critical error in error_os: {e}")
        sys.exit(1)

def powercfg_list():
    if platform.system() == 'Windows':
        os.system('powercfg /l')
    else:
        error_os()

def get_powercfg_list():
    if platform.system() == 'Windows':
        try:
            result = subprocess.run(
                ['powercfg', '/l'],
                capture_output=True,
                text=True,
                encoding='utf-8',
                shell=True
            )
            return result.stdout
        except Exception as e:
            logging.error(f"{log_error_executing} get powercfg /list ({e})")
            return ""
    else:
        error_os()
        return ""

def powercfg_geta_sh():
    if platform.system() == 'Windows':
        try:
            subprocess.run(
                ['powercfg', '/getactivescheme'],
                shell=True,
                capture_output=True,
                encoding='utf-8',
                check=True)
        except Exception as e:
            logging.error(f"{log_error_executing} powercfg /getactivescheme: ({e})")
    else:
        error_os()

def run_auto_update_check():
    if not UPDATE_CHECKER_AVAILABLE:
        logging.warning({log_error_update_module})
        return False
    
    try:
        config = read_config()
        check_on_startup = config.get("check_on_startup", False)
        
        if not check_on_startup:
            logging.debug(log_automatic_update_disabled)
            return False
        
        logging.info(log_automatic_check_updates)
        print(Fore.YELLOW + lang_automatic_check_updates)

        
        update_config = load_update_config()
        if not update_config:
            logging.error(log_error_auto_update_configuration_file)
            return False
        
        # Запускаем проверку обновлений (show_prompt=False для авто-проверки)
        need_exit = check_for_updates(
            update_config, 
            auto_start_check=True, 
            show_prompt=False
        )
        
        if need_exit:
            logging.info(log_update_ready_install)
            print(lang_check_update)
            print(f"\n{lang_program_closed_install_update}")
            print(lang_run_program_again_install)
            sleep(3)
            return True
        else:
            print(f"\n{lang_automatic_check_updates_completed}")
            sleep(2)
            return False
            
    except Exception as e:
        logging.error(f"{log_error_auto_update} ({e})")
        print(f"{lang_error_check_update}: {e}")
        sleep(2)
        return False

def manual_check_update():
    if not UPDATE_CHECKER_AVAILABLE:
        print(log_error_update_module)
        sleep(2)
        Main_Menu.main_menu()
        return
    
    try:
        update_config = load_update_config()
        if not update_config:
            print(log_error_reading_configuration_file)
            sleep(2)
            Main_Menu.main_menu()
            return
        
        # Запускаем проверку обновлений (show_prompt=True для ручной проверки)
        need_exit = check_for_updates(
            update_config, 
            auto_start_check=True, 
            show_prompt=True
        )
        
        if need_exit:
            print(lang_check_update)
            print(f"\n{lang_program_closed_install_update}")
            print(Fore.GREEN + "Запустите программу снова после установки.")
            sys.exit(3)
        else:
            print(Fore.GREEN + "\nПроверка обновлений завершена.")
            sleep(2)
            Main_Menu.main_menu()
            
    except Exception as e:
        print(Fore.RED + f"Ошибка при проверке обновлений: {e}")
        logging.error(f"Ошибка при проверке обновлений: {e}")
        sleep(2)
        Main_Menu.main_menu()

# Main menu program
class Main_Menu:
    def main_menu():
        logging.info("Переход в главное меню")
        while True:
            update_text_variables()
            clear()
            powercfg_list()
            print()
            print(lang_menu_title)
            print(f"\n1. {lang_autoConfiguration}")
            print("2.", lang_advancedSettings)
            print("3.", lang_check_update_main)
            print("4.", lang_supportdeveloper)
            print("5.", lang_settings_menu)
            print("9.", lang_back)
            print("0.", lang_exit)
            
            main_menu = input(lang_choice).lower()
            if main_menu == "1":
                logging.info("Переход в автоматические настройки через главное меню")
                automode_menu()
                break
            elif main_menu == "2":
                logging.info("Переход в расширенные настройки через главное меню")
                advancedSettings()
                break
            elif main_menu == "3":
                logging.info("Ручная проверка обновлений через главное меню")
                manual_check_update()
                break
            elif main_menu == "4":
                logging.info("Поддержка разработчика через главное меню")
                support_developer()
                break
            elif main_menu == "5":
                logging.info("Переход в настройки через главное меню")
                settings_menu()
                break
            elif main_menu in ["0", "exit", "end", "e"]:
                end()
                break
            elif main_menu in ["ru", "r", "ру", "р"]:
                language_setting('ru')
            elif main_menu == "en":
                language_setting('en')
            else:
                clear()
                logging.error('Неверный ввод или сообщение было написано с ошибкой (Главное меню)')
                print(lang_error_input)
                sleep(1)

def advancedSettings():
    logging.debug('Переход в расширенные параметры электропитания')
    while True:
        clear()
        powercfg_list()
        print('\nРасширенные параметры')
        print(f'\n1. {lang_delete_scheme}')
        print(f'2. {lang_reset_scheme}')
        print(f'3. {lang_add_scheme}')
        print(f'4. {lang_activate_scheme}')
        print(f'5. {lang_list_scheme}')
        print(f'9. {lang_back_main_menu}')
        print(f'0. {lang_exit}')

        advancedSettings = input(lang_choice)
        if advancedSettings == "1":
            logging.info('Переход в удаление схем через расширенные настройки')
            delete_scheme()
            break
        elif advancedSettings == "2":
            logging.info('Переход в функциию сброса схем через расширенные настройки')
            reset_scheme()
            break
        elif advancedSettings == "3":
            logging.info('Переход в добавление схем через расширенные настройки')
            add_scheme()
            break
        elif advancedSettings == "4":
            logging.info('Переход в активирование схем через расширенные настройки')
            activate_scheme()
            break
        elif advancedSettings == "5":
            logging.info('Переход в функцию просмотра всех схем')
            list_scheme()
            break
        elif advancedSettings in ["9", "back", "b"]:
            logging.info('Переход в главное меню через расширенные настройки')
            Main_Menu.main_menu()
            break
        elif advancedSettings in ["0", "exit", "end", "e"]:
            logging.info('Выход из приложения через расширенные настройки')
            end()
            break
        else:
            clear()
            logging.error('Неверный ввод или сообщение было написано с ошибкой (Расширенные настройки)')
            print(lang_error_input)
            sleep(1)

def delete_scheme():
    logging.debug('Переход в удаление схем')
    while True:
        clear()
        powercfg_list()
        print(f"\n{lang_what_delet_scheme}")
        print(f'\n1. {lang_balanced}')
        print(f'2. {lang_performance}')
        print(f'3. {lang_max_performance}')
        print(f'4. {lang_powersave}')
        print(f'5. {lang_manual_input}')
        print(f'0. {lang_exit}')

        delete_scheme = input(lang_choice)
        if delete_scheme == "1":
            logging.info(f'{log_select_delete_sh} "{lang_balanced}"')
            delete_balanced_scheme()
            break
        elif delete_scheme == "2":
            logging.info(f'{log_select_delete_sh} "{lang_performance}"')
            delete_performance_scheme()
            break
        elif delete_scheme == "3":
            logging.info(f'{log_select_delete_sh} "{lang_max_performance}"')
            delete_max_performance_scheme()
            break
        elif delete_scheme == "4":
            logging.info(f'{log_select_delete_sh} "{lang_powersave}"')
            delete_powersave_scheme()
            break
        elif delete_scheme == "5":
            logging.info(f'{log_select_delete_sh} "{lang_manual_input}"')
            delete_manual_input_scheme()
            break
        elif delete_scheme == "0":
            logging.info(f'{log_select_delete_sh} "{lang_exit}"')
            end()
            break
        else:
            logging.error('Неверный ввод или сообщение было написано с ошибкой (Удаление схем)')
            print(lang_error_input)
            sleep(1)

def delete_balanced_scheme():
    logging.debug(f'Переход в удаление схемы {lang_balanced}')
    clear()
    print(".")
    cmd = [
        "powercfg", "-delete", "381b4222-f694-41f0-9685-ff5bb260df2e"
    ]

    try:
        clear()
        print("..")
        subprocess.run(cmd,
                    shell=True,
                    capture_output=True, 
                    text=True,
                    encoding="utf-8",
                    check=True)
        print("...")
        clear()
        print(lang_balanced_scheme_deleted)
    except subprocess.CalledProcessError as e:
        clear()
        logging.error(f'Ошибка удаления схемы {lang_balanced} ошибка: {e} команда {cmd}')
        print(f'{lang_error_balanced_scheme_not_found}')
    sleep(2)
    delete_scheme()

def delete_performance_scheme():
    logging.debug(f'Переход в удаление схемы {lang_performance}')
    clear()
    print(".")
    cmd = [
        "powercfg", "-delete", "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
    ]

    try:
        clear()
        print("..")
        subprocess.run(cmd,
                    shell=True,
                    capture_output=True, 
                    text=True,
                    encoding="utf-8",
                    check=True)
        print("...")
        clear()
        print(lang_performance_scheme_deleted)
    except subprocess.CalledProcessError as e:
        clear()
        logging.error(f'Ошибка удаления схемы {lang_performance} ошибка: {e} команда {cmd}')
        print(f'{lang_error_performance_scheme_not_found}')
    sleep(2)
    delete_scheme()

def delete_max_performance_scheme():
    logging.debug(f'Переход в удаление схемы {lang_max_performance}')
    clear()
    print(".")
    cmd = [
        "powercfg", "-delete", "a1234567-b000-c000-d000-e70707070707"
    ]

    try:
        clear()
        print("..")
        subprocess.run(cmd,
                    shell=True,
                    capture_output=True, 
                    text=True,
                    encoding="utf-8",
                    check=True)
        print("...")
        clear()
        print(lang_max_performance_scheme_deleted)
    except subprocess.CalledProcessError as e:
        clear()
        logging.error(f'Ошибка удаления схемы {lang_max_performance} ошибка: {e} команда {cmd}')
        print(f'{lang_error_max_performance_scheme_not_found}')
    sleep(2)
    delete_scheme()

def delete_powersave_scheme():
    logging.debug(f'Переход в удаление схемы {lang_powersave}')
    clear()
    print(".")
    cmd = [
        "powercfg", "-delete", "a1841308-3541-4fab-bc81-f71556f20b4a"
    ]

    try:
        clear()
        print("..")
        subprocess.run(cmd,
                    shell=True,
                    capture_output=True, 
                    text=True,
                    encoding="utf-8",
                    check=True)
        print("...")
        clear()
        print(lang_low_power_scheme_deleted)
    except subprocess.CalledProcessError as e:
        clear()
        logging.error(f'Ошибка удаления схемы {lang_powersave} ошибка: {e} команда {cmd}')
        print(f'{lang_error_low_power_scheme_not_found}')
    sleep(2)
    delete_scheme()

def delete_manual_input_scheme():
    logging.debug(f'Переход в удаление схемы {lang_manual_input}')
    clear()
    powercfg_list()
    id_power_sh_send = input(f"\n{lang_enter_id_power_scheme}").lower()
    if id_power_sh_send == "back":
        advancedSettings()
    elif id_power_sh_send == "b":
        advancedSettings()
    elif id_power_sh_send == "exit":
        end()
    elif id_power_sh_send == "end":
        end()
    elif id_power_sh_send == "e":
        end()
    clear()
    print(".")
    cmd = [
        "powercfg", "-delete", f"{id_power_sh_send}"
    ]

    try:
        clear()
        print("..")
        subprocess.run(cmd,
                    shell=True,
                    capture_output=True, 
                    text=True,
                    encoding="utf-8",
                    check=True)
        clear()
        print("...")
        logging.info(f'{lang_scheme_succesfull_deleted} id = {id_power_sh_send}')
        clear()
        print(lang_scheme_succesfull_deleted)
    except subprocess.CalledProcessError as e:
        clear()
        logging.error(f'Ошибка удаления схемы {id_power_sh_send} ошибка: {e} команда {cmd}')
        print(f'{lang_error_id_power_scheme}')
    sleep(2)
    delete_scheme()

def reset_scheme():
    logging.debug(f'Переход в сброс схем')
    clear()
    print(".")

    scheme_before = get_powercfg_list()
    cmd = [
        "powercfg", "-restoredefaultschemes"
    ]

    try:
        clear()
        print("..")
        subprocess.run(cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    check=True)
        clear()
        print("...")
        logging.info(f'Успешно {lang_reset_scheme}')
        clear()
        print(lang_result_before)
        print(f'{scheme_before}')
        print(f"\n\n{lang_result_after}")
        powercfg_list()
        os.system('pause')
    except subprocess.CalledProcessError as e:
        clear()
        logging.error(f'Ошибка сброса схем {e} в {cmd}')
        print(lang_error_reset_scheme)
    advancedSettings()

def add_scheme():
    while True:
        clear()
        powercfg_list()
        print(f"\n{lang_addPowerPlanInfo}")
        print(f"1. {lang_max_performance}")
        print(f"8. {lang_back_main_menu}")
        print(f"9. {lang_back_advancedsettings}")
        print(f"0. {lang_exit}")

        add_scheme = input(lang_choice)
        if add_scheme == "1":
            add_scheme_max_perfomance()
            break
        elif add_scheme in ["8", "main", "m"]:
            Main_Menu.main_menu()
            break
        elif add_scheme in ["9", "back", "b"]:
            advancedSettings()
            break
        elif add_scheme in ["0", "exit", "end", "e"]:
            end()
            break
        else:
            clear()
            logging.error(f"{log_error_input} ({lang_advancedSettings})")
            print(lang_error_input)
            sleep(2)

def add_scheme_max_perfomance():
    clear()
    print(".")
    cmd = [
        "powercfg", "-duplicatescheme", "e9a42b02-d5df-448d-aa00-03f14749eb61", "a1234567-b000-c000-d000-e70707070707"
    ]

    try:
        clear()
        print("..")
        subprocess.run(cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    check=True)
        clear()
        print("...")
        logging.info(f'{log_add_sh} "{lang_max_performance}"')
        clear()
        print(lang_max_power_scheme_added)
    except subprocess.CalledProcessError as e:
        clear()
        logging.error(f'{log_error_add_sh} {lang_max_performance} ({e}) [{cmd}]')
        print(lang_error_add_max_power_scheme)
    sleep(2)
    advancedSettings()



def activate_scheme():
    while True:
        clear()
        powercfg_list()
        print(f"\n1. {lang_balanced}")
        print(f"2. {lang_performance}")
        print(f"3. {lang_max_performance}")
        print(f"4. {lang_powersave}")
        print(f"5. {lang_manual_input}")
        print(f"9. {lang_back_main_menu}")
        print(f"0. {lang_exit}")

        activate_scheme = input(lang_choice).lower()
        if activate_scheme == "1":
            activate_scheme_balanced()
            break
        elif activate_scheme == "2":
            activate_scheme_perfomance()
            break
        elif activate_scheme == "3":
            activate_scheme_max_perfomance()
            break
        elif activate_scheme == "4":
            activate_scheme_powersave()
            break
        elif activate_scheme == "5":
            activate_scheme_manual_input()
            break
        elif activate_scheme in ["9", "back", "b"]:
            Main_Menu.main_menu()
            break
        elif activate_scheme in ["0", "exit", "end", "e"]:
            end()
            break
        else:
            clear()
            logging.error(f"{log_error_input} ({lang_activate_scheme})")
            print(lang_error_input)
            sleep(1)

def activate_scheme_balanced():
    clear()
    print(".")
    cmd = [
        "powercfg", "/setactive", "381b4222-f694-41f0-9685-ff5bb260df2e"
    ]

    try:
        clear()
        print("..")
        subprocess.run(cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    check=True)
        clear()
        print("...")
        logging.info(f'{log_activate_sh} {lang_balanced}')
        clear()
        print(lang_balanced_scheme_activated)
    except subprocess.CalledProcessError as e:
        clear()
        logging.error(f'{log_error_activate_sh} {lang_balanced} ({e}) [{cmd}]')
        print(lang_error_balanced_scheme_not_found)
    sleep(1)
    advancedSettings()

def activate_scheme_perfomance():
    clear()
    print(".")
    cmd = [
        "powercfg", "/setactive", "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
    ]

    try:
        clear()
        print("..")
        subprocess.run(cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    check=True)
        clear()
        print("...")
        logging.info(f'{log_activate_sh} {lang_performance}')
        clear()
        print(lang_performance_scheme_activated)
    except subprocess.CalledProcessError as e:
        clear()
        logging.error(f'{log_error_activate_sh} {lang_performance} ({e}) [{cmd}]')
        print(lang_error_performance_scheme_not_found)
    sleep(1)
    advancedSettings()

def activate_scheme_max_perfomance():
    clear()
    print(".")
    cmd = [
        "powercfg", "/setactive", "a1234567-b000-c000-d000-e70707070707"
    ]

    try:
        clear()
        print("..")
        subprocess.run(cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    check=True)
        clear()
        print("...")
        logging.info(f'{log_activate_sh} {lang_max_performance}')
        clear()
        print(lang_max_performance_scheme_activated)
    except subprocess.CalledProcessError as e:
        clear()
        logging.error(f'{log_error_activate_sh} {lang_max_performance} ({e}) [{cmd}]')
        print(lang_error_max_performance_scheme_not_found)
    sleep(1)
    advancedSettings()

def activate_scheme_powersave():
    clear()
    print(".")
    cmd = [
        "powercfg", "/setactive", "a1841308-3541-4fab-bc81-f71556f20b4a"
    ]

    try:
        clear()
        print("..")
        subprocess.run(cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    check=True)
        clear()
        print("...")
        logging.info(f'{log_activate_sh} {lang_powersave}')
        clear()
        print(lang_max_performance_scheme_activated)
    except subprocess.CalledProcessError as e:
        clear()
        logging.error(f'{log_error_activate_sh} {lang_powersave} ({e}) [{cmd}]')
        print(lang_error_low_power_scheme_not_found)
    sleep(1)
    advancedSettings()

def activate_scheme_manual_input():
    clear()
    powercfg_list()
    id_power_sh_send = input(f"\n{lang_enter_id_power_scheme}").lower()
    if id_power_sh_send in ["back", "b", "", " "]:
        advancedSettings()
    elif id_power_sh_send in ["exit", "end", "e"]:
        advancedSettings()
    clear()
    print(".")
    cmd = [
        "powercfg", "/setactive", f"{id_power_sh_send}"
    ]

    try:
        clear()
        print("..")
        subprocess.run(cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    check=True)
        clear()
        print("...")
        logging.info(f'{log_activate_sh} {lang_manual_input}')
        clear()
        print(lang_max_performance_scheme_activated)
    except subprocess.CalledProcessError as e:
        clear()
        logging.error(f'{log_error_activate_sh} {id_power_sh_send} ({e}) [{cmd}]')
        print(lang_error_id_power_scheme)
    sleep(1)
    advancedSettings()

def list_scheme():
    logging.debug('Переход в просмотр схем')
    clear()
    powercfg_list()
    os.system('pause')
    advancedSettings()

def support_developer():
    logging.debug("Переход в поддержку разработчика")
    if current_lang == "ru":
        url = "https://pay.cloudtips.ru/p/0cdee068"
    elif current_lang == "en":
        url = "https://badgen.net/badge/%D1%81%D1%81%D1%8B%D0%BB%D0%BA%D0%B0/%D0%B2%20%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B5/red"
    else:
        url = "для вас нет ссылки"
    open_url_support_developer(url)

def open_url_support_developer(url):
    clear()
    print("Спасибо за поддержку!")
    print(f"\n{lang_open_page}")
    try:
        webbrowser.open(url)
        logging.info(f'Ссылка поддержки автора открыта: {url}')
        print(f'Cсылка открыта, если вам удобен другой сервис, то нажмите 2')
    except Exception as e:
        logging.error(f"Не удалось открыть ссылку, ошибка {e}")
        print(f"Не удалось открыть ссылку, ошибка {e}")
    support_developer = input("Нажмите enter чтобы продолжить")
    if support_developer == "2":
        url = "ссылка разрабатывается!"
        open_url_support_developer(url)
    elif support_developer == "1":
        url = "https://pay.cloudtips.ru/p/0cdee068"
        open_url_support_developer(url)
    else:
        Main_Menu.main_menu()

def settings_menu():
    logging.debug("Переход в меню настроек")
    while True:
        clear()
        update_text_variables()
        print(lang_settings_menu)
        print(f"\n1. {lang_language_settings}")
        print("2.", lang_settings_menu_scheme)
        print("3.", lang_beta_settings)
        print("4.", lang_back)
        print("5.", lang_exit)

        settings_menu = input(lang_choice).lower()
        if settings_menu in ["1", "lang", "l"]:
            language_settings()
            break
        elif settings_menu == "2":
            clear()
            logging.error("Эта функция недоступна, потому что может навредить вашему компьютеру! Она не готова!")
            print("ERROR: It is beta test!!!")
            print("Ошибка: Это тестовая версия!!!")
            sleep(2)
        elif settings_menu in ["3", "beta"]:
            beta_settings()
            break
        elif settings_menu in ["4", "9", "back", "b"]:
            Main_Menu.main_menu()
            break
        elif settings_menu in ["5", "0", "exit", "end", "e"]:
            end()
            break
        elif settings_menu in ["ru", "r", "ру", "р"]:
            language_setting('ru')
        elif settings_menu == "en":
            language_setting('en')
        else:
            clear()
            print(lang_error_input)
            sleep(1)

def setting_menu_scheme():
    while True:
        clear()
        print(f"{lang_settings_menu_scheme}\n")
        print(lang_config_power_plan)
        powercfg_geta_sh()
        print(f"\n1. {lang_settings_timeout_monitor}")
        print("2.", lang_settings_time_sleep)
        print("3.", lang_settings_timeout_disk)
        print("4.", lang_settings_hibernate)
        print("5.", lang_send_othet) # /A = Отчет о доступных в системе состояниях спящего режима.
        print("6.", lang_next)

def setting_menu_scheme_page2():
    while True:
        clear()
        print(f"{lang_settings_menu_scheme}\n")
        print(lang_config_power_plan)
        powercfg_geta_sh()
        print(f"\n1. {lang_}")
        print("2.", lang_)
        print("3.", lang_battery_report) # /BATTERYREPORT
        print("4.", lang_settings_hibernate) # powercfg /systempowerreport
        print("5.", lang_send_othet) # /A = Отчет о доступных в системе состояниях спящего режима.
        print("6.", lang_next)



def language_settings():
    logging.debug("Переход в меню настроек выбора языка")
    while True:
        clear()
        config = read_config()
        auto_language = config.get("auto_language", True)
        current_lang = config.get("language", "en")
        update_text_variables()

        lang_display = "Русский" if current_lang == "ru" else "English"
        auto_status = f"{Fore.GREEN}ON" if auto_language else f"{Fore.RED}OFF"

        print(f"{lang_current_language}: {lang_display}")
        print(f"{lang_auto_language_setting}: {auto_status}")
        print(f"\n{lang_select_language}")
        print(f"1. {lang_russian}")
        print("2.", lang_english)
        print(f"3. {lang_enable_auto_language if not auto_language else lang_disable_auto_language}")
        print("4.", lang_back)
        print("5.", lang_exit)
        select_language = input(lang_choice).lower()
        if select_language in ["1", "ru", "r", "ру", "р"]:
            language_setting('ru')
            update_text_variables()
            logging.info(f"{log_language_changed} Русский")
        elif select_language in ["2", "en", "e"]:
            language_setting('en')
            update_text_variables()
            logging.info(f"{log_language_changed} English")
        elif select_language in ["3", "auto", "a"]:
            config = read_config()
            config["auto_language"] = not config.get("auto_language", True)
            
            if config["auto_language"]:
                system_lang = get_system_lang()
                config["language"] = system_lang
                save_config(config)
                setup_localization(system_lang)
                update_text_variables()
                clear()
                print(lang_auto_language_enabled)
                logging.info(f"Автоопределение языка включено, системный язык: {system_lang}")
            else:
                save_config(config)
                current_lang = config.get("language", "en")
                setup_localization(current_lang)
                update_text_variables()
                clear()
                print(lang_auto_language_disabled)
                logging.info("Автоопределение языка отключено")
            sleep(1)
        elif select_language in ["4", "9", "back", "b"]:
            settings_menu()
            break
        elif select_language in ["0", "5", "exit", "end", "e"]:
            end()
            break
        else:
            clear()
            logging.error(f"{log_error_input} {lang_language_settings}")
            print(lang_error_input)
            sleep(1)

def beta_settings():
    while True:
        clear()
        config = read_config()
        allow_beta = config.get("allow_beta", True)
        print(lang_beta_settings)
        if allow_beta:
            print(f"\n1. {lang_disable_beta}")
        else:
            print(f"\n1. {lang_enable_beta}")
        print(f"2. {lang_back}")
        print(f"3. {lang_exit}")
    
        beta_settings = input(lang_choice).lower()
        if beta_settings == "1":
            config = read_config()
            config["allow_beta"] = not config.get("allow_beta", True)
            if save_config(config):
                if config["allow_beta"]:
                    clear()
                    print(lang_beta_enabled)
                else:
                    clear()
                    print(lang_beta_disabled)
            sleep(1)
        elif beta_settings in ["9", "2", "back", "b"]:
            settings_menu()
            break
        elif beta_settings in ["0", "3", "exit", "end", "e"]:
            end()
            break
        else:
            clear()
            logging.error(f"{log_error_input} {lang_beta_settings}")
            print(lang_error_input)
            sleep(1)

def end():
    clear()
    print("=]")
    logging.info(f"{log_exit_program}")
    sys.exit(0)

def automode_menu():
    logging.info("Переход в меню автоматической настройки")
    while True:
        clear()
        print(f"{lang_scheme_warning}")
        print(f"\n{lang_choice_required_mode}")
        print(f"1. {lang_max_performance} ({lang_max_power_consumption})")
        print(f"2. {lang_balanced} ({lang_balans_consumption})")
        print(f"3. {lang_powersave} ({lang_low_power})")
        print(f"4. {lang_back_main_menu}")
        print(f"5. {lang_exit}")
        
        automode = input(lang_choice).lower()
        if automode == "1":
            logging.info(f"{log_select_automode} {lang_max_performance}")
            automode1()
            break
        elif automode == "2":
            logging.info(f"{log_select_automode} {lang_balanced}")
            automode2()
            break
        elif automode == "3":
            logging.info(f"{log_select_automode} {lang_powersave}")
            automode3()
            break
        elif automode in ["9", "4", "back", "b"]:
            logging.info("Возврат в главное меню")
            Main_Menu.main_menu()
            break
        elif automode in ["0", "5", "exit", "end", "e"]:
            end()
            break
        else:
            logging.error(f"{log_error_input} {lang_autoConfiguration}")
            print(f"{lang_error_input}")
            sleep(1)

def automode1():
    logging.info("Настройка максимальной производительности")
    clear()
    print(".")

    scheme_before = get_powercfg_list()
    commands = [
        ["powercfg", "-restoredefaultschemes"],
        ["powercfg", "-duplicatescheme", "e9a42b02-d5df-448d-aa00-03f14749eb61", "a1234567-b000-c000-d000-e70707070707"],
        ["powercfg", "/setactive", "a1234567-b000-c000-d000-e70707070707"],
        ["powercfg", "-delete", "a1841308-3541-4fab-bc81-f71556f20b4a"],
        ["powercfg", "-delete", "381b4222-f694-41f0-9685-ff5bb260df2e"],
        ["powercfg", "-delete", "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"]
    ]
    
    for cmd in commands:
        try:
            clear()
            print("..")
            logging.debug(f"{log_progress} {' '.join(cmd)}")
            subprocess.run(cmd,
                        shell=True,
                        capture_output=True, 
                        text=True,
                        encoding="utf-8",
                        check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"{log_error_automode} ({e}) [{cmd}]")
            print(f"{Fore.RED}{lang_error_automode}")
    
    clear()
    print("...")
    clear()
    print(lang_result_before)
    print(scheme_before)
    print(f"\n{lang_result_after}")
    powercfg_list()
    os.system('pause')
    automode1_end_menu()

def automode1_end_menu():
    while True:
        clear()
        powercfg_list()
        print(f"\n1. {lang_back_main_menu}")
        print(f"2. {lang_exit}")

        autoend1 = input(lang_choice).lower()
        if autoend1 in ["1", "9", "back", "b"]:
            Main_Menu.main_menu()
            break
        elif autoend1 in ["2", "0", "exit", "end", "e"]:
            end()
            break
        else:
            logging.error(f"{log_error_input} {lang_autoConfiguration} {lang_max_performance}")
            print(f"{lang_error_input}")
            sleep(1)

def automode2():
    logging.info("Настройка сбалансированного режима")
    clear()
    print(".")
    
    scheme_before = get_powercfg_list()
    commands = [
        ["powercfg", "-restoredefaultschemes"],
        ["powercfg", "/setactive", "381b4222-f694-41f0-9685-ff5bb260df2e"],
        ["powercfg", "-delete", "a1841308-3541-4fab-bc81-f71556f20b4a"],
        ["powercfg", "-delete", "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635ca"]
    ]
    
    for cmd in commands:
        try:
            clear()
            print("..")
            logging.debug(f"{log_progress} {' '.join(cmd)}")
            subprocess.run(cmd,
                        shell=True,
                        capture_output=True, 
                        text=True,
                        encoding="utf-8",
                        check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"{log_error_automode} {cmd}: {e}")
            clear()
            print(f"{Fore.RED}{lang_error_automode}")
    clear()
    print("...")
    clear()
    print(lang_result_before)
    print(scheme_before)
    print(f"\n{lang_result_after}")
    powercfg_list()
    automode2_end_menu()

def automode2_end_menu():
    while True:
        clear()
        powercfg_list()
        print(f"\n1. {lang_back_main_menu}")
        print(f"2. {lang_exit}")

        autoend2 = input(lang_choice).lower()
        if autoend2 in ["1", "9", "back", "b"]:
            Main_Menu.main_menu()
            break
        elif autoend2 in ["2", "0", "exit", "end", "e"]:
            end()
            break
        else:
            logging.error(f"{log_error_input} {lang_autoConfiguration} {lang_balanced}")
            print(f"{lang_error_input}")
            sleep(1)

def automode3():
    logging.info("Настройка режима энергосбережения")
    clear()
    print(".")
    
    scheme_before = get_powercfg_list()
    commands = [
        ["powercfg", "-restoredefaultschemes"],
        ["powercfg", "/setactive", "a1841308-3541-4fab-bc81-f71556f20b4a"],
        ["powercfg", "-delete", "381b4222-f694-41f0-9685-ff5bb260df2e"],
        ["powercfg", "-delete", "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"]
    ]
    
    for cmd in commands:
        try:
            clear()
            print("..")
            logging.debug(f"{log_progress} {' '.join(cmd)}")
            subprocess.run(cmd,
                        shell=True,
                        capture_output=True, 
                        text=True,
                        encoding="utf-8",
                        check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"{log_error_automode} {cmd}: {e}")
            print(f"{Fore.RED}{lang_error_automode}")
    
    clear()
    print("...")
    clear()
    print(lang_result_before)
    print(scheme_before)
    print(f"\n{lang_result_after}")
    powercfg_list()
    automode3_end_menu()

def automode3_end_menu():
    while True:
        clear()
        powercfg_list()
        print(f"\n1. {lang_back_main_menu}")
        print(f"2. {lang_exit}")

        autoend3 = input(lang_choice).lower()
        if autoend3 in ["1", "9", "back", "b"]:
            Main_Menu.main_menu()
            break
        elif autoend3 in ["2","0", "exit", "end", "e"]:
            end()
            break
        else:
            logging.error(f"{log_error_input} {lang_autoConfiguration} {lang_powersave}")
            print(f"{lang_error_input}")
            sleep(1)

if __name__ == "__main__":
    config = apply_language_from_config()

    need_exit = run_auto_update_check()
    
    if need_exit:
        sys.exit(0)
    else:
        cheack_os()