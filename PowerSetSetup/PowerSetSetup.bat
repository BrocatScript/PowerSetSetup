@echo off
chcp 65001 > nul

::Сreator - BrocatScript
title Creator BrocatScript

::PowerSetSetup
title PowerSetSetup

::Версия PowerSetSetup
set "version=1.0.1fix"

::Coming soon 1.0.2 :]

::System color
for /f %%x in ('echo prompt $E ^| cmd') do set "COLOR=%%x"

::color
set "BLACK=%COLOR%[30m"
set "RED=%COLOR%[31m"
set "GREEN=%COLOR%[32m"
set "YELLOW=%COLOR%[33m"
set "BLUE=%COLOR%[34m"
set "MAGENTA=%COLOR%[35m"
set "CYAN=%COLOR%[36m"
set "WHITE=%COLOR%[37m"

::reset color
set "RESET=%COLOR%[0m"

::Launguage System
set "CONFIG_FILE=PowerSetSetup_Data\Language.ini"

if not exist "PowerSetSetup_Data" mkdir "PowerSetSetup_Data"

::Clear variable first
set "CURRENT_LANG="

:: Load configuration
if exist "%CONFIG_FILE%" (
    for /f "tokens=2 delims==" %%b in ('findstr "language" "%CONFIG_FILE%"') do set "CURRENT_LANG=%%b"
)

::Remove any spaces or special characters
set "CURRENT_LANG=%CURRENT_LANG: =%"

::If no language found or invalid, set to Русский
if not "%CURRENT_LANG%"=="en" set "CURRENT_LANG=ru"

::Load the appropriate language
if "%CURRENT_LANG%"=="en" goto :language_en
goto :language_ru

:language_ru
call :language_ru_reload
goto :main_menu

:language_en
call :language_en_reload
goto :main_menu

::Перевод
:language_ru_reload
set "lang_addPowerPlanInfo=%RED%ВНИМАНИЕ! Доступно для добавления: только %WHITE%(Максимальная производительность)!%RESET%"
set "lang_error_input=%RED%ОШИБКА: Сообщение написано неправильно или его нет! %WHITE%Попробуйте снова!%RESET%"
set "lang_scheme_warning=%RED%ВНИМАНИЕ! После выбора схемы электропитания все остальные будут удалены!%RESET%"
set "lang_choice=Введите номер: "
set "lang_main_menu=Вернуться в главное меню"
set "lang_settings=Вернуться в расширенные параметры"
set "lang_exit=Выйти"
set "lang_max_performance=Максимальная производительность"
set "lang_performance=Высокая производительность"
set "lang_balanced=Сбалансированная"
set "lang_powersave=Экономия энергии"
set "lang_change_language=Сменить язык"
set "lang_current_language=Текущий язык: Русский"
set "lang_select_language=Выберите язык:"
set "lang_russian=Русский"
set "lang_english=English"
set "lang_settings_menu=Настройки"
set "lang_language_settings=Настройки языка"
set "lang_menu_title=Главное меню"
set "lang_advancedSettings=Расширенные параметры"
set "lang_autoConfiguration=Автоматическая настройка"
set "lang_system_show_info=Показать системную информацию"
set "lang_test_pc=Тест производительности"
set "lang_check_update_main=Проверить обновления"
set "lang_check_update=Проверка обновлений"
set "lang_error_check_update=ОШИБКА: Не удалось проверить обновления!"
set "lang_info=О программе"
set "lang_system_info=Системная информация"
set "lang_about=О программе"
set "lang_author=Автор: BrocatScript"
set "lang_supportdeveloper=Поддержать разработчика"
set "lang_version=Текущая версия: "
set "lang_latest_version=Последняя версия: "
set "lang_new_release=Доступна новая версия: "
set "lang_download_update=Скачать обновелние"
set "lang_skip_update=Продолжить без обновления"
set "lang_system_latest_version=У вас %GREEN%последняя%RESET% версия!"
set "lang_open_page=Открываю страницу"
set "lang_choose_required_mode=Выберите нужный режим"
set "lang_max_power_consumption=Максимальное энергопотребление"
set "lang_balans_consumption=Баланс электропотребления"
set "lang_low_power=Снижает энергопотребление батареи"
set "lang_result_before=%CYAN%Результат до:%RESET%"
set "lang_result_after=%CYAN%Результат после:%RESET%"
set "lang_result=%CYAN%Результат:%RESET%"
set "lang_delete_scheme=Удалить схему"
set "lang_reset_scheme=Сбросить схемы"
set "lang_add_scheme=Добавить схему"
set "lang_activate_scheme=Активировать схему"
set "lang_list_scheme=Узнать список схем"
set "lang_manual_input=Ручной ввод"
set "lang_back=Вернуться назад"
set "lang_error_balanced_scheme_not_found=%RED%ОШИБКА: Схема "Сбалансированая" не найдена!%RESET%"
set "lang_balanced_scheme_activated=Схема "Сбалансированая" активирована!"
set "lang_error_performance_scheme_not_found=%RED%ОШИБКА: Схема "Высокая производительность" не найдена!%RESET%"
set "lang_perfomance_scheme_activated=Схема "Высокая производительность" активирована!"
set "lang_max_perfomance_scheme_not_found=%RED%Схема "Максимальная производительность" не найдена!%RESET%"
set "lang_max_perfomance_scheme_activated=Схема "Максимальная производительность" активирована!"
set "lang_low_power_scheme_not_found=%RED%Схема "Экономия энергии" не найдена!%RESET%"
set "lang_low_power_scheme_activated=Схема "Экономия энергии" активирована!%RESET%"
set "lang_enter_id_power_scheme=Введите ID схемы электропитания: "
set "lang_error_id_power_scheme=%RED%ОШИБКА: Схема с ID %WHITE%%id_select_sh_send%%RED% не найдена!%RESET%"
set "lang_id_power_scheme_activated=Схема %id_select_sh_send% активирована!"
set "lang_error_add_max_power_scheme=%RED%ОШИБКА: Не удалось добавить схему электропитания %WHITE%"Максимальная производительность"!%RESET%"
set "lang_max_power_scheme_added=Схема "Максимальная производительность" успешно добавлена!"
set "lang_what_delet_scheme=Что вы хотите удалить?"
set "lang_balanced_scheme_deleted=Схема "Сбалансированная" успешно удалена!"
set "lang_perfomance_scheme_deleted=Схема "Высокая производительность" успешно удалена!%RESET%"
set "lang_max_perfomance_scheme_deleted=Схема "Максимальная производительность" успешно удалена!"
set "lang_low_power_scheme_deleted=Схема "Экономия энергии" успешно удалена!"
set "lang_scheme_succesfull_deleted=Схема успешно удалена!"
set "lang_error_back_main_menu=%RED%ОШИБКА! Вы не можете вернуться назад, так как это главное меню.%RESET%"
set "lang_back_select_delet_scheme=Вернуться к выбору удаления схем?"
set "lang_settings_succesfull=Успешно!"
set "lang_error_timeout_0_minutes=%RED%Ошибка: невозможно выставить%CYAN% 0 минут!%RESET%"
set "lang_error_timeout_10_minutes=%RED%Ошибка: невозможно выставить%CYAN% 10 минут!%RESET%"
set "lang_error_timeout_15_minutes=%RED%Ошибка: невозможно выставить%CYAN% 15 минут!%RESET%"
set "lang_error_timeout_20_minutes=%RED%Ошибка: невозможно выставить%CYAN% 20 минут!%RESET%"
set "lang_enter_timeout_minutes=Укажите время отключения дисплея: "
set "lang_error_send_timeout_minutes=%RED%Ошибка: невозможно задать время отключения %CYAN%"%time_timeout_monitor%"%RESET%"
set "lang_minutes=минут"
set "lang_settings_menu_scheme=Расширенные настройки схем"
set "lang_settings_timeout_monitor=Время выключения дисплея"
set "lang_settings_time_sleep=Время перехода в спящий режим"
set "lang_settings_timeout_disk=Время выключения жесткого диска"
set "lang_config_power_plan=Текущие настройки схемы питания"
set "lang_beta_settings=Настройки beta-версий"
set "lang_beta_enabled=Beta-версии обновлений %CYAN%включены%RESET%"
set "lang_beta_disabled=Beta-обновления %CYAN%выключены%RESET%"
set "lang_enable_beta=%CYAN%Включить%RESET% beta-версии обновлений"
set "lang_disable_beta=%CYAN%Выключить%RESET% beta-версии обновлений"
set "lang_settings_saved=Настройки сохранены"
set "lang_fix_update=Доступно исправление для этого обновления:"
set "lang_beta_update=Доступно beta-обновление:"
goto :eof

:language_en_reload
set "lang_addPowerPlanInfo=%RED%WARNING: Available to add: only %CYAN%(Ultimate Performance)!%RESET%"
set "lang_error_input=%RED%ERROR: The message is written incorrectly or it is empty! %WHITE%Try again!%RESET%"
set "lang_scheme_warning=%RED%WARNING: All other power plans will be deleted after you select one!%RESET%"
set "lang_choice=Enter the number: "
set "lang_main_menu=Back to main menu"
set "lang_settings=Back to Advanced Settings"
set "lang_exit=Exit"
set "lang_max_performance=Maximum performance"
set "lang_performance=High performance"
set "lang_balanced=Balanced"
set "lang_powersave=Power saving"
set "lang_change_language=Change language"
set "lang_current_language=Current language: English"
set "lang_select_language=Select language:"
set "lang_russian=Русский"
set "lang_english=English"
set "lang_settings_menu=Settings"
set "lang_language_settings=Language settings"
set "lang_menu_title=Main Menu"
set "lang_advancedSettings=Advanced settings"
set "lang_autoConfiguration=Automatic configuration"
set "lang_system_show_info=Show system information"
set "lang_test_pc=Performance test"
set "lang_check_update_main=Check for updates"
set "lang_check_update=Update check"
set "lang_error_check_update=ERROR: Update check failed!"
set "lang_info=About"
set "lang_system_info=System information"
set "lang_test_perf=Performance test"
set "lang_about=About"
set "lang_author=Author: BrocatScript"
set "lang_supportdeveloper=Support the developer"
set "lang_version=Current version: "
set "lang_latest_version=Latest version "
set "lang_new_release=New version available: "
set "lang_download_update=Download update"
set "lang_skip_update=Skip update"
set "lang_system_latest_version=You have the %GREEN%latest%RESET% version!"
set "lang_open_page=Opening the page"
set "lang_choose_required_mode=Choose the required mode"
set "lang_max_power_consumption=Maximum power consumption"
set "lang_balans_consumption=Power consumption balance"
set "lang_low_power=Lowers battery consumption"
set "lang_result_before=%CYAN%Result before:%RESET%"
set "lang_result_after=%CYAN%Result after:%RESET%"
set "lang_result=%CYAN%Result:%RESET%"
set "lang_delete_scheme=Delete the scheme"
set "lang_reset_scheme=Reset the schemes"
set "lang_add_scheme=Add a scheme"
set "lang_activate_scheme=Activate the scheme"
set "lang_list_scheme=List all schemes"
set "lang_manual_input=Manual input"
set "lang_back=Go back"
set "lang_error_balanced_scheme_not_found=%RED%ERROR: Scheme "Balanced" not found!%RESET%"
set "lang_balanced_scheme_activated=Scheme "Balanced" activated!"
set "lang_error_performance_scheme_not_found=%RED%ERROR: Scheme "High performance" not found!%RESET%"
set "lang_perfomance_scheme_activated=Scheme "High performance" activated!"
set "lang_max_perfomance_scheme_not_found=%RED%ERROR: Scheme "Maximum performance" not found!%RESET%"
set "lang_max_perfomance_scheme_activated=Scheme "Maximum performance" activated!"
set "lang_low_power_scheme_not_found=%RED%Scheme "Power saving" not found!%RESET%"
set "lang_low_power_scheme_activated=Scheme "Power saving" activated!"
set "lang_enter_id_power_scheme=Enter the power scheme ID: "
set "lang_error_id_power_scheme=%RED%ERROR: Scheme with ID %WHITE%%id_select_sh_send%%RED% not found!%RESET%"
set "lang_id_power_scheme_activated=Scheme %id_select_sh_send% activated!"
set "lang_error_add_max_power_scheme=%RED%ERROR: Failed to add the power scheme %WHITE%"Maximum Performance"!%RESET%"
set "lang_max_power_scheme_added=Scheme "Maximum Performance" successfully added!"
set "lang_what_delet_scheme=What do you want to delete?"
set "lang_balanced_scheme_deleted=Scheme "Balanced" successfully deleted!"
set "lang_perfomance_scheme_deleted=Scheme "High performance" succesfull deleted!"
set "lang_max_perfomance_scheme_deleted=Scheme "Maximum performance" succesfull deleted!"
set "lang_low_power_scheme_deleted=Scheme "Power saving" succesfull deleted!"
set "lang_scheme_succesfull_deleted=Scheme successfully deleted!"
set "lang_error_back_main_menu=%RED%ERROR! You cannot go back because this is the main menu.%RESET%"
set "lang_back_select_delet_scheme=Go back to select which scheme to delete?"
set "lang_settings_succesfull=Succesfull!"
set "lang_error_timeout_0_minutes=%RED%Error: Cannot set%CYAN% 0 minutes!%RESET%"
set "lang_error_timeout_10_minutes=%RED%Error: Cannot set%CYAN% 10 minutes!%RESET%"
set "lang_error_timeout_15_minutes=%RED%Error: Cannot set%CYAN% 15 minutes!%RESET%"
set "lang_error_timeout_20_minutes=%RED%Error: Cannot set%CYAN% 20 minutes!%RESET%"
set "lang_enter_timeout_minutes=Set the display turn‑off time: "
set "lang_error_send_timeout_minutes=%RED%Error: Cannot set shutdown time to %CYAN%"%time_timeout_monitor%"%RESET%"
set "lang_minutes=minutes"
set "lang_settings_menu_scheme=Advanced scheme settings"
set "lang_settings_timeout_monitor=Display off time"
set "lang_settings_time_sleep=Time to enter sleep mode"
set "lang_settings_timeout_disk=Hard disk shutdown time"
set "lang_config_power_plan=Current power supply circuit settings"
set "lang_beta_settings=Beta Version Settings"
set "lang_beta_enabled=Beta updates %CYAN%enabled%RESET%"
set "lang_beta_disabled=Beta updates %CYAN%disabled%RESET%"
set "lang_enable_beta=%CYAN%Enable%RESET% beta updates"
set "lang_disable_beta=%CYAN%Disable%RESET% beta updates"
set "lang_settings_saved=Settings saved"
set "lang_fix_update=A fix for the update is available:"
set "lang_beta_update=Beta update available:"
goto :eof

::Reload language function
:reload_language
if "%CURRENT_LANG%"=="en" goto :language_en_reload
goto :language_ru_reload

::Главное меню
:main_menu
cls
timeout /t 1 > nul
powercfg /l
echo.
echo %lang_menu_title%
echo 1. %lang_autoConfiguration%
echo 2. %lang_advancedSettings%
echo 3. %lang_check_update_main%
echo 4. %lang_supportdeveloper%
echo 5. %lang_settings_menu%
echo 6. %lang_exit%
set /p choice="%lang_choice%"
if "%choice%" == "1" goto :menu_yes
if "%choice%" == "2" goto :menu_not
if "%choice%" == "3" goto :check_update
if "%choice%" == "4" goto :donat
if "%choice%" == "5" goto :settings_menu
if "%choice%" == "6" goto :end
if /i "%choice%" == "update" goto :check_update
if /i "%choice%" == "virus" goto :virus
if /i "%choice%" == "donat" goto :donat
if /i "%choice%" == "exit" goto :end
if /i "%choice%" == "stop" goto :end
if /i "%choice%" == "back" goto :back
if /i "%choice%" == "end" goto :end
if /i "%choice%" == "not" goto :menu_not
if /i "%choice%" == "нет" goto :menu_not
if /i "%choice%" == "yes" goto :menu_yes
if /i "%choice%" == "d" goto :donat
if /i "%choice%" == "e" goto :end
if /i "%choice%" == "да" goto :menu_yes
if /i "%choice%" == "b" goto :back
if /i "%choice%" == "u" goto :check_update
if /i "%choice%" == "y" goto :menu_yes
if /i "%choice%" == "д" goto :menu_yes
if /i "%choice%" == "s" goto :end
if /i "%choice%" == "n" goto :menu_not
if /i "%choice%" == "н" goto :menu_not

cls
echo %lang_error_input%
timeout /t 2 > nul
cls
goto :main_menu

:donat
start "" "https://pay.cloudtips.ru/p/0cdee068"
powershell -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('Благодарим за поддержку! Thank you for your support!', 'PowerSetSetup', 'OK', 'Information')"
goto :main_menu

:settings_menu
cls
echo 1. %lang_change_language%
echo 2. %lang_settings_menu_scheme%
echo 3. %lang_main_menu%
echo 4. %lang_exit%
set /p settings_menu_choice="%lang_choice%"
if "%settings_menu_choice%" == "1" goto :language_settings
if "%settings_menu_choice%" == "2" goto :settings_menu_scheme
if "%settings_menu_choice%" == "3" goto :main_menu
if "%settings_menu_choice%" == "4" goto :end
if /i "%settings_menu_choice%" == "back" goto :main_menu
if /i "%settings_menu_choice%" == "stop" goto :end
if /i "%settings_menu_choice%" == "end" goto :end
if /i "%settings_menu_choice%" == "b" goto :main_menu
if /i "%settings_menu_choice%" == "s" goto :end
if /i "%settings_menu_choice%" == "e" goto :end

:settings_menu_scheme
cls
for /f "tokens=2 delims=:(" %%i in ('powercfg /getactivescheme') do (
    set "SCHEME=%%i"
)
set "SCHEME=%SCHEME: =%"
echo %lang_config_power_plan%
echo GUID: %SCHEME%
echo.
timeout /t 1 >nul
echo 1. %lang_settings_timeout_monitor%
echo 2. %lang_settings_time_sleep%
echo 3. %lang_settings_timeout_disk%
echo 4. %lang_back%
echo 5. %lang_exit%
set /p settings_menu_scheme="%lang_choice%"
if "%settings_menu_scheme%" == "1" goto :settings_timeout_monitor
if "%settings_menu_scheme%" == "2" goto :settings_timeout_standby
if "%settings_menu_scheme%" == "3" goto :settings_timeout_disk
if "%settings_menu_scheme%" == "4" goto :settings_menu
if "%settings_menu_scheme%" == "5" goto :end
if /i "%settings_menu_scheme%" == "back" goto :settings_menu
if /i "%settings_menu_scheme%" == "end" goto :end
if /i "%settings_menu_scheme%" == "exit" goto :end
if /i "%settings_menu_scheme%" == "stop" goto :end
if /i "%settings_menu_scheme%" == "s" goto :end
if /i "%settings_menu_scheme%" == "e" goto :end
if /i "%settings_menu_scheme%" == "b" goto :settings_menu

cls
echo %lang_error_input%
timeout /t 2 > nul
goto :settings_menu_scheme

:settings_timeout_disk
cls
timeout /t 1 >nul
echo 1. 10 %lang_minutes%
echo 2. 15 %lang_minutes%
echo 3. 20 %lang_minutes%
echo 4. 0 %lang_minutes%
echo 5. %lang_manual_input%
echo 6. %lang_back%
echo 7. %lang_exit%
set /p settings_timeout_disk="%lang_choice%"
if "%settings_timeout_disk%" == "1" goto :10_timeout_disk
if "%settings_timeout_disk%" == "2" goto :15_timeout_disk
if "%settings_timeout_disk%" == "3" goto :20_timeout_disk
if "%settings_timeout_disk%" == "4" goto :0_timeout_disk
if "%settings_timeout_disk%" == "5" goto :send_timeout_disk
if "%settings_timeout_disk%" == "6" goto :settings_menu_scheme
if "%settings_timeout_disk%" == "7" goto :end
if /i "%settings_timeout_disk%" == "exit" goto :end
if /i "%settings_timeout_disk%" == "stop" goto :end
if /i "%settings_timeout_disk%" == "end" goto :end
if /i "%settings_timeout_disk%" == "back" goto :settings_menu_scheme
if /i "%settings_timeout_disk%" == "b" goto :settings_menu_scheme
if /i "%settings_timeout_disk%" == "e" goto :end
if /i "%settings_timeout_disk%" == "s" goto :end


cls
echo %lang_error_input%
timeout /t 2 > nul
cls
goto :settings_timeout_disk

:10_timeout_disk
cls
powercfg /change disk-timeout-ac 10 >nul 2>&1
powercfg /change disk-timeout-dc 10 >nul 2>&1
if %errorlevel% neq 0 (
    echo %lang_error_timeout_10_minutes%
    timeout /t 2 >nul
    goto :settings_timeout_disk
) else (
    echo %lang_settings_succesfull%
    timeout /t 1 >nul
    goto :settings_timeout_disk
)

:15_timeout_disk
cls
powercfg /change disk-timeout-ac 15 >nul 2>&1
powercfg /change disk-timeout-dc 15 >nul 2>&1
if %errorlevel% neq 0 (
    echo %lang_error_timeout_10_minutes%
    timeout /t 2 >nul
    goto :settings_timeout_disk
) else (
    echo %lang_settings_succesfull%
    timeout /t 1 >nul
    goto :settings_timeout_disk
)

:20_timeout_disk
cls
powercfg /change disk-timeout-ac 20 >nul 2>&1
powercfg /change disk-timeout-dc 20 >nul 2>&1
if %errorlevel% neq 0 (
    echo %lang_error_timeout_10_minutes%
    timeout /t 2 >nul
    goto :settings_timeout_disk
) else (
    echo %lang_settings_succesfull%
    timeout /t 1 >nul
    goto :settings_timeout_disk
)

:0_timeout_disk
cls
powercfg /change disk-timeout-ac 0 >nul 2>&1
powercfg /change disk-timeout-dc 0 >nul 2>&1
if %errorlevel% neq 0 (
    echo %lang_error_timeout_10_minutes%
    timeout /t 2 >nul
    goto :settings_timeout_disk
) else (
    echo %lang_settings_succesfull%
    timeout /t 1 >nul
    goto :settings_timeout_disk
)

:send_timeout_disk
cls
timeout /t 1 >nul
set /p time_timeout_disk=%lang_enter_timeout_minutes%
if /i "%time_timeout_disk%" == "back" goto :settings_timeout_disk
if /i "%time_timeout_disk%" == "exit" goto :end
if /i "%time_timeout_disk%" == "stop" goto :end
if /i "%time_timeout_disk%" == "end" goto :end
if /i "%time_timeout_disk%" == "b" goto :settings_timeout_disk
if /i "%time_timeout_disk%" == "e" goto :end
if /i "%time_timeout_disk%" == "s" goto :end
powercfg /change disk-timeout-ac %time_timeout_disk% >nul 2>&1
powercfg /change disk-timeout-dc %time_timeout_disk% >nul 2>&1
if "%time_timeout_disk%" == "" goto :send_timeout_disk
if %errorlevel% neq 0 (
    echo %lang_error_send_timeout_minutes%
    timeout /t 2 > nul
    goto :send_timeout_disk
) else (
    echo %lang_settings_succesfull%
    timeout /t 1 >nul
    goto :settings_timeout_disk
)

:settings_timeout_standby
cls
timeout /t 1 >nul
echo 1. 10 %lang_minutes%
echo 2. 15 %lang_minutes%
echo 3. 20 %lang_minutes%
echo 4. 0 %lang_minutes%
echo 5. %lang_manual_input%
echo 6. %lang_back%
echo 7. %lang_exit%
set /p settings_timeout_standby="%lang_choice%"
if "%settings_timeout_standby%" == "1" goto :10_timeout_standby
if "%settings_timeout_standby%" == "2" goto :15_timeout_standby
if "%settings_timeout_standby%" == "3" goto :20_timeout_standby
if "%settings_timeout_standby%" == "4" goto :0_timeout_standby
if "%settings_timeout_standby%" == "5" goto :send_timeout_standby
if "%settings_timeout_standby%" == "6" goto :settings_menu_scheme
if "%settings_timeout_standby%" == "7" goto :end
if /i "%settings_timeout_standby%" == "back" goto :settings_menu_scheme
if /i "%settings_timeout_standby%" == "stop" goto :end
if /i "%settings_timeout_standby%" == "exit" goto :end
if /i "%settings_timeout_standby%" == "end" goto :end
if /i "%settings_timeout_standby%" == "e" goto :end
if /i "%settings_timeout_standby%" == "s" goto :end
if /i "%settings_timeout_standby%" == "b" goto :settings_menu_scheme

cls
echo %lang_error_input%
timeout /t 2 > nul
cls
goto :settings_timeout_standby

:10_timeout_standby
cls
powercfg /change standby-timeout-ac 10 >nul 2>&1
powercfg /change standby-timeout-dc 10 >nul 2>&1
if %errorlevel% neq 0 (
    echo %lang_error_timeout_10_minutes%
    timeout /t 2 >nul
    goto :settings_timeout_standby
) else (
    echo %lang_settings_succesfull%
    timeout /t 1 >nul
    goto :settings_timeout_standby
)

:15_timeout_standby
cls
powercfg /change standby-timeout-ac 15 >nul 2>&1
powercfg /change standby-timeout-dc 15 >nul 2>&1
if %errorlevel% neq 0 (
    echo %lang_error_timeout_15_minutes%
    timeout /t 2 >nul
    goto :settings_timeout_standby
) else (
    echo %lang_settings_succesfull%
    timeout /t 1 >nul
    goto :settings_timeout_standby
)

:20_timeout_standby
cls
powercfg /change standby-timeout-ac 20 >nul 2>&1
powercfg /change standby-timeout-dc 20 >nul 2>&1
if %errorlevel% neq 0 (
    echo %lang_error_timeout_20_minutes%
    timeout /t 2 >nul
    goto :settings_timeout_standby
) else (
    echo %lang_settings_succesfull%
    timeout /t 1 >nul
    goto :settings_timeout_standby
)

:0_timeout_standby
cls
powercfg /change standby-timeout-ac 0 >nul 2>&1
powercfg /change standby-timeout-dc 0 >nul 2>&1
if %errorlevel% neq 0 (
    echo %lang_error_timeout_0_minutes%
    timeout /t 2 >nul
    goto :settings_timeout_standby
) else (
    echo %lang_settings_succesfull%
    timeout /t 1 >nul
    goto :settings_timeout_standby
)

:send_timeout_standby
cls
timeout /t 1 >nul
set /p time_timeout_standby=%lang_enter_timeout_minutes%
if /i "%time_timeout_standby%" == "back" goto :settings_timeout_standby
if /i "%time_timeout_standby%" == "exit" goto :end
if /i "%time_timeout_standby%" == "stop" goto :end
if /i "%time_timeout_standby%" == "end" goto :end
if /i "%time_timeout_standby%" == "b" goto :settings_timeout_standby
if /i "%time_timeout_standby%" == "e" goto :end
if /i "%time_timeout_standby%" == "s" goto :end
powercfg /change standby-timeout-ac %time_timeout_standby% >nul 2>&1
powercfg /change standby-timeout-dc %time_timeout_standby% >nul 2>&1
if "%time_timeout_standby%" == "" goto :send_timeout_standby
if %errorlevel% neq 0 (
    echo %lang_error_send_timeout_minutes%
    timeout /t 2 > nul
    goto :send_timeout_standby
) else (
    echo %lang_settings_succesfull%
    timeout /t 1 >nul
    goto :settings_timeout_standby
)

:settings_timeout_monitor
cls
timeout /t 1 >nul
echo 1. 10 %lang_minutes%
echo 2. 15 %lang_minutes%
echo 3. 20 %lang_minutes%
echo 4. 0 %lang_minutes%
echo 5. %lang_manual_input%
echo 6. %lang_back%
echo 7. %lang_exit%
set /p settings_timeout_monitor="%lang_choice%"
if "%settings_timeout_monitor%" == "1" goto :10_timeout_monitor
if "%settings_timeout_monitor%" == "2" goto :15_timeout_monitor
if "%settings_timeout_monitor%" == "3" goto :20_timeout_monitor
if "%settings_timeout_monitor%" == "4" goto :0_timeout_monitor
if "%settings_timeout_monitor%" == "5" goto :send_timeout_monitor
if "%settings_timeout_monitor%" == "6" goto :settings_menu_scheme
if "%settings_timeout_monitor%" == "7" goto :end
if /i "%settings_timeout_monitor%" == "back" goto :settings_menu_scheme
if /i "%settings_timeout_monitor%" == "stop" goto :end
if /i "%settings_timeout_monitor%" == "exit" goto :end
if /i "%settings_timeout_monitor%" == "end" goto :end
if /i "%settings_timeout_monitor%" == "e" goto :end
if /i "%settings_timeout_monitor%" == "s" goto :end
if /i "%settings_timeout_monitor%" == "b" goto :settings_menu_scheme

cls
echo %lang_error_input%
timeout /t 2 > nul
cls
goto :settings_timeout_monitor

:10_timeout_monitor
cls
powercfg /change monitor-timeout-ac 10 >nul 2>&1
powercfg /change monitor-timeout-dc 10 >nul 2>&1
if %errorlevel% neq 0 (
    echo %lang_error_timeout_10_minutes%
    timeout /t 2 >nul
    goto :settings_timeout_monitor
) else (
    echo %lang_settings_succesfull%
    timeout /t 1 >nul
    goto :settings_timeout_monitor
)

:15_timeout_monitor
cls
powercfg /change monitor-timeout-ac 15 >nul 2>&1
powercfg /change monitor-timeout-dc 15 >nul 2>&1
if %errorlevel% neq 0 (
    echo %lang_error_timeout_15_minutes%
    timeout /t 2 >nul
    goto :settings_timeout_monitor
) else (
    echo %lang_settings_succesfull%
    timeout /t 1 >nul
    goto :settings_timeout_monitor
)

:20_timeout_monitor
cls
powercfg /change monitor-timeout-ac 20 >nul 2>&1
powercfg /change monitor-timeout-ac 20 >nul 2>&1
if %errorlevel% neq 0 (
    echo %lang_error_timeout_20_minutes%
    timeout /t 2 >nul
    goto :settings_timeout_monitor
) else (
    echo %lang_settings_succesfull%
    timeout /t 1 >nul
    goto :settings_timeout_monitor
)

:0_timeout_monitor
cls
powercfg /change monitor-timeout-ac 0 >nul 2>&1
powercfg /change monitor-timeout-ac 0 >nul 2>&1
if %errorlevel% neq 0 (
    echo %lang_error_timeout_0_minutes%
    timeout /t 2 >nul
    goto :settings_timeout_monitor
) else (
    echo %lang_settings_succesfull%
    timeout /t 1 >nul
    goto :settings_timeout_monitor
)

:send_timeout_monitor
cls
timeout /t 1 >nul
set /p time_timeout_monitor=%lang_enter_timeout_minutes%
if /i "%time_timeout_monitor%" == "back" goto :settings_timeout_monitor
if /i "%time_timeout_monitor%" == "exit" goto :end
if /i "%time_timeout_monitor%" == "stop" goto :end
if /i "%time_timeout_monitor%" == "end" goto :end
if /i "%time_timeout_monitor%" == "b" goto :settings_timeout_monitor
if /i "%time_timeout_monitor%" == "e" goto :end
if /i "%time_timeout_monitor%" == "s" goto :end
powercfg /change monitor-timeout-ac %time_timeout_monitor% >nul 2>&1
powercfg /change monitor-timeout-dc %time_timeout_monitor% >nul 2>&1
if "%time_timeout_monitor%" == "" goto :send_timeout_monitor
if %errorlevel% neq 0 (
    echo %lang_error_send_timeout_minutes%
    timeout /t 2 > nul
    goto :send_timeout_monitor
) else (
    echo %lang_settings_succesfull%
    timeout /t 1 >nul
    goto :settings_timeout_monitor
)

:language_settings
cls
call :reload_language
timeout /t 1 >nul
echo %lang_language_settings%
echo 1. %lang_russian%
echo 2. %lang_english%
echo 3. %lang_main_menu%
echo 4. %lang_exit%
set /p language_settings_choice="%lang_choice%"
if "%language_settings_choice%" == "1" goto :set_russian
if "%language_settings_choice%" == "2" goto :set_english
if "%language_settings_choice%" == "3" goto :main_menu
if "%language_settings_choice%" == "4" goto :end
if /i "%language_settings_choice%" == "back" goto :main_menu
if /i "%language_settings_choice%" == "exit" goto :end
if /i "%language_settings_choice%" == "stop" goto :end
if /i "%language_settings_choice%" == "end" goto :end
if /i "%language_settings_choice%" == "e" goto :end
if /i "%language_settings_choice%" == "s" goto :end
if /i "%language_settings_choice%" == "b" goto :main_menu

:set_russian
echo language=ru > "%CONFIG_FILE%"
set "CURRENT_LANG=ru"
goto :language_settings

:set_english
echo language=en > "%CONFIG_FILE%"
set "CURRENT_LANG=en"
goto :language_settings

:check_update
cls
echo %GREEN%%lang_check_update%%RESET%
echo %lang_version%%BLUE%%version%%RESET%

::GitHub URL
set "VERSION_URL=https://raw.githubusercontent.com/BrocatScript/PowerSetSetup/main/version.txt"
powershell -Command "Invoke-RestMethod -Uri '%VERSION_URL%'" > temp_ver.txt 2>nul

if not exist temp_ver.txt (
    echo %RED%%lang_error_check_update%%RESET%
    timeout /t 2 >nul
    goto :main_menu
)

set "latest_version="
< temp_ver.txt (
  set /p latest_version=
)
del temp_ver.txt

if "%latest_version%"=="" (
    echo %RED%%lang_error_check_update%%RESET%
    timeout /t 2 >nul
    goto :main_menu
)

echo %lang_latest_version%%CYAN%%latest_version%%RESET%
echo.

set "is_fix=0"
if not "%latest_version:fix=%"=="%latest_version%" set is_fix=1

set "current_has_fix=0"
if not "%version:fix=%"=="%version%" set current_has_fix=1

set "is_beta=0"
if not "%latest_version:beta=%"=="%latest_version%" set is_beta=1

set "current_has_beta=0"
if not "%version:beta=%"=="%version%" set current_has_beta=1

set "clean_version=%version%"
set "clean_latest=%latest_version%"

set "clean_version=%clean_version:beta=%"
set "clean_version=%clean_version:fix=%"
set "clean_latest=%clean_latest:beta=%"
set "clean_latest=%clean_latest:fix=%"

for /f "tokens=1-3 delims=." %%a in ("%clean_version%") do (
    set "current_major=%%a"
    set "current_minor=%%b"
    set "current_patch=%%c"
)

for /f "tokens=1-3 delims=." %%a in ("%clean_latest%") do (
    set "latest_major=%%a"
    set "latest_minor=%%b"
    set "latest_patch=%%c"
)

set "need_update=0"

if %latest_major% gtr %current_major% set need_update=1
if %latest_major% equ %current_major% (
    if %latest_minor% gtr %current_minor% set need_update=1
    if %latest_minor% equ %current_minor% (
        if %latest_patch% gtr %current_patch% set need_update=1
    )
)

if "%is_fix%"=="1" (
    if %latest_major% equ %current_major% (
        if %latest_minor% equ %current_minor% (
            if %latest_patch% equ %current_patch% (
                if "%current_has_fix%"=="0" (
                    set need_update=1
                )
                if "%current_has_fix%"=="1" (
                    if not "%latest_version%"=="%version%" (
                        set need_update=1
                    )
                )
            )
        )
    )
)

if "%is_beta%"=="1" (
    if %latest_major% equ %current_major% (
        if %latest_minor% equ %current_minor% (
            if %latest_patch% equ %current_patch% (
                if "%current_has_beta%"=="0" (
                    set need_update=1
                )
                if "%current_has_beta%"=="1" (
                    if not "%latest_version%"=="%version%" (
                        set need_update=1
                    )
                )
            )
        )
    )
)

if %need_update% equ 0 (
    echo %lang_system_latest_version%
    timeout /t 2 >nul
    goto :main_menu
)

if "%is_fix%"=="0" (
    if "%is_beta%"=="1" (
        echo %lang_system_latest_version%
        timeout /t 2 >nul
        goto :main_menu
    )
)

:updates_choice
echo %lang_new_release%%GREEN%%latest_version%%RESET%
echo.

if "%is_fix%"=="1" (
    echo %lang_fix_update% %GREEN%%latest_version%%RESET%
) else if "%is_beta%"=="1" (
    echo %lang_beta_update% %CYAN%%latest_version%%RESET%
)
echo.
echo.
echo 1. %lang_download_update%
echo 2. %lang_skip_update%
set /p choice_update="%lang_choice%"
if "%choice_update%"=="1" goto :yes_update
if "%choice_update%"=="2" goto :not_update
if /i "%choice_update%"=="yes" goto :yes_update
if /i "%choice_update%"=="y" goto :yes_update
if /i "%choice_update%"=="not" goto :not_update
if /i "%choice_update%"=="n" goto :not_update
if /i "%choice_update%"=="back" goto :main_menu
if /i "%choice_update%"=="b" goto :main_menu
if /i "%choice_update%"=="end" goto :end
if /i "%choice_update%"=="e" goto :end

cls
echo %lang_error_input%
timeout /t 2 > nul
goto :check_update

:yes_update
cls
echo %lang_open_page%
start "" "https://github.com/BrocatScript/PowerSetSetup/releases"
echo.
timeout /t 2 >nul
cls
goto :main_menu

:not_update
cls
goto :main_menu

:menu_yes
cls
timeout /t 1 > nul
echo %lang_scheme_warning%
echo.
echo %lang_choose_required_mode%
echo 1. %lang_max_performance% (%lang_max_power_consumption%)
echo 2. %lang_balanced% (%lang_balans_consumption%)
echo 3. %lang_powersave% (%lang_low_power%)
echo 4. %lang_main_menu%
echo 5. %lang_exit%
set /p automode="%lang_choice%"
if "%automode%" == "1" goto :automode1
if "%automode%" == "2" goto :automode2
if "%automode%" == "3" goto :automode3
if "%automode%" == "4" goto :main_menu
if "%automode%" == "5" goto :end
if /i "%automode%" == "back" goto :main_menu
if /i "%automode%" == "b" goto :main_menu
if /i "%automode%" == "stop" goto :end
if /i "%automode%" == "exit" goto :end
if /i "%automode%" == "end" goto :end
if /i "%automode%" == "e" goto :end
if /i "%automode%" == "s" goto :end

cls
echo %lang_error_input%
timeout /t 2 > nul
goto :menu_yes

:automode1
cls
echo %lang_result_before%
powercfg /l
powercfg -restoredefaultschemes
powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61 a1234567-b000-c000-d000-e70707070707
powercfg /setactive a1234567-b000-c000-d000-e70707070707
powercfg -delete a1841308-3541-4fab-bc81-f71556f20b4a
powercfg -delete 381b4222-f694-41f0-9685-ff5bb260df2e
powercfg -delete 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
echo.
echo.
echo %lang_result_after%
goto :automode1_end_menu

:automode1_end_menu
powercfg /l
echo.
echo %lang_choice%
echo 1. %lang_main_menu%
echo 2. %lang_exit%
set /p autoend1="%lang_choice%"
if "%autoend1%" == "1" goto :main_menu
if "%autoend1%" == "2" goto :end
if /i "%autoend1%" == "back" goto :main_menu
if /i "%autoend1%" == "stop" goto :end
if /i "%autoend1%" == "exit" goto :end
if /i "%autoend1%" == "end" goto :end
if /i "%autoend1%" == "b" goto :main_menu
if /i "%autoend1%" == "e" goto :end
if /i "%autoend1%" == "s" goto :end

cls
echo %lang_error_input%
timeout /t 2 >nul
cls
goto :automode1_end_menu

:automode2
cls
echo %lang_result_before%
powercfg /l
powercfg -restoredefaultschemes
powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e
powercfg -delete a1841308-3541-4fab-bc81-f71556f20b4a
powercfg -delete 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
echo.
echo.
echo %lang_result_after%
goto :automode2_end_menu

:automode2_end_menu
powercfg /l
echo.
echo %lang_choice%
echo 1. %lang_main_menu%
echo 2. %lang_exit%
set /p autoend2="%lang_choice%"
if "%autoend2%" == "1" goto :main_menu
if "%autoend2%" == "2" goto :end
if /i "%autoend2%" == "back" goto :main_menu
if /i "%autoend2%" == "stop" goto :end
if /i "%autoend2%" == "exit" goto :end
if /i "%autoend2%" == "end" goto :end
if /i "%autoend2%" == "b" goto :main_menu
if /i "%autoend2%" == "e" goto :end
if /i "%autoend2%" == "s" goto :end

cls
echo %lang_error_input%
timeout /t 2 >nul
cls
goto :automode2_end_menu

:automode3
cls
echo %lang_result_before%
powercfg /l
powercfg -restoredefaultschemes
powercfg /setactive a1841308-3541-4fab-bc81-f71556f20b4a
powercfg -delete 381b4222-f694-41f0-9685-ff5bb260df2e
powercfg -delete 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
echo.
echo.
echo %lang_result_after%
goto :automode3_end_menu

:automode3_end_menu
powercfg /l
echo.
echo %lang_choice%
echo 1. %lang_main_menu%
echo 2. %lang_exit%
set /p autoend3="%lang_choice%"
if "%autoend3%" == "1" goto :main_menu
if "%autoend3%" == "2" goto :end
if /i "%autoend3%" == "back" goto :main_menu
if /i "%autoend3%" == "stop" goto :end
if /i "%autoend3%" == "exit" goto :end
if /i "%autoend3%" == "end" goto :end
if /i "%autoend3%" == "b" goto :main_menu
if /i "%autoend3%" == "e" goto :end
if /i "%autoend3%" == "s" goto :end

cls
echo %lang_error_input%
timeout /t 2 >nul
cls
goto :automode3_end_menu

:menu_not
cls
timeout /t 1 > nul
powercfg /l
echo.
echo %lang_advancedSettings%
echo.
echo 1. %lang_delete_scheme%
echo 2. %lang_reset_scheme%
echo 3. %lang_add_scheme%
echo 4. %lang_activate_scheme%
echo 5. %lang_list_scheme%
echo 6. %lang_exit%
echo 7. %lang_main_menu%
set /p choice2="%lang_choice%"
if "%choice2%" == "1" goto :delete_scheme
if "%choice2%" == "2" goto :reset_scheme
if "%choice2%" == "3" goto :add_scheme
if "%choice2%" == "4" goto :select_scheme
if "%choice2%" == "5" goto :list_scheme
if "%choice2%" == "6" goto :end
if "%choice2%" == "7" goto :main_menu
if /i "%choice2%" == "exit" goto :end
if /i "%choice2%" == "stop" goto :end
if /i "%choice2%" == "end" goto :end
if /i "%choice2%" == "back" goto :main_menu
if /i "%choice2%" == "b" goto :main_menu

cls
echo %lang_error_input%
timeout /t 2 > nul
cls
goto :menu_not

:select_scheme
cls
timeout /t 1 > nul
powercfg /l
echo.
echo 1. %lang_balanced%
echo 2. %lang_performance%
echo 3. %lang_max_performance%
echo 4. %lang_powersave%
echo 5. %lang_manual_input%
echo 6. %lang_back%
echo 7. %lang_exit%
set /p select_scheme="%lang_choice%"
if "%select_scheme%" == "1" goto :select_sh1
if "%select_scheme%" == "2" goto :select_sh2
if "%select_scheme%" == "3" goto :select_sh3
if "%select_scheme%" == "4" goto :select_sh4
if "%select_scheme%" == "5" goto :select_sh_send
if "%select_scheme%" == "6" goto :menu_not
if "%select_scheme%" == "7" goto :end
if /i "%select_scheme%" == "back" goto :menu_not
if /i "%select_scheme%" == "b" goto :menu_not
if /i "%select_scheme%" == "stop" goto :end
if /i "%select_scheme%" == "exit" goto :end
if /i "%select_scheme%" == "end" goto :end
if /i "%select_scheme%" == "e" goto :end

cls
echo %lang_error_input%
timeout /t 2 > nul
cls
goto :select_scheme

:select_sh1
cls
powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo %lang_error_balanced_scheme_not_found%
    timeout /t 2 > nul
    goto :select_scheme
) else (
    echo.
    echo %lang_balanced_scheme_activated%
    powercfg /l
    timeout /t 2 > nul
    goto :select_scheme
)

:select_sh2
cls
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo %lang_error_performance_scheme_not_found%
    timeout /t 2 > nul
    goto :select_scheme
) else (
    echo.
    echo %lang_perfomance_scheme_activated%
    powercfg /l
    timeout /t 2 > nul
    goto :select_scheme
)

:select_sh3
cls
powercfg /setactive a1234567-b000-c000-d000-e70707070707 >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo %lang_max_perfomance_scheme_not_found%
    timeout /t 2 > nul
    goto :select_scheme
) else (
    echo.
    echo %lang_max_perfomance_scheme_activated%
    powercfg /l
    timeout /t 2 > nul
    goto :select_scheme
)

:select_sh4
cls
powercfg /setactive a1841308-3541-4fab-bc81-f71556f20b4a >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo %lang_low_power_scheme_not_found%
    powercfg /l
    timeout /t 2 > nul
    goto :select_scheme
) else (
    echo.
    echo %lang_low_power_scheme_activated%
    powercfg /l
    timeout /t 2 > nul
    goto :select_scheme
)

:select_sh_send
cls
powercfg /l
echo.
set /p id_select_sh_send=%lang_enter_id_power_scheme%
powercfg /setactive %id_select_sh_send% >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo %lang_error_id_power_scheme%
    timeout /t 2 > nul
    goto :select_sh_send
) else (
    echo.
    echo %lang_id_power_scheme_activated%
    goto :select_scheme
)

:list_scheme
cls
powercfg /l
pause
goto :menu_not

:add_scheme
cls
timeout /t 1 > nul
powercfg /l
echo.
echo %lang_addPowerPlanInfo%
echo 1. %lang_max_performance%
echo 2. %lang_settings%
echo 3. %lang_main_menu%
echo 4. %lang_exit%
set /p adding_scheme="%lang_choice%"
if "%adding_scheme%" == "1" goto :add_1
if "%adding_scheme%" == "2" goto :menu_not
if "%adding_scheme%" == "3" goto :main_menu
if "%adding_scheme%" == "4" goto :end
if /i "%adding_scheme%" == "back" goto :main_menu
if /i "%adding_scheme%" == "b" goto :main_menu
if /i "%adding_scheme%" == "exit" goto :end
if /i "%adding_scheme%" == "stop" goto :end
if /i "%adding_scheme%" == "end" goto :end
if /i "%adding_scheme%" == "e" goto :end
if /i "%adding_scheme%" == "s" goto :end

cls
echo %lang_error_input%
timeout /t 2 > nul
cls
goto :add_scheme

:add_1
cls
timeout /t 1 > nul
powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61 a1234567-b000-c000-d000-e70707070707 >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo %lang_error_add_max_power_scheme%
    timeout /t 2 > nul
    goto :add_scheme
) else (
    echo.
    echo %lang_max_power_scheme_added%
    echo.
    echo %lang_result%
    powercfg /l
    echo.
    timeout /t 2 > nul
)
echo 1. %lang_main_menu%
echo 2. %lang_settings%
echo 3. %lang_exit%
set /p mini_choice3="%lang_choice%"
if "%mini_choice3%" == "1" goto :main_menu
if "%mini_choice3%" == "2" goto :menu_not
if "%mini_choice3%" == "3" goto :end
if /i "%mini_choice3%" == "stop" goto :end
if /i "%mini_choice3%" == "exit" goto :end
if /i "%mini_choice3%" == "end" goto :end
if /i "%mini_choice3%" == "e" goto :end
if /i "%mini_choice3%" == "s" goto :end

cls
echo %lang_error_input%
timeout /t 2 > nul
cls
goto :add_scheme

:reset_scheme
cls
timeout /t 1 > nul
echo %lang_result_before%
powercfg /l
echo.
powercfg -restoredefaultschemes
echo %lang_result_after%
powercfg /l
echo.
echo 1. %lang_main_menu%
echo 2. %lang_settings%
echo 3. %lang_exit%
set /p reset_schemes="%lang_choice%"
if "%reset_schemes%" == "1" goto :main_menu
if "%reset_schemes%" == "2" goto :menu_not
if "%reset_schemes%" == "3" goto :end
if /i "%reset_schemes%" == "stop" goto :end
if /i "%reset_schemes%" == "exit" goto :end
if /i "%reset_schemes%" == "end" goto :end
if /i "%reset_schemes%" == "e" goto :end
if /i "%reset_schemes%" == "s" goto :end

cls
echo %lang_error_input%
timeout /t 2 > nul
cls
goto :reset_scheme

:delete_scheme
cls
powercfg /l
echo.
echo %lang_what_delet_scheme%
echo 1. %lang_balanced%
echo 2. %lang_performance%
echo 3. %lang_max_performance%
echo 4. %lang_powersave%
echo 5. %lang_manual_input%
echo 6. %lang_exit%
set /p choice3="%lang_choice%"
if /i "%choice3%" == "del1" goto :del1
if /i "%choice3%" == "1" goto :del1
if /i "%choice3%" == "del2" goto :del2
if /i "%choice3%" == "2" goto :del2
if /i "%choice3%" == "del3" goto :del3
if /i "%choice3%" == "3" goto :del3
if /i "%choice3%" == "del4" goto :del4
if /i "%choice3%" == "4" goto :del4
if /i "%choice3%" == "send" goto :send_del
if /i "%choice3%" == "s" goto :send_del
if /i "%choice3%" == "back" goto :menu_not
if /i "%choice3%" == "b" goto :menu_not
if /i "%choice3%" == "stop" goto :end
if /i "%choice3%" == "exit" goto :end
if /i "%choice3%" == "end" goto :end
if /i "%choice3%" == "e" goto :end

cls
echo %lang_error_input%
timeout /t 2 > nul
cls
goto :delete_scheme

:del1
cls
timeout /t 1 > nul
powercfg -delete 381b4222-f694-41f0-9685-ff5bb260df2e >nul 2>&1

if %errorlevel% neq 0 (
    echo.
    echo %lang_error_balanced_scheme_not_found%
    timeout /t 2 > nul
    goto :delete_scheme
) else (
    echo.
    echo %lang_balanced_scheme_deleted%
    echo.
    powercfg /l
    timeout /t 2 > nul
    goto :next
)

:del2
cls
timeout /t 1 > nul
powercfg -delete 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c >nul 2>&1

if %errorlevel% neq 0 (
    echo.
    echo %lang_error_performance_scheme_not_found%
    timeout /t 2 > nul
    goto :delete_scheme
) else (
    echo.
    echo %lang_perfomance_scheme_deleted%
    echo.
    powercfg /l
    timeout /t 2 > nul
    goto :next
)

:del3
cls
timeout /t 1 > nul
powercfg -delete a1234567-b000-c000-d000-e70707070707 >nul 2>&1

if %errorlevel% neq 0 (
    echo.
    echo %lang_max_perfomance_scheme_not_found%
    timeout /t 2 > nul
    goto :delete_scheme
) else (
    echo.
    echo %lang_max_perfomance_scheme_deleted%
    echo.
    powercfg /l
    timeout /t 2 > nul
    goto :next
)

:del4
cls
timeout /t 1 > nul
powercfg -delete a1841308-3541-4fab-bc81-f71556f20b4a >nul 2>&1

if %errorlevel% neq 0 (
    echo.
    echo %lang_low_power_scheme_not_found%
    timeout /t 2 > nul
    goto :delete_scheme
) else (
    echo.
    echo %lang_low_power_scheme_deleted%
    echo.
    powercfg /l
    timeout /t 2 > nul
    goto :next
)

:send_del
cls
timeout /t 1 > nul
powercfg /l
echo.
set /p id_scheme="%lang_enter_id_power_scheme%"

if /i "%id_scheme%" == "back" goto :main_menu
if /i "%id_scheme%" == "exit" goto :end
if /i "%id_scheme%" == "stop" goto :end
if /i "%id_scheme%" == "end" goto :end
if /i "%id_scheme%" == "b" goto :main_menu
if /i "%id_scheme%" == "e" goto :end
if /i "%id_scheme%" == "s" goto :end

powercfg -delete %id_scheme% >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo %lang_error_id_power_scheme%
    timeout /t 2 > nul
    goto :send_del
) else (
    echo.
    echo %lang_scheme_succesfull_deleted%
    goto :next
)

:back
cls
timeout /t 1 > nul
echo %lang_error_back_main_menu%
timeout /t 2 > nul
goto :main_menu

:next
cls
timeout /t 1 > nul
powercfg /l
echo.
echo.
echo 1. %lang_back_select_delet_scheme%
echo 2. %lang_exit%
echo 3. %lang_main_menu%
set /p choice4="%lang_choice%"
if "%choice4%" == "1" goto :delete_scheme
if "%choice4%" == "2" goto :end
if "%choice4%" == "3" goto :main_menu
if /i "%choice4%" == "yes" goto :delete_scheme
if /i "%choice4%" == "y" goto :delete_scheme
if /i "%choice4%" == "да" goto :delete_scheme
if /i "%choice4%" == "д" goto :delete_scheme
if /i "%choice4%" == "not" goto :end
if /i "%choice4%" == "n" goto :end
if /i "%choice4%" == "нет" goto :end
if /i "%choice4%" == "н" goto :end
if /i "%choice4%" == "stop" goto :end
if /i "%choice4%" == "exit" goto :end
if /i "%choice4%" == "end" goto :end
if /i "%choice4%" == "e" goto :end
if /i "%choice4%" == "s" goto :end
if /i "%choice4%" == "back" goto :main_menu
if /i "%choice4%" == "b" goto :main_menu

cls
echo %lang_error_input%
timeout /t 2 > nul
cls
goto :next

:end
cls
exit