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
import re
import shutil
from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import urlparse
import requests

sleep = time.sleep

Name_Program = "PowerSetSetup"

APP_VERSION = "1.02.0"        # формат A.BB.C
BUILD_CHANNEL = "stable"      # "stable" | "beta" | "demo"
IS_PORTABLE = False           # True - в портативной сборке (обновление скачивается архивом)
version = f"{APP_VERSION} {BUILD_CHANNEL}"   # для лога

MANIFEST_URL = "https://raw.githubusercontent.com/BrocatScript/PowerSetSetup/main/version_test.json"
WINGET_ID = "BrocatScript.PowerSetSetup"     # TODO: реальный Id пакета из winget-pkgs
ALLOWED_URL_PREFIX = "https://github.com/BrocatScript/"   # скачивать и открывать можно только отсюда

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "logs.txt")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    level=logging.INFO, # DEBUG for detailed logs, INFO for general information
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, mode='w', encoding='utf-8'),
        # logging.StreamHandler()  # Вывод в консоль
    ]
)

loading1 = "| "
loading2 = "/ "
loading3 = "\\ "

logger = logging.getLogger()
logging.info(f"--- {Name_Program} {version} ---")

logging.debug("Launching UTF-8 encoding")
os.system('chcp 65001 > nul')

def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        error_os()

init(autoreset=True)

# Локализация
LOCALE_DIR = 'data/config/locale'
DOMAIN = 'messages'

_ = None
current_lang = 'en'

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

_CONFIG_CACHE = None

CONFIG_DEFAULTS = {
    "include_beta": False,        # бывший allow_beta: учитывать ли beta-версии при проверке
    "portable_choice": None,      # запомненный формат архива для portable, например ".zip"
    "portable_remember": False,   # галка «Запомнить выбор»
    "update_method": None,       # "winget" или "github" — запомненный способ обновления
    "update_method_remember": False, # запоминать ли способ обновления
    "update_required": False,     # пропущено обязательное обновление
    "mandatory_version": None,    # какая именно версия обязательная (чтобы флаг гас после установки)
}

def migrate_config(cfg):
    """Дополняет старый config.json новыми ключами. True, если что-то изменилось."""
    changed = False
    if "allow_beta" in cfg:
        old = bool(cfg.pop("allow_beta"))
        cfg.setdefault("include_beta", old)
        changed = True
    
    for key, value in CONFIG_DEFAULTS.items():
        if key not in cfg:
            cfg[key] = value
            changed = True
    return changed

def load_config(force_reload=False):
    global _CONFIG_CACHE
    global BUILD_CHANNEL
    if _CONFIG_CACHE is not None and not force_reload:
        return _CONFIG_CACHE
    config_path = os.path.join('data', 'config', 'config.json')
    default_config = {
        "language": None,
        "auto_language": True,
        "include_beta": False,
        "auto_download_install": False,
        "update_required": False,
        "build": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), # не используется
        "last_modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "portable_choice": None,
        "portable_remember": False,
        "mandatory_version": None,
        "update_method": None,
        "update_method_remember": False,
        "emotes_support": False, # новый ключ для поддержки эмодзи в интерфейсе, бета тестирование
        "description": "settings for PowerSetSetup"
    }

    migrated = False
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                logging.info(f"The configuration file is uploaded: {config_path}")
            migrated = migrate_config(config)
        else:
            logging.warning(f"The configuration file was not found. The default settings are used. File ({config_path})")
            config = default_config
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Error when reading the config.json: {e}")
        print(f"Error when reading the config.json: {e}")
        config = default_config
        sleep(2)
    _CONFIG_CACHE = config
    if migrated:                  # перезаписываем только корректно прочитанный файл
        save_config(config)
    return config

def save_config(config):
    global _CONFIG_CACHE
    config_path = os.path.join('data', 'config', 'config.json')
    try:
        config["last_modified"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        _CONFIG_CACHE = config  # обновляем кеш
        logging.info(f"Config saved: {config_path}")
        return True
    except Exception as e:
        logging.error(f"Error saving config: {e}")
        return False

def setup_localization(lang_code):
    global _, current_lang
    try:
        normalized_lang = (lang_code or "en").lower()[:2]
        current_lang = normalized_lang
        if normalized_lang == "en":
            translation = gettext.NullTranslations()
        else:
            translation = gettext.translation(DOMAIN, LOCALE_DIR, languages=[normalized_lang], fallback=True)
        translation.install()
        _ = translation.gettext
        logging.info(f"The language is set: {normalized_lang}")
    except Exception as e:
        logging.error(f"Error when setting the language: {lang_code}: {e}")
        _ = gettext.gettext

def apply_language_from_config():
    config = load_config()
    
    if config.get("auto_language", True):
        system_lang = get_system_lang()
        logging.info(f"Automatic language detection: system language = {system_lang}")
        setup_localization(system_lang)
    else:
        saved_lang = config.get("language", "en")
        logging.info(f"The saved language is used: {saved_lang}")
        setup_localization(saved_lang)
    
    return config

def language_setting(new_lang):
    config = load_config()
    config["language"] = new_lang
    config["auto_language"] = False
    if save_config(config):
        logging.info(f"{log_configuration_file_saved}")
    
    setup_localization(new_lang)

config = apply_language_from_config()

id_power_sh_send = ""

def update_text_variables():
    global lang_addPowerPlanInfo, lang_scheme_warning, lang_fix_update
    global lang_choice, lang_back_main_menu, lang_back_advancedsettings, lang_exit
    global lang_max_performance, lang_performance, lang_balanced, lang_powersave
    global lang_change_language, lang_current_language, lang_select_language
    global lang_settings_menu, lang_language_settings, lang_press_enter
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
    global lang_low_power_scheme_deleted, lang_beta_updates, lang_on
    global lang_settings_succesfull, lang_successfully, lang_off
    global lang_minutes, lang_settings_time_sleep, lang_auto_language_setting
    global lang_settings_timeout_monitor, lang_low_beta_updates
    global lang_config_power_plan, lang_beta_settings, lang_interface_settings
    global lang_automatic_check_updates, lang_program_closed_install_update
    global lang_run_program_again_install, lang_automatic_check_updates_completed
    global lang_interface_emotes, lang_enable, lang_disable, lang_update_settings
    
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
    global log_automatic_check_updates, log_update_ready_install, log_automatic_update_disabled, log_go_main_menu, log_go_automode_menu
    global log_go_advanced_menu, log_add_sh

    # logs errors
    global log_error_input, log_error_activate_sh, log_error_automode, log_configuration_file_not_found, log_error_language_set
    global log_error_reading_configuration_file, log_error_configuration_file_saved, log_error_executing, log_error_update_module
    global log_error_auto_update_configuration_file, log_error_auto_update, log_error_check_update, log_error_add_sh
    
    # Определение всех языковых строк lang
    lang_addPowerPlanInfo = _('{Fore.RED}WARNING: Available to add: only {Fore.CYAN}"Ultimate Performance"!').format(Fore=Fore)
    lang_scheme_warning = _('{Fore.RED}WARNING: All other power plans will be deleted after you select one!').format(Fore=Fore)
    lang_choice = _("\nEnter the number: ")
    lang_back_main_menu = _("Back to main menu")
    lang_back_advancedsettings = _("Back to Advanced Settings")
    lang_exit = _("{Fore.RED}Exit").format(Fore=Fore)
    lang_max_performance = _("Maximum performance")
    lang_performance = _("High performance")
    lang_balanced = _("Balanced")
    lang_powersave = _("Power saving")
    lang_change_language = _("Change language")
    lang_current_language = _("Current language")
    lang_select_language = _("Select language:")
    lang_settings_menu = _("Settings")
    lang_language_settings = _("Language settings")
    lang_menu_title = _("Main Menu")
    lang_advancedSettings = _("Advanced settings")
    lang_autoConfiguration = _("Automatic configuration")
    lang_system_show_info = _("Show system information")
    lang_test_pc = _("Performance test")
    lang_update_settings = _("Update settings")
    lang_check_update_main = _("Check for updates")
    lang_check_update = _("Checking for updates")
    lang_info = _("About")
    lang_system_info = _("System information")
    lang_test_perf = _("Performance test")
    lang_about = _("About")
    lang_author = _("Author: BrocatScript")
    lang_supportdeveloper = _("Support the author")
    lang_version = _("Current version:")
    lang_latest_version = _("Latest version:")
    lang_new_release = _("New version available:")
    lang_download_update = _("Download the update?")
    lang_skip_update = _("Skip update")
    lang_system_latest_version = _('You have the {Fore.GREEN}latest{Fore.RESET} version!').format(Fore=Fore)
    lang_open_page = _("Opening the page")
    lang_choice_required_mode = _("Choose the required mode")
    lang_max_power_consumption = _("Maximum power consumption")
    lang_balans_consumption = _("Power consumption balance")
    lang_low_power = _("Lowers battery consumption")
    lang_result_before = _('{Fore.CYAN}Result before:').format(Fore=Fore)
    lang_result_after = _('{Fore.CYAN}Result after:').format(Fore=Fore)
    lang_result = _('{Fore.CYAN}Result:').format(Fore=Fore)
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
    lang_enter_timeout_minutes = _("Set the display turn‑off time:")
    lang_minutes = _("minutes")
    lang_settings_menu_scheme = _("Advanced scheme settings")
    lang_settings_timeout_monitor = _("Display off time")
    lang_settings_time_sleep = _("Time to enter sleep mode")
    lang_settings_timeout_disk = _("Hard disk shutdown time")
    lang_config_power_plan = _("Current power supply circuit settings")
    lang_beta_settings = _("Beta Version Settings")
    lang_settings_saved = _("Settings saved")
    lang_fix_update = _("A fix for the update is available:")
    lang_beta_update = _("Beta update available:")
    lang_beta_updates = _("Beta updates")
    lang_low_beta_updates = _("beta updates")
    lang_auto_language_setting = _("Auto language detection")
    lang_automatic_check_updates = _("Automatic check for updates")
    lang_program_closed_install_update = _("The program will be closed to install the update.")
    lang_run_program_again_install = _("Run the program again after installation.")
    lang_automatic_check_updates_completed = _("The automatic update check is completed.")
    lang_interface_emotes = _("Emojis in the interface:")
    lang_enable = _("Enable")
    lang_disable = _("Disable")
    lang_interface_settings = _("Interface Settings")
    lang_on = _("ON")
    lang_off = _("OFF")

    # errors
    lang_error_os = _('{Fore.RED}YOUR SYSTEM IS NOT WINDOWS, THE PROGRAM IS TERMINATING!').format(Fore=Fore)
    lang_error_id_power_scheme = _('{Fore.RED}ERROR: Scheme with ID {Fore.WHITE}{id}{Fore.RED} not found!').format(Fore=Fore, id="{id}")
    lang_error_reset_scheme = _("ERROR: couldn't restore schemas to default settings")
    lang_error_timeout_0_minutes = _('{Fore.RED}Error: Cannot set {Fore.CYAN}0 minutes!').format(Fore=Fore)
    lang_error_timeout_10_minutes = _('{Fore.RED}Error: Cannot set {Fore.CYAN}10 minutes!').format(Fore=Fore)
    lang_error_timeout_15_minutes = _('{Fore.RED}Error: Cannot set {Fore.CYAN}15 minutes!').format(Fore=Fore)
    lang_error_timeout_20_minutes = _('{Fore.RED}Error: Cannot set {Fore.CYAN}20 minutes!').format(Fore=Fore)
    lang_error_back_main_menu = _('{Fore.RED}ERROR! You cannot go back because this is the main menu.').format(Fore=Fore)
    lang_error_add_max_power_scheme = _('{Fore.RED}ERROR: Failed to add the power scheme {Fore.WHITE}"Maximum Performance"!').format(Fore=Fore)
    lang_error_low_power_scheme_not_found = _('{Fore.RED}Scheme "Power saving" not found!').format(Fore=Fore)
    lang_error_max_performance_scheme_not_found = _('{Fore.RED}ERROR: Scheme "Maximum performance" not found!').format(Fore=Fore)
    lang_error_performance_scheme_not_found = _('{Fore.RED}ERROR: Scheme "High performance" not found!').format(Fore=Fore)
    lang_error_balanced_scheme_not_found = _('{Fore.RED}ERROR: Scheme "Balanced" not found!').format(Fore=Fore)
    lang_error_check_update = _('{Fore.RED}ERROR: Update check failed!').format(Fore=Fore)
    lang_error_input = _('{Fore.RED}ERROR: The message is written incorrectly or it is empty! {Fore.WHITE}Try again!').format(Fore=Fore)
    lang_error_automode = _('{Fore.RED}ERROR: An error occurred during the automatic configuration!').format(Fore=Fore)
    lang_press_enter = _("Press {Fore.CYAN}Enter{Fore.RESET} to continue...").format(Fore=Fore)
    
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
    log_go_main_menu = _("Go to the main menu")
    log_go_automode_menu = _("Switching to automatic settings via the main menu")
    log_go_advanced_menu = _("Access to advanced settings via the main menu")

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
    log_error_check_update = _("Updates verification error")
    log_add_sh = _("The scheme was successfully added:")
    log_error_add_sh = _("Couldn't add schema:")


# update text
update_text_variables()

def error_os():
    try:
        print(lang_error_os)
        sleep(3)
        sys.exit(0)
    except Exception as e:
        logging.error(f"Critical error in error_os: {e}, uninstall program please!")
        print(f"{Fore.RED}Critical error in error_os: {e}")
        sys.exit(1)

def _powercfg_run(args, check=True):
    """Run powercfg reliably and return CompletedProcess.

    powercfg is a native Windows executable, so shell=True is intentionally not
    used. stderr/stdout are captured so real Windows error messages reach the log.
    """
    if platform.system() != 'Windows':
        error_os()

    cmd = ['powercfg', *[str(arg) for arg in args]]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            check=check,
            shell=False,
        )
        if result.stdout.strip():
            logging.debug(f"powercfg stdout: {result.stdout.strip()}")
        if result.stderr.strip():
            logging.debug(f"powercfg stderr: {result.stderr.strip()}")
        return result
    except subprocess.CalledProcessError as e:
        stdout = (e.stdout or '').strip()
        stderr = (e.stderr or '').strip()
        logging.error(
            f"powercfg failed (code={e.returncode}): {' '.join(cmd)}; "
            f"stdout={stdout!r}; stderr={stderr!r}"
        )
        raise
    except FileNotFoundError:
        logging.exception("powercfg.exe was not found in PATH")
        raise
    except Exception:
        logging.exception(f"Unexpected error while running {' '.join(cmd)}")
        raise


def _extract_guids(text):
    return set(re.findall(
        r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
        text or '',
        re.IGNORECASE,
    ))


def powercfg_list():
    """Print the current power-plan list."""
    try:
        result = _powercfg_run(['/list'])
        if result.stdout:
            print(result.stdout, end='' if result.stdout.endswith('\n') else '\n')
        return result.stdout
    except Exception as e:
        logging.error(f"{log_error_executing} powercfg /list: {e}")
        return ""


def get_powercfg_list():
    """Return the raw output of powercfg /list, or an empty string on failure."""
    try:
        return _powercfg_run(['/list']).stdout or ''
    except Exception as e:
        logging.error(f"{log_error_executing} get powercfg /list: {e}")
        return ""


def powercfg_list_get():
    """Return scheme GUIDs; return None when powercfg itself failed."""
    try:
        result = _powercfg_run(['/list'])
        guids = _extract_guids(result.stdout)
        logging.debug(f"Found power schemes: {sorted(guids)}")
        return guids
    except Exception as e:
        logging.error(f"Не удалось получить список схем: {e}")
        return None


def powercfg_geta_sh():
    """Print and return the active power-plan information."""
    try:
        result = _powercfg_run(['/getactivescheme'])
        output = result.stdout or ''
        if output:
            print(output, end='' if output.endswith('\n') else '\n')
        return output
    except Exception as e:
        logging.error(f"{log_error_executing} powercfg /getactivescheme: ({e})")
        return ""


def _get_active_guid():
    """Return the active scheme GUID, or None if it cannot be determined."""
    output = powercfg_geta_sh()
    guids = _extract_guids(output)
    return next(iter(guids), None) if guids else None


def _find_scheme_guid(preferred_guid):
    """Find preferred scheme GUID, case-insensitively."""
    guids = powercfg_list_get()
    if guids is None:
        return None
    for guid in guids:
        if guid.lower() == preferred_guid.lower():
            return guid
    return None


def _duplicate_scheme(source_guid):
    """Duplicate a scheme and return the GUID reported by powercfg.

    powercfg may create a GUID different from the source GUID. The old code
    ignored that returned GUID, which made activation fail intermittently.
    """
    result = _powercfg_run(['-duplicatescheme', source_guid])
    guids = _extract_guids(result.stdout)
    if not guids:
        # Some Windows/localization combinations may put the useful text in stderr.
        guids = _extract_guids(result.stderr)
    if not guids:
        raise RuntimeError(
            f"powercfg duplicated the scheme but did not return a GUID. "
            f"stdout={result.stdout!r}, stderr={result.stderr!r}"
        )
    # The first GUID is normally the source and the second is the new destination.
    # Prefer a GUID that differs from the source; otherwise use the only GUID.
    for guid in guids:
        if guid.lower() != source_guid.lower():
            return guid
    return next(iter(guids))


def _ensure_scheme(source_guid):
    """Ensure a scheme exists and return the GUID that can actually be activated.

    Automodes intentionally remove all non-selected schemes. Therefore a later
    automode may need to recreate a standard Windows scheme whose source GUID
    was removed by an earlier automode. In that case restore the Windows
    default plans once, then retry the duplication.
    """
    existing = _find_scheme_guid(source_guid)
    if existing:
        return existing

    logging.info(f"Scheme {source_guid} is absent; restoring default power schemes before recreation")
    try:
        _powercfg_run(['-restoredefaultschemes'])
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Не удалось восстановить стандартные схемы перед созданием {source_guid}. "
            f"returncode={e.returncode}; stderr={getattr(e, 'stderr', '')!r}"
        ) from e

    # Check again after restore. Most standard schemes are recreated directly.
    existing = _find_scheme_guid(source_guid)
    if existing:
        return existing

    logging.info(f"Scheme {source_guid} is still absent; trying to duplicate it")
    created = _duplicate_scheme(source_guid)
    logging.info(f"Created power scheme {created} from {source_guid}")

    if _find_scheme_guid(created) is None:
        raise RuntimeError(f"Created scheme {created} was not found in powercfg /list")
    return created


def _activate_scheme_guid(guid):
    """Activate a scheme and verify that Windows accepted it."""
    _powercfg_run(['/setactive', guid])
    active = _get_active_guid()
    if active is None or active.lower() != guid.lower():
        raise RuntimeError(
            f"powercfg reported success, but active scheme is {active!r}; expected {guid!r}"
        )
    logging.info(f"Power scheme activated successfully: {guid}")
    return True


def activate_power_scheme(source_guid, scheme_name, success_message, error_message):
    """Common reliable activation path for manual and automatic modes."""
    clear()
    print(".")
    try:
        actual_guid = _ensure_scheme(source_guid)
        print("..")
        _activate_scheme_guid(actual_guid)
        clear()
        print("...")
        logging.info(f'{log_activate_sh} {scheme_name}; GUID={actual_guid}')
        print(success_message)
        return actual_guid
    except subprocess.CalledProcessError as e:
        clear()
        logging.error(f'{log_error_activate_sh} {scheme_name}: {e}')
        print(error_message)
    except Exception as e:
        clear()
        logging.error(f'{log_error_activate_sh} {scheme_name}: {e}', exc_info=True)
        print(error_message)
    sleep(1)
    return None

def build_full_version(config=None):
    """Версия берётся из КОДА (APP_VERSION / BUILD_CHANNEL), config.json не читается."""
    if BUILD_CHANNEL == "stable":
        return APP_VERSION
    return f"{APP_VERSION} {BUILD_CHANNEL}"


# ОБНОВЛЕНИЯ
# Манифест на GitHub (version_1.00.0.json): ключи stable / beta / demo,
# по одной записи на канал. Версии формата A.BB.C: 1.00.0 < 1.00.1 < 1.10.0.
# При ОДИНАКОВОМ номере stable лучше beta, а beta лучше demo.

KNOWN_CHANNELS = ("stable", "beta", "demo")
CHANNEL_RANK = {"stable": 2, "beta": 1, "demo": 0}
_VER_RE = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")
_NO_URL = {"", "none", "demo"}          # "None" / "demo" / пусто в download_url = ссылки нет


def parse_app_version(s):
    """'1.02.1' -> (1, 2, 1). Кортежи сравниваются по частям."""
    m = _VER_RE.match(str(s).strip())
    if not m:
        raise ValueError(f"bad version: {s!r}")
    return tuple(int(x) for x in m.groups())


def _channel_key(version_tuple, channel):
    """Что «лучше»: сначала номер версии, при равенстве - стабильность канала."""
    return (version_tuple, CHANNEL_RANK.get(channel, 0))


@dataclass
class UpdateInfo:
    channel: str
    version: str
    release_url: Optional[str]
    download_url: Optional[str]
    winget_update: bool
    github_update: bool
    mandatory: bool
    changelog: str
    portable: dict = field(default_factory=dict)   # {".7z": url, ".zip": url} - в порядке манифеста
    same_version: bool = False                     # тот же номер, но канал стабильнее (beta -> stable)


@dataclass
class CheckResult:
    status: str                            # "update" | "up_to_date" | "error"
    update: Optional[UpdateInfo] = None    # stable/beta, который лучше текущей сборки
    demo: Optional[UpdateInfo] = None      # показывается ТОЛЬКО когда обновления нет
    warning: Optional[str] = None          # "demo_build" | "unknown_build"
    error: Optional[str] = None


@dataclass
class Action:
    kind: str                       # "winget" | "download_exe" | "portable" | "demo" | "open_page" | "none"
    url: Optional[str] = None
    options: dict = field(default_factory=dict)   # portable: {".zip": url, ...}
    preselected: Optional[str] = None             # portable: запомненный формат / updater: метод


def fetch_manifest(url=None, timeout=5.0):
    """Читает манифест с GitHub сразу в память (без временных файлов)."""
    url = url or MANIFEST_URL
    if not url.startswith("https://"):
        raise ValueError("manifest must be fetched over https")
    # Всегда запрашиваем свежий манифест: CDN/proxy не должен отдавать старый ответ.
    # Параметр меняется при каждом запросе; не используем локальный файл/кэш.
    cache_buster = time.time_ns()
    headers = {
        "Cache-Control": "no-cache, no-store, max-age=0",
        "Pragma": "no-cache",
        "Expires": "0",
        "User-Agent": f"{Name_Program}/{APP_VERSION}",
    }
    resp = requests.get(
        url,
        timeout=timeout,
        headers=headers,
        params={"_": cache_buster},
    )
    resp.raise_for_status()
    if len(resp.content) > 256 * 1024:
        raise ValueError("manifest is too large")
    return resp.json()


def _safe_url(u):
    """Ссылка годится, только если она с нашего GitHub. "None"/"demo"/пусто -> None."""
    if not isinstance(u, str) or u.strip().lower() in _NO_URL:
        return None
    return u if u.startswith(ALLOWED_URL_PREFIX) else None


def _url_ext(url):
    return os.path.splitext(urlparse(url).path)[1].lower()


def _make_info(channel, e, lang):
    formats = [str(f).lower() for f in (e.get("portable_format") or [])]
    urls = [u for u in (_safe_url(x) for x in (e.get("portable_download_url") or [])) if u]
    by_ext = {_url_ext(u): u for u in urls}
    # Список форматов СОБИРАЕТСЯ из манифеста: только те, для которых реально есть ссылка,
    # в порядке portable_format
    order = formats or list(by_ext)
    portable = {ext: by_ext[ext] for ext in order if ext in by_ext}
    log = e.get("changelog") or {}
    return UpdateInfo(
        channel=channel, version=e["version"],
        release_url=_safe_url(e.get("release_url")),
        download_url=_safe_url(e.get("download_url")),
        winget_update=e.get("winget_update") is True,
        github_update=e.get("github_update") is True,
        mandatory=e.get("mandatory") is True,
        changelog=log.get(lang) or log.get("en") or "",
        portable=portable,
    )


def _manifest_entry(manifest, channel):
    e = manifest.get(channel)
    if not isinstance(e, dict):
        return None
    try:
        return parse_app_version(e["version"]), e
    except (KeyError, ValueError, TypeError):
        return None                        # битый канал не ломает остальные


def check_manifest(manifest, current=None, include_beta=False, build_channel=None, lang=None):
    current = current or APP_VERSION
    build_channel = build_channel or BUILD_CHANNEL
    lang = lang or current_lang
    warning = None
    if build_channel == "demo":
        warning = "demo_build"
    elif build_channel not in KNOWN_CHANNELS:
        warning = "unknown_build"
    try:
        cur_key = _channel_key(parse_app_version(current), build_channel)
        if not isinstance(manifest, dict):
            raise ValueError("manifest is not an object")

        # include_beta=false -> beta и demo вообще не рассматриваются; stable видят все
        names = ["stable"] + (["beta"] if include_beta else [])
        found = [(n, _manifest_entry(manifest, n)) for n in names]
        found = [(n, f) for n, f in found if f]
        best = max(found, key=lambda x: _channel_key(x[1][0], x[0]), default=None)

        if best and _channel_key(best[1][0], best[0]) > cur_key:
            name, (ver, entry) = best
            info = _make_info(name, entry, lang)
            info.same_version = (ver == parse_app_version(current))
            return CheckResult("update", update=info, warning=warning)

        # Обновлений stable/beta нет. Demo упоминаем только при include_beta
        demo = None
        if include_beta:
            d = _manifest_entry(manifest, "demo")
            if d and _channel_key(d[0], "demo") > cur_key:
                demo = _make_info("demo", d[1], lang)
        return CheckResult("up_to_date", demo=demo, warning=warning)
    except Exception as exc:
        return CheckResult("error", warning=warning, error=f"{type(exc).__name__}: {exc}")


def fetch_and_check(include_beta=False):
    """Скачать манифест и проверить. Не бросает исключений: сбой -> status="error"."""
    try:
        manifest = fetch_manifest()
    except Exception as exc:
        return CheckResult("error", error=f"{type(exc).__name__}: {str(exc)[:200]}")
    return check_manifest(manifest, include_beta=include_beta)


def mandatory_pending(cfg, current=None):
    """Работает БЕЗ сети: на старте главного меню показать плашку."""
    if not cfg.get("update_required"):
        return False
    ver = cfg.get("mandatory_version")
    if not ver:
        return True                        # флаг есть, версии нет: погасим при следующей проверке
    try:
        return parse_app_version(ver) > parse_app_version(current or APP_VERSION)
    except ValueError:
        return False


def _clear_mandatory(cfg):
    cfg["update_required"] = False
    cfg["mandatory_version"] = None


def track_mandatory(cfg, result, current=None):
    """Вызывать после каждой проверки (потом save_config)."""
    if result.status == "up_to_date":
        _clear_mandatory(cfg)              # сервер подтвердил: новее ничего нет
    elif result.update is not None and result.update.mandatory:
        old = cfg.get("mandatory_version")
        if not old or parse_app_version(result.update.version) > parse_app_version(old):
            cfg["mandatory_version"] = result.update.version
        cfg["update_required"] = True
    if not mandatory_pending(cfg, current):
        _clear_mandatory(cfg)              # версия программы уже дошла до нужной
    return cfg


# ---------- winget ----------
def installed_via_winget():
    """winget upgrade работает только для копий, которые winget «знает» (не zip/portable)."""
    if shutil.which("winget") is None:
        return False
    try:
        r = subprocess.run(
            ["winget", "list", "--id", WINGET_ID, "--exact", "--accept-source-agreements"],
            capture_output=True, text=True, timeout=30)
        return r.returncode == 0           # по коду возврата, а не по тексту (он локализован)
    except (OSError, subprocess.TimeoutExpired):
        return False


def start_winget_upgrade():
    """Запускает установку/обновление пакета Winget в отдельной консоли.

    --force нужен в том числе для копий, изначально установленных с GitHub:
    Winget может не распознавать их как зарегистрированную установку.
    """
    cmd = ["winget", "install", "--id", WINGET_ID, "--exact", "--force",
           "--accept-package-agreements", "--accept-source-agreements"]
    subprocess.Popen(cmd, creationflags=0x00000010, close_fds=True)   # CREATE_NEW_CONSOLE


# ---------- что делать с найденным обновлением ----------
def _page_action(info):
    return Action("open_page", url=info.release_url) if info.release_url else Action("none")


def plan_action(info, is_portable=None, remembered_format=None, winget_check=None,
                remembered_method=None):
    is_portable = IS_PORTABLE if is_portable is None else is_portable

    if info.channel == "demo":
        return Action("demo", url=info.release_url)

    if is_portable:
        if info.github_update and info.portable:
            pre = remembered_format if remembered_format in info.portable else None
            return Action("portable", options=dict(info.portable), preselected=pre)
        return _page_action(info)

    # Метод доступен только если соответствующий способ включён в манифест
    # и для GitHub действительно есть URL установщика.
    methods = {}
    if info.winget_update:
        methods["winget"] = True
    if info.github_update and info.download_url:
        methods["github"] = info.download_url

    if not methods:
        return _page_action(info)
    if remembered_method in methods:
        return Action("winget") if remembered_method == "winget" else Action("download_exe", url=methods["github"])
    # Если сохранённый способ пропал из манифеста, показываем доступную альтернативу,
    # а не переключаем молча.
    if remembered_method and remembered_method not in methods:
        return Action("choose_method", options=methods)
    if len(methods) == 1:
        method = next(iter(methods))
        return Action("winget") if method == "winget" else Action("download_exe", url=methods[method])
    return Action("choose_method", options=methods)


# ---------- скачивание ----------
def _downloads_dir():
    return os.path.join(os.path.expanduser("~"), "Downloads")


def download_file(url, dest_dir=None, timeout=30.0, allowed_prefix=None, progress=None):
    """Качает файл в «Загрузки» (сначала .part, потом переименование). Возвращает путь."""
    prefix = allowed_prefix or ALLOWED_URL_PREFIX
    if not url.startswith(prefix):
        raise ValueError("download url is not allowed")
    folder = dest_dir or _downloads_dir()
    os.makedirs(folder, exist_ok=True)
    name = os.path.basename(urlparse(url).path) or "PowerSetSetup_update"
    stem, ext = os.path.splitext(name)
    dest, n = os.path.join(folder, name), 1
    while os.path.exists(dest):            # не затираем прошлые загрузки
        dest = os.path.join(folder, f"{stem} ({n}){ext}")
        n += 1
    tmp = dest + ".part"
    try:
        headers = {"User-Agent": f"{Name_Program}/{APP_VERSION}"}
        with requests.get(url, stream=True, timeout=timeout, headers=headers) as r:
            r.raise_for_status()
            total = int(r.headers.get("content-length", 0) or 0)
            done = 0
            with open(tmp, "wb") as f:
                for chunk in r.iter_content(chunk_size=1 << 16):
                    if not chunk:
                        continue
                    f.write(chunk)
                    done += len(chunk)
                    if progress:
                        progress(done, total)
        os.replace(tmp, dest)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
    return dest


# ---------- интерфейс ----------
def _pause():
    input(f"\n{lang_press_enter}")


def _ask_yes_no(question):
    answer = input(f"{question} (y/n): ").strip().lower()
    return answer in ("y", "yes", "д", "да")


_download_progress_started = None


def _print_progress(done, total):
    """Показывает процент, среднюю скорость и объём загрузки в одной строке."""
    global _download_progress_started
    now = time.monotonic()
    if _download_progress_started is None:
        _download_progress_started = now
    elapsed = max(now - _download_progress_started, 0.001)
    speed = done / elapsed  # bytes/sec
    done_mb = done / (1024 * 1024)
    speed_mb = speed / (1024 * 1024)
    if total > 0:
        total_mb = total / (1024 * 1024)
        percent = done / total * 100
        line = f"{percent:5.1f}% | {speed_mb:5.2f} MB/s | {done_mb:.1f}/{total_mb:.1f} MB"
    else:
        line = f"{done_mb:.1f} MB | {speed_mb:5.2f} MB/s"
    print(f"\r{line:<55}", end="", flush=True)


def print_update_required_banner():
    """Плашка в главном меню: обязательное обновление ещё не установлено (работает без сети)."""
    cfg = load_config()
    if mandatory_pending(cfg):
        ver = cfg.get("mandatory_version")
        suffix = f": {ver}" if ver else ""
        print(f"{Fore.RED}{_('A required update is available')}{suffix}")
        print(f"{Fore.RED}{_('Install it from the main menu:')} {lang_check_update_main}")

def _open_release_page(url):
    print(f"\n{lang_open_page}")
    try:
        webbrowser.open(url)
        logging.info(f"Release page opened: {url}")
    except Exception as e:
        logging.error(f"Could not open the release page: {e}")
        print(e)


def _show_demo(info):
    """Demo: только предупреждение и ссылка. Скачать «привычным способом» нельзя."""
    print(_("A demo version is available: {version}").format(version=info.version))
    print(_("It is only meant for trying out new features. Do not replace your working version with it!"))
    print(_("This version cannot be installed in the usual way because it is a demo version."))
    if info.changelog:
        print(f"\n{_('What is new:')} {info.changelog}")
    if info.release_url:
        print(f"{_('Release page:')} {info.release_url}\n")
        if _ask_yes_no(_("Open the release page?")):
            _open_release_page(info.release_url)


def choose_portable_format(options, remember_default=False):
    """Меню выбора формата архива.

    options - словарь {".7z": url, ".zip": url}, его порядок и состав приходят из манифеста.
    Пункты меню строятся ЦИКЛОМ по списку форматов, а выбранный номер превращается обратно в
    формат через formats[номер - 1]. Поэтому .zip может быть и пунктом 1, и 2, и 3 - в коде
    нет ни одного жёстко прописанного "1 = .7z".

    Возвращает (формат, запомнить_выбор) или None, если пользователь пропустил обновление.
    """
    formats = list(options)
    remember = remember_default
    while True:
        clear()
        print(f"{_('Choose the archive format to download:')}\n")
        for number, fmt in enumerate(formats, start=1):
            print(f"{number}. {fmt}")
        skip_number = len(formats) + 1
        print(f"{skip_number}. {lang_skip_update}")
        print(f"\n[{'x' if remember else ' '}] {_('Remember my choice')}")
        print(_('Type r to turn "Remember my choice" on or off'))

        answer = input(lang_choice).strip().lower()
        typed_format = answer if answer.startswith(".") else f".{answer}"
        if answer in ("r", "к"):                      # «галочка»
            remember = not remember
        elif answer.isdigit() and 1 <= int(answer) <= len(formats):
            return formats[int(answer) - 1], remember
        elif typed_format in formats:                 # можно вписать и "zip" / ".zip"
            return typed_format, remember
        elif (answer.isdigit() and int(answer) == skip_number) or answer in ("0", "9", "b", "back", "skip"):
            return None
        else:
            logging.error("Invalid input in the portable format menu")
            print(lang_error_input)
            sleep(1)


def choose_update_method(options, remember_default=False):
    """Выбор Winget/GitHub с переключаемой галочкой запоминания."""
    methods = list(options)
    remember = remember_default
    while True:
        clear()
        print(f"{_('Choose how to update PowerSetSetup:')}\n")
        for number, method in enumerate(methods, start=1):
            label = _('Winget') if method == "winget" else _('GitHub installer')
            print(f"{number}. {label}")
        print(f"{len(methods) + 1}. {lang_skip_update}")
        print(f"\n[{'x' if remember else ' '}] {_('Remember my choice')}")
        print(_('Type r to turn "Remember my choice" on or off'))
        answer = input(lang_choice).strip().lower()
        if answer in ("r", "к"):
            remember = not remember
        elif answer.isdigit() and 1 <= int(answer) <= len(methods):
            return methods[int(answer) - 1], remember
        elif answer.isdigit() and int(answer) == len(methods) + 1 or answer in ("0", "b", "back", "skip"):
            return None, remember
        else:
            logging.error("Invalid input in the update method menu")
            print(lang_error_input)
            sleep(1)


def _download_with_ui(url):
    global _download_progress_started
    _download_progress_started = time.monotonic()
    print(f"\n{_('Downloading...')}")
    try:
        path = download_file(url, progress=_print_progress)
    except Exception as e:
        logging.error(f"Update download failed: {e}")
        print(_("{Fore.RED}Download failed: {error}").format(Fore=Fore, error=e))
        _pause()
        return None
    print()
    print(_("Saved to: {path}").format(path=path))
    logging.info(f"Update downloaded: {path}")
    return path


def _finish_after_download(path, message):
    """Показать файл в проводнике, дождаться Enter и закрыть программу (пользователь ставит сам)."""
    print(f"\n{message}")
    try:
        subprocess.Popen(["explorer", f"/select,{path}"])
    except Exception as e:
        logging.warning(f"Could not open Explorer: {e}")
    _pause()
    sys.exit(0)


def _run_update_action(info, action, config):
    """Выполнить выбранное действие. Возвращает False, если пользователь отказался/не вышло."""
    auto = config.get("auto_download_install", False)

    if action.kind == "choose_method":
        picked = choose_update_method(action.options, config.get("update_method_remember", False))
        if picked[0] is None:
            config["update_method_remember"] = picked[1]
            if not picked[1]:
                config["update_method"] = None
            save_config(config)
            return False
        method, remember = picked
        config["update_method_remember"] = remember
        config["update_method"] = method if remember else None
        save_config(config)
        selected = Action("winget") if method == "winget" else Action("download_exe", url=action.options["github"])
        return _run_update_action(info, selected, config)

    if action.kind == "winget":
        print(_("The update will be installed with winget in a separate window."))
        if not auto and not _ask_yes_no(_("Install the update?")):
            return False
        try:
            start_winget_upgrade()
        except Exception as e:
            logging.error(f"Could not start winget: {e}")
            print(_("{Fore.RED}Could not start winget: {error}").format(Fore=Fore, error=e))
            _pause()
            return False
        logging.info("winget upgrade started, closing the program")
        print(lang_program_closed_install_update)
        print(lang_run_program_again_install)
        sleep(2)
        sys.exit(0)

    if action.kind == "download_exe":
        print(_('The installer will be downloaded to the "Downloads" folder'))
        if not auto and not _ask_yes_no(lang_download_update):
            return False
        path = _download_with_ui(action.url)
        if path is None:
            return False
        _finish_after_download(path, _("Run the downloaded file yourself. The program will now close."))

    if action.kind == "portable":
        if action.preselected:                        # формат запомнен: спрашивать не нужно
            fmt = action.preselected
            print(_("Archive format: {fmt}").format(fmt=fmt))
            if not auto and not _ask_yes_no(lang_download_update):
                return False
        else:
            picked = choose_portable_format(action.options, config.get("portable_remember", False))
            if picked is None:
                return False
            fmt, remember = picked
            config["portable_remember"] = remember
            config["portable_choice"] = fmt if remember else None
            save_config(config)
        path = _download_with_ui(action.options[fmt])
        if path is None:
            return False
        _finish_after_download(
            path, _("Unpack the archive and replace the current version yourself. The program will now close."))

    if action.kind == "demo":
        _show_demo(info)
        return False

    if action.kind == "open_page":
        print(_("Automatic installation is not available for this version. You can download it manually from the release page"))
        print(f"{_('Release page:')} {action.url}\n")
        if _ask_yes_no(_("Open the release page?")):
            _open_release_page(action.url)
        return False

    print(_("No download link is available for this version."))
    return False


def check_update():
    """Пункт главного меню «Проверка обновлений»."""
    logging.info("Checking for updates")
    clear()
    config = load_config()
    print(lang_check_update + "...")
    result = fetch_and_check(config.get("include_beta", False))

    before = (config.get("update_required"), config.get("mandatory_version"))
    track_mandatory(config, result)
    if before != (config.get("update_required"), config.get("mandatory_version")):
        save_config(config)

    clear()
    if result.warning == "demo_build":
        print(_("{Fore.YELLOW}This is a demo build. It only demonstrates some features, so use it with extreme caution!").format(Fore=Fore))
    elif result.warning == "unknown_build":
        print(_("{Fore.YELLOW}This build is unknown to the update system. Use it with caution!").format(Fore=Fore))
    print(f"{lang_version} {build_full_version()}\n")

    if result.status == "error":
        print(lang_error_check_update)

        if result.error and "JSONDecodeError" in result.error:
            details = _(
                "Server-side problem: invalid version manifest format!"
            )
            print(_("Details: {details}").format(details=details))

            logging.error(
                "Update check failed: invalid JSON in version manifest"
            )
            logging.error("System: %s", result.error)

        else:
            details = _("Could not retrieve or process update information.")
            print(_("Details: {details}").format(details=details))

            logging.error("Update check failed: %s", result.error)

        _pause()
        main_menu()
        return

    if result.status == "up_to_date":
        logging.info("No update available")
        print(lang_system_latest_version)
        if result.demo:
            print()
            _show_demo(result.demo)
        _pause()
        main_menu()
        return

    info = result.update
    if info is None:                       # для type checker: при status="update" сюда не попадём
        main_menu()
        return
    if info.same_version:
        print(f"{_('Your beta build has been released as a stable version:')} {info.version} ({info.channel})")
    elif info.channel == "beta":
        print(f"{lang_beta_update} {info.version}")
    else:
        print(f"{lang_new_release} {info.version} ({info.channel})")
    if info.changelog:
        print(f"{_('What is new:')} {info.changelog}")
    if info.mandatory:
        print(_("{Fore.RED}This update is required. Skipping it is not recommended").format(Fore=Fore))
    print()

    remembered = config.get("portable_choice") if config.get("portable_remember") else None
    remembered_method = config.get("update_method") if config.get("update_method_remember") else None
    action = plan_action(info, remembered_format=remembered, remembered_method=remembered_method)
    logging.info(f"Update found: {info.channel} {info.version}, action: {action.kind}")
    _run_update_action(info, action, config)
    main_menu()

event_brocatscript = False

# Main menu program
def main_menu():
    global event_brocatscript
    logging.info(log_go_main_menu)
    while True:
        if event_brocatscript == True:
            add_color = Fore.GREEN
            add_color2 = Fore.CYAN
        else:
            add_color = ""
            add_color2 = ""
        update_text_variables()
        clear()
        print(f"{Fore.CYAN}PowerSetSetup {Fore.RESET}v{build_full_version()}")
        print_update_required_banner()
        powercfg_list()
        print()
        # print(event_brocatscript)
        print(f"{add_color}{lang_menu_title}")
        print(f"\n1. {lang_autoConfiguration}")
        print("2.", lang_advancedSettings)
        print("3.", lang_check_update_main)
        # print("4.", "lang_diagnostics")
        print("4.", lang_supportdeveloper)
        print("5.", lang_settings_menu)
        print("6.", lang_back)
        print(f"7. {lang_exit}")

        main_menu = input(lang_choice).lower().strip()
        if main_menu == "1":
            logging.info(log_go_automode_menu)
            automode_menu()
            break
        elif main_menu == "2":
            logging.info(log_go_advanced_menu)
            advancedSettings()
            break
        elif main_menu == "3":
            logging.info("start Checking for updates...") # временно
            check_update()
            break
        # elif main_menu == "4":
            # logging.info("Diagnostics")
            # diagnostics()
           # break
        elif main_menu == "4":
            logging.info("Support Developer") # временно
            support_developer()
            break
        elif main_menu == "5":
            logging.info("Start Settings menu") # временно
            settings_menu()
            break
        elif main_menu in ["9", "6", "back", "b"]:
            clear()
            print(f"{lang_error_back_main_menu}")
            sleep(1)
        elif main_menu in ["0", "7", "exit", "end", "e"]:
            end()
            break
        elif main_menu in ["ru", "r", "ру", "р"]:
            language_setting('ru')
        elif main_menu == "en":
            language_setting('en')
        elif main_menu == "brocatscript":
            event_brocat_script()
        elif main_menu == "stop event" or "stopevent":
            stop_all_event()
        else:
            clear()
            logging.error(f"{log_error_input} (Main_menu)")
            print(f"{lang_error_input}")
            sleep(1)

def stop_all_event():
    clear()
    global event_brocatscript
    event_brocatscript = False

def event_brocat_script():
    global event_brocatscript
    clear()
    if current_lang == "ru":
        print(f"{Fore.YELLOW}Событие BrocatScript{Fore.RESET}")
        print(f"{Fore.YELLOW}Это скрытое событие в программе{Fore.RESET}")
        print(f"{Fore.YELLOW}Вы нашли секретную функцию!{Fore.RESET}")
        print(f"{Fore.YELLOW}Эта функция не документирована и может быть удалена в будущих версиях.{Fore.RESET}")
        print(f"{Fore.YELLOW}Спасибо за использование PowerSetSetup!{Fore.RESET}")
        _pause()
    else:
        print(f"{Fore.YELLOW}BrocatScript event{Fore.RESET}")
        print(f"{Fore.YELLOW}This is a hidden event in the program{Fore.RESET}")
        print(f"{Fore.YELLOW}You have found a secret feature!{Fore.RESET}")
        print(f"{Fore.YELLOW}This feature is not documented and may be removed in future versions.{Fore.RESET}")
        print(f"{Fore.YELLOW}Thank you for using PowerSetSetup!{Fore.RESET}")
        _pause()

    event_brocatscript = True
    logging.info("")
    logging.info(r'01010101ba   01010101ba     ,ad0101ba,      .ad0101ba,         db    010101010101      ad01010ba     ,ad1010ba,   101010101ba  {}  10101010ba  101010101010')
    logging.info(r'10      "1b  10      \1b   d1/      \0b    d1}"    "{1b       d01b        01          [1"     "0b   d1}`    `{0b  01      \1b  []  10      \1b      10     ')
    logging.info(r'01      ,0}  01      ,0}  d0/        \1b  d0/                d1/\0b       10          [0,          d0/            10      ,0}  []  01      /0}      01     ')
    logging.info(r"10aaaaaa1}/  10aaaaaa1/'  10          01  10                d0/  \1b      01          `\1aaaaa,    10             01aaaaaa1/'  []  10aaaaaa1/'      10     ")
    logging.info(r'01""""""0b\  01""""01/    01          10  01               d1/aaaa\0b     10            `"""""0b,  01             10""""01/    []  01""""""         01     ')
    logging.info(r'10      `1b  10    \1b    {1\        /0}  {0\             d0""""""""1b    01                  \1b  {1\            01    \1b    []  10               10     ')
    logging.info(r"01      a0}  01     \0b    {0a\    /a1}    {1a.    .a0}  d1/        \0b   10          \1a     a0]   {0a.    .a1}  10     \0b   []  01               01     ")
    logging.info(r'01010101}"   10      \1b    \[ERROR!]/      \[CODE-00]/ d0/          \1b  01           \ERROR-0/     \[CODE-01]/  01      \1b  []  10               10     ')


# эта функция может не дойдет до реализации
# def diagnostics():
#     logging.info("Diagnostics the system")
#     clear()
#     if platform.system() == "Windows":
#         try:
#             result = subprocess.run(
#                 ["sfc", "/scannow"],
#                 capture_output=True, 
#                 text=True,
#                 encoding="utf-8",
#                 check=False
#             )
#             if result.returncode == 0:
#                 logging.info("sfc /scannow completed successfully")
#                 print("sfc /scannow: OK")
#             else:
#                 logging.error(f"sfc /scannow failed with code {result.returncode}: {result.stderr}")
#                 print(f"sfc /scannow failed (code {result.returncode})")
#             clear()
#             print(f"sfc /scannow output:\n{result.stdout}")
#         except Exception as e:
#             clear()
#             logging.exception("Exception while running sfc /scannow")
#             print(f"Error running sfc: {e}")
#     else:
#         error_os()

def check_os():
    logging.info('Checking the system')
    if platform.system() == "Windows":
        logging.info('The system is recognized as Windows')
        main_menu()
    else:
        logging.error(f'The system is recognized as {platform.system()}')
        error_os()

def advancedSettings():
    logging.debug('Переход в расширенные параметры электропитания')
    while True:
        clear()
        powercfg_list()
        print(f'\n{lang_advancedSettings}')
        print(f'\n1. {lang_delete_scheme}')
        print(f'2. {lang_reset_scheme}')
        print(f'3. {lang_add_scheme}')
        print(f'4. {lang_activate_scheme}')
        print(f'5. {lang_list_scheme}')
        print(f'6. {lang_back_main_menu}')
        print(f'7. {lang_exit}')

        advancedSettings = input(lang_choice)
        if advancedSettings == "1":
            logging.info('Переход в удаление схем через расширенные настройки')
            delete_scheme()
            break
        elif advancedSettings == "2":
            logging.info('Переход в функцию сброса схем через расширенные настройки')
            reset_scheme()
            break
        elif advancedSettings == "3":
            logging.info('Переход в добавление схем через расширенные настройки')
            add_scheme()
            break
        elif advancedSettings == "4":
            logging.info('Переход в активацию схем через расширенные настройки')
            activate_scheme()
            break
        elif advancedSettings == "5":
            logging.info('Переход в функцию просмотра всех схем')
            list_scheme()
            break
        elif advancedSettings in ["9", "6", "back", "b"]:
            logging.info('Переход в главное меню через расширенные настройки')
            main_menu()
            break
        elif advancedSettings in ["0", "7", "exit", "end", "e"]:
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
        print(f"6. {lang_back_advancedsettings}")
        print(f'7. {lang_exit}')

        delete_scheme = input(lang_choice).lower()
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
        elif delete_scheme in ["9", "6", "b", "back"]:
            logging.info(f'{log_select_delete_sh} "{lang_back_advancedsettings}"')
            advancedSettings()
            break
        elif delete_scheme in ["0", "7", "e", "exit", "end"]:
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
        _powercfg_run(cmd[1:])
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
        _powercfg_run(cmd[1:])
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
        "powercfg", "-delete", "e9a42b02-d5df-448d-aa00-03f14749eb61"
    ]

    try:
        clear()
        print("..")
        _powercfg_run(cmd[1:])
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
        _powercfg_run(cmd[1:])
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
        _powercfg_run(cmd[1:])
        clear()
        print("...")
        logging.info(f'{lang_scheme_succesfull_deleted} id = {id_power_sh_send}')
        clear()
        print(lang_scheme_succesfull_deleted)
    except subprocess.CalledProcessError as e:
        clear()
        logging.error(f'Ошибка удаления схемы {id_power_sh_send} ошибка: {e} команда {cmd}')
        print(lang_error_id_power_scheme.format(id=id_power_sh_send))
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
        _powercfg_run(cmd[1:])
        clear()
        print("...")
        logging.info(f'Успешно {lang_reset_scheme}')
        clear()
        print(lang_result_before)
        print(f'{scheme_before}')
        print(f"\n\n{lang_result_after}")
        powercfg_list()
        _pause()
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
        print(f"2. {lang_back_advancedsettings}")
        print(f"3. {lang_back_main_menu}")
        print(f"4. {lang_exit}")

        add_scheme = input(lang_choice)
        if add_scheme == "1":
            add_scheme_max_perfomance()
            break
        elif add_scheme in ["8", "4", "back", "b"]:
            advancedSettings()
            break
        elif add_scheme in ["9", "3", "main", "m"]:
            main_menu()
            break
        elif add_scheme in ["0", "4", "exit", "end", "e"]:
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
        "powercfg", "-duplicatescheme", "e9a42b02-d5df-448d-aa00-03f14749eb61"
    ]

    try:
        clear()
        print("..")
        _powercfg_run(cmd[1:])
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
        print(f"6. {lang_back_advancedsettings}")
        print(f"7. {lang_exit}")

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
        elif activate_scheme in ["6", "9", "back", "b"]:
            advancedSettings()
            break
        elif activate_scheme in ["7", "0", "exit", "end", "e"]:
            end()
            break
        else:
            clear()
            logging.error(f"{log_error_input} ({lang_activate_scheme})")
            print(lang_error_input)
            sleep(1)

def activate_scheme_balanced():
    activate_power_scheme(
        "381b4222-f694-41f0-9685-ff5bb260df2e",
        lang_balanced,
        lang_balanced_scheme_activated,
        lang_error_balanced_scheme_not_found
    )
    advancedSettings()

def activate_scheme_perfomance():
    activate_power_scheme(
        "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c",
        lang_performance,
        lang_performance_scheme_activated,
        lang_error_performance_scheme_not_found
    )
    advancedSettings()

def activate_scheme_max_perfomance():
    activate_power_scheme(
        "e9a42b02-d5df-448d-aa00-03f14749eb61",
        lang_max_performance,
        lang_max_performance_scheme_activated,
        lang_error_max_performance_scheme_not_found
    )
    advancedSettings()

def activate_scheme_powersave():
    activate_power_scheme(
        "a1841308-3541-4fab-bc81-f71556f20b4a",
        lang_powersave,
        lang_low_power_scheme_activated,
        lang_error_low_power_scheme_not_found
    )
    advancedSettings()

def activate_scheme_manual_input():
    clear()
    powercfg_list()
    id_power_sh_send = input(f"\n{lang_enter_id_power_scheme}").lower()
    if id_power_sh_send in ["back", "b", "", " "]:
        advancedSettings()
    elif id_power_sh_send in ["exit", "end", "e"]:
        end()
    clear()
    print(".")
    cmd = [
        "powercfg", "/setactive", f"{id_power_sh_send}"
    ]

    try:
        clear()
        print("..")
        _powercfg_run(cmd[1:])
        clear()
        print("...")
        logging.info(f'{log_activate_sh} {lang_manual_input}')
        clear()
        print(lang_activate_scheme + id_power_sh_send)
    except Exception as e:
        clear()
        logging.error(f'{log_error_activate_sh} {id_power_sh_send} ({e}) [{cmd}]')
        print(lang_error_id_power_scheme.format(id=id_power_sh_send))
    sleep(1)
    advancedSettings()

def list_scheme():
    logging.debug('Переход в просмотр схем')
    clear()
    powercfg_list()
    _pause()

def support_developer():
    while True:
        clear()
        url = ""
        logging.debug("Переход в поддержку разработчика")
        print("1. Cloudtips")
        if current_lang == "ru":
            print("2. DonationAlerts (нет ссылки)")
        else:
            print("2. DonationAlerts (not url)")
        print(f"3. {lang_back_main_menu}")
        print(f"4. {lang_exit}")
        choice = input(lang_choice).lower().strip()

        if choice == "1":
            url = "https://pay.cloudtips.ru/p/0cdee068"
            open_url_support_developer(url)
        if choice == "2":
            clear()
            if current_lang == "ru":
                print("Ссылка не создана или в данный момент не работает.")
            else:
                print("The link has not been created or is not working at the moment.\n")
            _pause()
        if choice == "3":
            main_menu()
        if choice in ["4", "0", "exit", "end", "e", "stop", "s"]:
            end()

def open_url_support_developer(url):
    clear()
    if current_lang == "ru":
        print("Спасибо за поддержку!")
    else:
        print("Thanks for the support!")

    print(f"\n{lang_open_page}")
    try:
        webbrowser.open(url)
        logging.info(f'Ссылка поддержки автора открыта: {url}')
    except Exception as e:
        logging.error(f"Не удалось открыть ссылку, ошибка {e}")
        if current_lang == "ru":
            print(f"Не удалось открыть ссылку, ошибка {e}")
        else:
            print(f"The link could not be opened due to an error {e}")
    _pause()


def convert_time(value, default_unit="m"):
    """
    Convert a time string into total seconds.

    Supported:
        121314       -> interpreted as minutes by default
        "121314m"   -> minutes
        "1h 40m 30s"
        "1ч 40м 30с"
        "1h 60m 30s" -> normalized to 2h 30s

    Returns:
        int: total seconds

    Raises:
        ValueError: invalid or empty input
    """
    if value is None:
        raise ValueError("Time value cannot be empty.")

    text = str(value).strip().lower()

    if not text:
        raise ValueError("Time value cannot be empty.")

    # Plain number = default unit
    if re.fullmatch(r"\d+(?:\.\d+)?", text):
        number = float(text)

        if number < 0:
            raise ValueError("Time cannot be negative.")

        units = {
            "s": 1,
            "m": 60,
            "h": 3600,
        }

        if default_unit not in units:
            raise ValueError(f"Unknown default unit: {default_unit}")

        return int(number * units[default_unit])

    # Replace Russian units with English ones
    text = text.replace("ч", "h")
    text = text.replace("м", "m")
    text = text.replace("с", "s")

    pattern = r"(\d+(?:\.\d+)?)\s*(h|m|s)"
    matches = re.findall(pattern, text)

    if not matches:
        raise ValueError("Invalid time format.")

    # Make sure the entire string was understood
    remaining = re.sub(pattern, "", text).strip()

    if remaining:
        raise ValueError(f"Invalid time format: {remaining}")

    total_seconds = 0

    for number, unit in matches:
        number = float(number)

        if unit == "h":
            total_seconds += int(number * 3600)
        elif unit == "m":
            total_seconds += int(number * 60)
        elif unit == "s":
            total_seconds += int(number)

    return total_seconds


def format_time(total_seconds):
    """
    Convert seconds into normalized human-readable time.

    Examples:
        3600  -> "1h"
        3630  -> "1h 30s"
        7200  -> "2h"
        7260  -> "2h 1m"
    """
    total_seconds = int(total_seconds)

    if total_seconds < 0:
        raise ValueError("Time cannot be negative.")

    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts = []

    if hours:
        parts.append(f"{hours}h")

    if minutes:
        parts.append(f"{minutes}m")

    if seconds:
        parts.append(f"{seconds}s")

    return " ".join(parts) if parts else "0s"


def normalize_time(value, default_unit="m"):
    """
    Convert any supported time format directly into normalized text.

    Example:
        "1ч 60м 30с" -> "2h 30s"
    """
    total_seconds = convert_time(value, default_unit)
    return format_time(total_seconds)


def settings_menu():
    logging.debug("Переход в меню настроек")
    while True:
        clear()
        update_text_variables()
        print(lang_settings_menu)
        # Пункты - это СПИСОК: номера выдаются по порядку, а не прописаны в коде.
        # Пункт "portable" есть только в портативной сборке, остальные номера сдвигаются сами.
        items = [("lang", lang_language_settings),
                 ("scheme", lang_settings_menu_scheme),
                 ("update", lang_update_settings),
                 ("custom", lang_interface_settings)]

        items += [("back", lang_back), ("exit", lang_exit)]
        print()
        for number, (item_key, item_label) in enumerate(items, start=1):
            print(f"{number}. {item_label}")

        answer = input(lang_choice).lower()
        if answer.isdigit() and 1 <= int(answer) <= len(items):
            action = items[int(answer) - 1][0]
        elif answer in ["lang", "l"]:
            action = "lang"
        elif answer == "update":
            action = "update"
        elif answer == "scheme":
            action = "scheme"
        elif answer == "custom":
            action = "custom"
        elif answer in ["9", "back", "b"]:
            action = "back"
        elif answer in ["0", "exit", "end", "e"]:
            action = "exit"
        elif answer in ["ru", "r", "ру", "р"]:
            language_setting('ru')
            continue
        elif answer == "en":
            language_setting('en')
            continue
        else:
            clear()
            print(f"{lang_error_input}")
            sleep(1)
            continue

        if action == "lang":
            language_settings()
        elif action == "scheme":
            logging.info("Переход в настройки схемы электропитания")
            setting_menu_scheme()
        elif action == "update":
            update_settings()
        elif action == "custom":
            interface_customization()
        elif action == "back":
            main_menu()
        elif action == "exit":
            end()
        break

def update_settings():
    while True:
        clear()
        print(lang_update_settings)
        print("\n1.", lang_beta_settings)
        if IS_PORTABLE:
            print("2.", _("Portable update format"))
            print("3.", lang_settings_menu)
            print("4.", lang_exit)
        else:
            print("2.", _("Update method"))
            print("3.", lang_settings_menu)
            print("4.", lang_exit)

        choice = input(lang_choice).lower()

        if choice == "1":
            beta_settings()
        if choice == "2" and IS_PORTABLE:
            portable_settings()
        if choice in ["4","9","back","b"] and IS_PORTABLE:
            settings_menu()
        if choice == "2" and not IS_PORTABLE:
            update_method()
        if choice in ["5","0","exit","end","e","stop","s"] and IS_PORTABLE:
            end()
        if choice in ["3","9","back","b"] and not IS_PORTABLE:
            settings_menu()
        if choice in ["4","0","exit","end","e","stop","s"] and not IS_PORTABLE:
            end()
        else:
            clear()
            print(lang_error_input)
            time.sleep(2)

def update_method():
    while True:
        clear()
        config = load_config()
        global emotes_support

        method = {
            "winget": "Winget",
            "github": "Github"
        }

        remembered = config.get("update_method_remember", False)
        selected_method = config.get("update_method")

        print(f"{_('Update method')}\n")
        print(
            f"{_('Remember the choice') + ":"} "
            f"{lang_enable if remembered else lang_disable}"
        )

        text_marker = "[✅ ]" if emotes_support else "[✓]"

        if remembered:
            method_name = method.get(
                selected_method,
                _('not selected')
            )
            marker = text_marker if selected_method in method else ""
            print(f"{_('Default method:')} {method_name}  {marker}".rstrip())

        print()

        items = [
            ("toggle", f"{lang_disable if remembered else lang_enable}"),
        ]

        if remembered:
            items.append(("method", _("Select default method")))

        items += [
            ("back", lang_back),
            ("exit", lang_exit),
        ]

        for number, (key, label) in enumerate(items, start=1):
            print(f"{number}. {label}")

        answer = input(lang_choice).lower().strip()

        if not answer.isdigit() or not (1 <= int(answer) <= len(items)):
            if answer in ("9", "back", "b"):
                action = "back"
            elif answer in ("0", "exit", "end", "e"):
                action = "exit"
            else:
                clear()
                logging.error(f"{log_error_input} update_method_settings")
                print(lang_error_input)
                sleep(1)
                continue
        else:
            action = items[int(answer) - 1][0]

        if action == "toggle":
            config["update_method_remember"] = not remembered
            if not config["update_method_remember"]:
                config["update_method"] = None
            save_config(config)

        elif action == "method":
            clear()
            print(f"{_('Select default method') + ":"}\n")

            method_items = list(method.items())

            for number, (key, label) in enumerate(method_items, start=1):
                # Маркер ставится ТОЛЬКО у выбранного формата,
                # а его вид зависит от режима эмодзи.
                if key == selected_method:
                    marker = " [✅ ]" if emotes_support else " [✓]"
                else:
                    marker = ""
                print(f"{number}. {label}{marker}")

            print(f"\n0. {lang_back}")

            choice = input(lang_choice).strip()

            if choice == "0":
                continue

            if choice.isdigit() and (1 <= int(choice) <= len(method_items)):
                config["update_method"] = method_items[int(choice) - 1][0]
                save_config(config)

        elif action == "back":
            update_settings()
            break

        elif action == "exit":
            end()
            break
        

def setting_menu_scheme():
    while True:
        clear()
        print(f"{lang_settings_menu_scheme}\n")
        print(lang_config_power_plan)
        powercfg_geta_sh()
        print(f"\n1. {lang_settings_timeout_monitor}")
        print("2.", lang_settings_time_sleep)
        print("3.", lang_settings_timeout_disk)
        print("5.", lang_back_main_menu)
        print("6.", lang_exit)

        choice = input(lang_choice).lower()
        if choice in ["5", "9", "back", "b"]:
            settings_menu()
            break
        elif choice in ["6", "0", "exit", "end", "e"]:
            end()
            break
        elif choice == "1":
            logging.info("Переход в настройки таймаута монитора")
            settings_timeout_monitor()
            break
        elif choice == "2":
            logging.info("Переход в настройки таймаута сна")
            settings_time_sleep()
            break
        elif choice == "3":
            logging.info("Переход в настройки таймаута диска")
            settings_timeout_disk()
            break
        elif choice == "4":
            logging.info("Переход в настройки интерфейса")
            interface_customization()
            break
        else:
            print(lang_error_input)
            sleep(1)


emotes_support = config.get("emotes_support", False)

def interface_customization():
    global emotes_support
    while True:
        clear()
        print(lang_interface_settings, "\n")
        # print(f"1. Color")
        print("1.", lang_interface_emotes, f"{lang_on if emotes_support else lang_off}")
        print(f"2. {lang_back_main_menu}")
        print(f"3. {lang_exit}")

        choice = input(lang_choice).lower().strip()

        if choice in ["4", "9", "back", "b"]:
            settings_menu()
            break
        elif choice in ["5", "0", "exit", "end", "e"]:
            end()
            break
        elif choice == "1":
            emotes_support = not emotes_support
            clear()
        elif choice == "2":
            settings_menu()
            break
        elif choice == "3":
            end()
            break
        else:
            clear()
            print(lang_error_input)
            sleep(1)

def settings_timeout_disk():
    while True:
        clear()
        print(f"{lang_settings_timeout_disk}\n")
        print(f"1. 0 {lang_minutes}")
        print(f"2. 10 {lang_minutes}")
        print(f"3. 15 {lang_minutes}")
        print(f"4. 20 {lang_minutes}")
        print(f"5. {lang_manual_input}")
        print(f"6. {lang_back_main_menu}")
        print(f"7. {lang_exit}")

        choice = input(lang_choice).lower()
        if choice in ["6", "9", "back", "b"]:
            setting_menu_scheme()
            break
        elif choice in ["7", "0", "exit", "end", "e"]:
            end()
            break
        elif choice == "1":
            settings_timeout_disk_sleep(0)
        elif choice == "2":
            settings_timeout_disk_sleep(10)
        elif choice == "3":
            settings_timeout_disk_sleep(15)
        elif choice == "4":
            settings_timeout_disk_sleep(20)
        elif choice == "5":
            settings_timeout_disk_sleep_manual()
            break
        else:
            clear()
            print(lang_error_input)
            sleep(1)
    setting_menu_scheme()

def settings_timeout_disk_sleep_manual():
    clear()
    while True:
        try:
            clear()
            print(f"{lang_manual_input} {lang_settings_timeout_disk}")
            timeout_input = input(f"\n{lang_enter_timeout_minutes} {Fore.LIGHTBLACK_EX}(10m, 1h 30м, 90s, 15ч):{Fore.WHITE} ")
            if timeout_input in ["back", "b"]:
                settings_timeout_disk()
                break
            elif timeout_input in ["exit", "end", "e"]:
                end()
                break
            total_seconds = convert_time(timeout_input, default_unit="m")
            timeout_minutes = total_seconds // 60

            subprocess.run(["powercfg", "/change", "disk-timeout-ac", str(timeout_minutes)], check=True)
            clear()
            print(f"{lang_settings_succesfull} {format_time(total_seconds)}.")
            logging.info(f"Disk timeout set to {timeout_input} = ({timeout_minutes}) minutes. {format_time(total_seconds)}")
            sleep(2)
            break
        except ValueError as e:
            clear()
            print(f"{Fore.RED}{lang_error_input}: {e}")
            logging.error(f"Invalid input for disk timeout: {e}")
            sleep(1)
        except subprocess.CalledProcessError as e:
            clear()
            print(f"{Fore.RED}Critical error: {e}")
            logging.error(f"Failed to set disk timeout: {e}")
            sleep(1)
    settings_timeout_disk()

def settings_timeout_disk_sleep(timeout_minutes):
    clear()
    try:
        subprocess.run(["powercfg", "/change", "disk-timeout-ac", str(timeout_minutes)], check=True)
        print(f"{lang_settings_succesfull} {timeout_minutes} {lang_minutes}.")
        logging.info(f"Disk timeout set to {timeout_minutes} minutes.")
        sleep(2)
    except subprocess.CalledProcessError as e:
        clear()
        print(f"{Fore.RED}Critical error: {e}")
        logging.error(f"Failed to set disk timeout: {e}")


def settings_time_sleep():
    while True:
        clear()
        print(f"{lang_settings_time_sleep}\n")
        print(f"1. 0 {lang_minutes}")
        print(f"2. 10 {lang_minutes}")
        print(f"3. 15 {lang_minutes}")
        print(f"4. 20 {lang_minutes}")
        print(f"5. {lang_manual_input}")
        print(f"6. {lang_back_main_menu}")
        print(f"7. {lang_exit}")

        choice = input(lang_choice).lower()
        if choice in ["6", "9", "back", "b"]:
            setting_menu_scheme()
            break
        elif choice in ["7", "0", "exit", "end", "e"]:
            end()
            break
        elif choice == "1":
            settings_timeout_sleep(0)
        elif choice == "2":
            settings_timeout_sleep(10)
        elif choice == "3":
            settings_timeout_sleep(15)
        elif choice == "4":
            settings_timeout_sleep(20)
        elif choice == "5":
            settings_timeout_sleep_manual()
            break
        else:
            clear()
            print(lang_error_input)
            sleep(1)
    setting_menu_scheme()

def settings_timeout_sleep_manual():
    clear()
    while True:
        try:
            clear()
            print(f"{lang_manual_input} {lang_settings_time_sleep}")
            timeout_input = input(f"\n{lang_enter_timeout_minutes} {Fore.LIGHTBLACK_EX}(10m, 1h 30м, 90s, 15ч):{Fore.WHITE} ")
            if timeout_input in ["back", "b"]:
                settings_time_sleep()
                break
            elif timeout_input in ["exit", "end", "e"]:
                end()
                break
            total_seconds = convert_time(timeout_input, default_unit="m")
            timeout_minutes = total_seconds // 60

            subprocess.run(["powercfg", "/change", "standby-timeout-ac", str(timeout_minutes)], check=True)
            clear()
            print(f"{lang_settings_succesfull} {format_time(total_seconds)}.")
            logging.info(f"Sleep timeout set to {timeout_input} = ({timeout_minutes}) minutes. {format_time(total_seconds)}")
            sleep(2)
            break
        except ValueError as e:
            clear()
            print(f"{Fore.RED}{lang_error_input}: {e}")
            logging.error(f"Invalid input for sleep timeout: {e}")
            sleep(1)
        except subprocess.CalledProcessError as e:
            clear()
            print(f"{Fore.RED}Critical error: {e}")
            logging.error(f"Failed to set sleep timeout: {e}")
            sleep(1)
    settings_time_sleep()

def settings_timeout_sleep(timeout_minutes):
    clear()
    try:
        subprocess.run(["powercfg", "/change", "standby-timeout-ac", str(timeout_minutes)], check=True)
        print(f"{lang_settings_succesfull} {timeout_minutes} {lang_minutes}.")
        logging.info(f"Sleep timeout set to {timeout_minutes} minutes.")
        sleep(2)
    except subprocess.CalledProcessError as e:
        clear()
        print(f"{Fore.RED}Critical error: {e}")
        logging.error(f"Failed to set sleep timeout: {e}")


def settings_timeout_monitor():
    while True:
        clear()
        print(f"{lang_settings_timeout_monitor}\n")
        print(f"1. 0 {lang_minutes}")
        print(f"2. 10 {lang_minutes}")
        print(f"3. 15 {lang_minutes}")
        print(f"4. 20 {lang_minutes}")
        print(f"5. {lang_manual_input}")
        print(f"6. {lang_back_main_menu}")
        print(f"7. {lang_exit}")

        choice = input(lang_choice).lower()
        if choice in ["6", "9", "back", "b"]:
            setting_menu_scheme()
            break
        elif choice in ["7", "0", "exit", "end", "e"]:
            end()
            break
        elif choice == "1":
            settings_timeout_monitor_sleep(0)
        elif choice == "2":
            settings_timeout_monitor_sleep(10)
        elif choice == "3":
            settings_timeout_monitor_sleep(15)
        elif choice == "4":
            settings_timeout_monitor_sleep(20)
        elif choice == "5":
            settings_timeout_monitor_sleep_manual()
            break
        else:
            clear()
            print(lang_error_input)
            sleep(1)

def settings_timeout_monitor_sleep(timeout_minutes):
    clear()
    try:
        subprocess.run(["powercfg", "/change", "monitor-timeout-ac", str(timeout_minutes)], check=True)
        print(f"{lang_settings_succesfull} {timeout_minutes} {lang_minutes}.")
        logging.info(f"Monitor timeout set to {timeout_minutes} minutes.")
        sleep(2)
    except subprocess.CalledProcessError as e:
        clear()
        print(f"{Fore.RED}Critical error: {e}")
        logging.error(f"Failed to set monitor timeout: {e}")

def settings_timeout_monitor_sleep_manual():
    clear()
    while True:
        try:
            clear()
            print(f"{lang_manual_input} {lang_settings_timeout_monitor}")
            timeout_input = input(f"\n{lang_enter_timeout_minutes} {Fore.LIGHTBLACK_EX}(10m, 1h 30м, 90s, 15ч):{Fore.WHITE} ")
            if timeout_input in ["back", "b"]:
                settings_timeout_monitor()
                break
            elif timeout_input in ["exit", "end", "e"]:
                end()
                break
            total_seconds = convert_time(timeout_input, default_unit="m")
            timeout_minutes = total_seconds // 60

            subprocess.run(["powercfg", "/change", "monitor-timeout-ac", str(timeout_minutes)], check=True)
            clear()
            print(f"{lang_settings_succesfull} {format_time(total_seconds)}.")
            logging.info(f"Monitor timeout set to {timeout_input} = ({timeout_minutes}) minutes. {format_time(total_seconds)}")
            sleep(2)
            break
        except ValueError as e:
            clear()
            print(f"{Fore.RED}{lang_error_input}: {e}")
            logging.error(f"Invalid input for monitor timeout: {e}")
            sleep(1)
        except subprocess.CalledProcessError as e:
            clear()
            print(f"{Fore.RED}Critical error: {e}")
            logging.error(f"Failed to set monitor timeout: {e}")
            sleep(1)
    settings_timeout_monitor()


def setting_menu_scheme_page2(): # not ready yet
    while True:
        clear()
        print(f"{lang_settings_menu_scheme}\n")
        print(lang_config_power_plan)
        powercfg_geta_sh()
        # print(f"\n1. {lang_}")
        # print("2.", lang_)
        # print("3.", lang_battery_report) # /BATTERYREPORT
        # print("4.", lang_settings_hibernate) # powercfg /systempowerreport
        # print("5.", lang_)
        # print("6.", lang_next)



def language_settings():
    global current_lang
    logging.debug("Переход в меню настроек выбора языка")
    while True:
        clear()
        config = load_config()
        auto_language = config.get("auto_language", True)
        current_lang = config.get("language", "en")
        update_text_variables()

        lang_display = "Русский" if current_lang == "ru" else "English"
        auto_status = f"{Fore.GREEN}ON" if auto_language else f"{Fore.RED}OFF"

        print(f"{lang_current_language}: {lang_display}")
        print(f"{lang_auto_language_setting}: {auto_status}")
        print(f"\n{lang_select_language}")
        print("1. Русский")
        print("2. English")
        if not auto_language:
            print(f"3. {lang_enable} {lang_auto_language_setting}")
        else:
            print(f"3. {lang_disable} {lang_auto_language_setting}")
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
            config = load_config()
            config["auto_language"] = not config.get("auto_language", True)
            
            if config["auto_language"]:
                system_lang = get_system_lang()
                config["language"] = system_lang
                save_config(config)
                setup_localization(system_lang)
                update_text_variables()
                clear()
                logging.info(f"Автоопределение языка включено, системный язык: {system_lang}")
            else:
                save_config(config)
                current_lang = config.get("language", "en")
                setup_localization(current_lang)
                update_text_variables()
                clear()
                logging.info("Автоопределение языка отключено")
        elif select_language in ["4", "9", "back", "b"]:
            settings_menu()
            break
        elif select_language in ["0", "5", "exit", "end", "e"]:
            end()
            break
        else:
            clear()
            logging.error(f"{log_error_input} {lang_language_settings}")
            print(f"{Fore.RED} {lang_error_input}")
            sleep(1)


def beta_settings():
    while True:
        clear()
        config = load_config()
        include_beta = config.get("include_beta", False)
        print(lang_beta_settings)
        if include_beta:
            print(f"\n1. {lang_disable} {lang_beta_updates}")
        else:
            print(f"\n1. {lang_enable} {lang_beta_updates}")
        print(f"2. {lang_back}")
        print(f"3. {lang_exit}")

        beta_settings = input(lang_choice).lower()
        if beta_settings == "1":
            config = load_config()
            config["include_beta"] = not config.get("include_beta", False)
            if save_config(config):
                if config["include_beta"]:
                    clear()
                    print(lang_enable, lang_beta_updates)
                else:
                    clear()
                    print(lang_disable, lang_beta_updates)
            sleep(1)
        elif beta_settings in ["9", "2", "back", "b"]:
            update_settings()
            break
        elif beta_settings in ["0", "3", "exit", "end", "e"]:
            end()
            break
        else:
            clear()
            logging.error(f"{log_error_input} {lang_beta_settings}")
            print(lang_error_input)
            sleep(1)

def portable_settings():
    """Настройки формата portable-обновления."""
    global emotes_support

    formats = {
        ".zip": "ZIP",
        ".7z": "7-Zip",
        ".rar": "RAR",
    }

    while True:
        clear()
        config = load_config()

        remembered = config.get("portable_remember", False)
        selected_format = config.get("portable_choice")

        print(f"{_('Portable update format')}\n")
        print(
            f"{_('Remember format:')} "
            f"{lang_enable if remembered else lang_disable}"
        )

        text_marker = "[✅ ]" if emotes_support else "[✓]"

        if remembered:
            format_name = formats.get(
                selected_format,
                _('not selected')
            )
            marker = text_marker if selected_format in formats else ""
            print(f"{_('Default format:')} {format_name}  {marker}".rstrip())

        print()

        items = [
            ("toggle", f"{lang_disable if remembered else lang_enable}"),
        ]

        if remembered:
            items.append(("format", _("Select default format")))

        items += [
            ("back", lang_back),
            ("exit", lang_exit),
        ]

        for number, (key, label) in enumerate(items, start=1):
            print(f"{number}. {label}")

        answer = input(lang_choice).lower().strip()

        if not answer.isdigit() or not (1 <= int(answer) <= len(items)):
            if answer in ("9", "back", "b"):
                action = "back"
            elif answer in ("0", "exit", "end", "e"):
                action = "exit"
            else:
                clear()
                logging.error(f"{log_error_input} portable_settings")
                print(lang_error_input)
                sleep(1)
                continue
        else:
            action = items[int(answer) - 1][0]

        if action == "toggle":
            config["portable_remember"] = not remembered
            if not config["portable_remember"]:
                config["portable_choice"] = None
            save_config(config)

        elif action == "format":
            clear()
            print(f"{_('Select default format') + ":"}\n")

            format_items = list(formats.items())

            for number, (key, label) in enumerate(format_items, start=1):
                # Маркер ставится ТОЛЬКО у выбранного формата,
                # а его вид зависит от режима эмодзи.
                if key == selected_format:
                    marker = " [✅ ]" if emotes_support else " [✓]"
                else:
                    marker = ""
                print(f"{number}. {label}{marker}")

            print(f"\n0. {lang_back}")

            choice = input(lang_choice).strip()

            if choice == "0":
                continue

            if choice.isdigit() and (1 <= int(choice) <= len(format_items)):
                config["portable_choice"] = format_items[int(choice) - 1][0]
                save_config(config)

        elif action == "back":
            update_settings()
            break

        elif action == "exit":
            end()
            break

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
            logging.info("Переход в главное меню")
            main_menu()
            break
        elif automode in ["0", "5", "exit", "end", "e"]:
            end()
            break
        else:
            logging.error(f"{log_error_input} {lang_autoConfiguration}")
            print(f"{lang_error_input}")
            sleep(1)

def _delete_all_other_schemes(keep_guid):
    keep_guid = keep_guid.lower()
    schemes = powercfg_list_get()
    if schemes is None:
        raise RuntimeError("Не удалось получить список схем перед удалением")

    deleted = []
    failed = []

    for guid in sorted(schemes):
        if guid.lower() == keep_guid:
            continue

        try:
            _powercfg_run(['-delete', guid])
            deleted.append(guid)
            logging.info(f"Deleted power scheme: {guid}")
        except subprocess.CalledProcessError as e:
            failed.append(guid)
            logging.error(
                f"Не удалось удалить схему {guid}: "
                f"returncode={e.returncode}, stdout={getattr(e, 'stdout', '')!r}, "
                f"stderr={getattr(e, 'stderr', '')!r}"
            )

    remaining = powercfg_list_get()
    if remaining is None:
        raise RuntimeError("Не удалось проверить список схем после удаления")

    unexpected = {g for g in remaining if g.lower() != keep_guid}
    if unexpected:
        logging.warning(f"После очистки остались схемы: {sorted(unexpected)}")

    if failed:
        logging.warning(f"Не удалось удалить схемы: {sorted(failed)}")

    return deleted, failed, remaining


def automode1():
    logging.info("Переход в меню настройки режима: " + str(lang_max_performance))
    clear()
    print(loading1)

    scheme_before = get_powercfg_list()
    if not scheme_before:
        logging.warning("Не удалось получить исходный список схем или список пуст")

    try:
        # 1. Ensure Maximum Performance exists.
        #    If Windows does not have the Ultimate Performance template,
        #    duplicate it and use the GUID actually returned by powercfg.
        actual_guid = _ensure_scheme("e9a42b02-d5df-448d-aa00-03f14749eb61")

        clear()
        print(loading2)


        # 2. It must be active before deleting all other schemes.
        _activate_scheme_guid(actual_guid)

        clear()
        print(loading3)

        # 3. Automode 1 intentionally leaves ONLY Maximum Performance.
        deleted, failed, remaining = _delete_all_other_schemes(actual_guid)

        clear()
        print(lang_result_before)
        print(scheme_before)
        print(f"\n{lang_result_after}")
        powercfg_list()

        logging.info(
            f"Automatic mode activated: {lang_max_performance}; "
            f"GUID={actual_guid}; deleted={deleted}; failed={failed}; "
            f"remaining={sorted(remaining)}"
        )

        _pause()
        automode1_end_menu()
    except subprocess.CalledProcessError as e:
        clear()
        logging.error(
            f"{log_error_automode} {lang_max_performance}: "
            f"returncode={e.returncode}, stdout={getattr(e, 'stdout', '')!r}, "
            f"stderr={getattr(e, 'stderr', '')!r}",
            exc_info=True
        )
        print(f"{Fore.RED}{lang_error_automode}")
        print(f"{Fore.RED}powercfg: {(getattr(e, 'stderr', '') or getattr(e, 'stdout', '') or str(e)).strip()}")
        sleep(3)
    except Exception as e:
        clear()
        logging.error(f"{log_error_automode} {lang_max_performance}: {e}", exc_info=True)
        print(f"{Fore.RED}{lang_error_automode}")
        print(f"{Fore.RED}{e}")
        sleep(3)

def automode1_end_menu():
    while True:
        clear()
        powercfg_list()
        print(f"\n1. {lang_back_main_menu}")
        print(f"2. {lang_exit}")

        autoend1 = input(lang_choice).lower()
        if autoend1 in ["1", "9", "back", "b"]:
            main_menu()
            break
        elif autoend1 in ["2", "0", "exit", "end", "e"]:
            end()
            break
        else:
            logging.error(f"{log_error_input} {lang_autoConfiguration} {lang_max_performance}")
            print(f"{lang_error_input}")
            sleep(1)

def automode2():
    logging.info("Переход в меню настройки режима: " + str(lang_balanced))
    clear()
    print(loading1)

    scheme_before = get_powercfg_list()
    if not scheme_before:
        logging.warning("Не удалось получить исходный список схем или список пуст")

    try:
        # Do NOT restore defaults here. Restoring on every mode switch was the
        # main reason schemes appeared/disappeared and custom plans were lost.
        actual_guid = _ensure_scheme("381b4222-f694-41f0-9685-ff5bb260df2e")

        clear()
        print(loading2)

        _activate_scheme_guid(actual_guid)

        clear()
        print(loading3)

        # Keep only the scheme selected by this automatic mode.
        deleted, failed, remaining = _delete_all_other_schemes(actual_guid)

        clear()
        print(lang_result_before)
        print(scheme_before)
        print(f"\n{lang_result_after}")
        powercfg_list()
        logging.info(
            f"Automatic mode activated: {lang_balanced}; "
            f"GUID={actual_guid}; deleted={deleted}; failed={failed}; "
            f"remaining={sorted(remaining)}"
        )
        _pause()
        automode2_end_menu()
    except subprocess.CalledProcessError as e:
        clear()
        logging.error(f"{log_error_automode} {lang_balanced}: {e}", exc_info=True)
        print(f"{Fore.RED}{lang_error_automode}")
        print(f"{Fore.RED}powercfg: {(getattr(e, 'stderr', '') or getattr(e, 'stdout', '') or str(e)).strip()}")
        sleep(3)
    except Exception as e:
        clear()
        logging.error(f"{log_error_automode} {lang_balanced}: {e}", exc_info=True)
        print(f"{Fore.RED}{lang_error_automode}")
        print(f"{Fore.RED}{e}")
        sleep(3)

def automode2_end_menu():
    while True:
        clear()
        powercfg_list()
        print(f"\n1. {lang_back_main_menu}")
        print(f"2. {lang_exit}")

        autoend2 = input(lang_choice).lower()
        if autoend2 in ["1", "9", "back", "b"]:
            main_menu()
            break
        elif autoend2 in ["2", "0", "exit", "end", "e"]:
            end()
            break
        else:
            logging.error(f"{log_error_input} {lang_autoConfiguration} {lang_balanced}")
            print(f"{lang_error_input}")
            sleep(1)

def automode3():
    logging.info("Переход в меню настройки режима: " + str(lang_powersave))
    clear()
    print(loading1)

    scheme_before = get_powercfg_list()
    if not scheme_before:
        logging.warning("Не удалось получить исходный список схем или список пуст")

    try:
        # Do NOT restore defaults here. Restoring on every mode switch was the
        # main reason schemes appeared/disappeared and custom plans were lost.
        actual_guid = _ensure_scheme("a1841308-3541-4fab-bc81-f71556f20b4a")

        clear()
        print(loading2)

        _activate_scheme_guid(actual_guid)

        clear()
        print(loading3)

        # Keep only the scheme selected by this automatic mode.
        deleted, failed, remaining = _delete_all_other_schemes(actual_guid)

        clear()
        print(lang_result_before)
        print(scheme_before)
        print(f"\n{lang_result_after}")
        powercfg_list()
        logging.info(
            f"Automatic mode activated: {lang_powersave}; "
            f"GUID={actual_guid}; deleted={deleted}; failed={failed}; "
            f"remaining={sorted(remaining)}"
        )
        _pause()
        automode3_end_menu()
    except subprocess.CalledProcessError as e:
        clear()
        logging.error(f"{log_error_automode} {lang_powersave}: {e}", exc_info=True)
        print(f"{Fore.RED}{lang_error_automode}")
        print(f"{Fore.RED}powercfg: {(getattr(e, 'stderr', '') or getattr(e, 'stdout', '') or str(e)).strip()}")
        sleep(3)
    except Exception as e:
        clear()
        logging.error(f"{log_error_automode} {lang_powersave}: {e}", exc_info=True)
        print(f"{Fore.RED}{lang_error_automode}")
        print(f"{Fore.RED}{e}")
        sleep(3)

def automode3_end_menu():
    while True:
        clear()
        powercfg_list()
        print(f"\n1. {lang_back_main_menu}")
        print(f"2. {lang_exit}")

        autoend3 = input(lang_choice).lower()
        if autoend3 in ["1", "9", "back", "b"]:
            main_menu()
            break
        elif autoend3 in ["2", "0", "exit", "end", "e"]:
            end()
            break
        else:
            logging.error(f"{log_error_input} {lang_autoConfiguration} {lang_powersave}")
            print(f"{lang_error_input}")
            sleep(1)

if __name__ == "__main__":
    config = apply_language_from_config()
    check_os()