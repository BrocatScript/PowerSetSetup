<div align="center">

<img src="docs/assets/icons/logo.svg" width="96" alt="PowerSetSetup">

# PowerSetSetup ⚡

**[English](#english)** &nbsp;&nbsp; 🌐 &nbsp;&nbsp; **[Русский](#русский)**

![Windows 10/11](https://img.shields.io/badge/Windows-10%2F11-0078D6?style=for-the-badge&logo=windows)
![License](https://img.shields.io/badge/License-PolyForm%20Noncommercial-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Supported-success?style=for-the-badge)

</div>

---

<a id="english"></a>

# English

> **Switch Windows power plans in one click, and clean up the ones you don't need. No Control Panel digging, no `powercfg` commands to memorize.**

<div align="center">

[![Download](https://img.shields.io/badge/⬇️%20Download-brightgreen?style=for-the-badge&logo=windows)](https://github.com/BrocatScript/PowerSetSetup/releases/latest)

[![Releases](https://img.shields.io/badge/🚀%20Releases-Available%20Versions-blue?style=for-the-badge&logo=github)](https://github.com/BrocatScript/PowerSetSetup/releases)
[![Issues](https://img.shields.io/badge/🐞%20Issues-Report%20Bug-red?style=for-the-badge&logo=github)](https://github.com/BrocatScript/PowerSetSetup/issues)
[![Pull Requests](https://img.shields.io/badge/🔀%20PRs-Contribute-green?style=for-the-badge&logo=github)](https://github.com/BrocatScript/PowerSetSetup/pulls)
[![Wiki](https://img.shields.io/badge/📚%20Wiki-Documentation-lightgrey?style=for-the-badge&logo=readthedocs)](https://github.com/BrocatScript/PowerSetSetup/wiki)
[![News](https://img.shields.io/badge/📰%20News-lightgrey?style=for-the-badge&logo=readthedocs)](https://github.com/BrocatScript/PowerSetSetup/blob/main/docs/NEWS.md)
[![Source](https://img.shields.io/badge/📁%20Source-Code-black?style=for-the-badge&logo=github)](https://github.com/BrocatScript/PowerSetSetup)

</div>

## 🤔 What is it and who is it for?

Windows has power plans that decide how your PC trades speed for energy use. Switching between them is awkward: the plan you need is often hidden in the Control Panel, missing entirely, or only reachable through `powercfg` commands with long GUIDs.

**PowerSetSetup** puts the three modes people actually use on one screen:

| Mode | When to use it |
|---|---|
| ⚡ **Maximum performance** | Games, rendering, compiling: when speed matters |
| ⚖️ **Balanced** | Everyday work |
| 🔋 **Power saving** | A laptop away from the socket: when battery life matters |

Pick a mode and you're done. It manages the same standard Windows power plans through the built-in `powercfg` tool. It does not change hidden system settings.

**It is for you if** you switch between gaming and battery modes, your plan list is cluttered by laptop vendors, or you simply don't want to use the command line.

## 🖼️ Screenshots

<div align="center">

<img src="docs/assets/screenshots/main_en.png" width="720" alt="Main window: choosing a power plan"
title="Main menu PowerSetSetup">

<br><br>

<img src="docs/assets/screenshots/automode_en.png" width="720" alt="Automatic modes"
title="Automatic modes PowerSetSetup">

<br><br>

<img src="docs/assets/screenshots/advanced_en.png" width="720" alt="Advanced settings"
title="Advanced settings PowerSetSetup">

<details>
<summary>Other screens: "Settings" and "Advanced Scheme Settings"</summary>

<img src="docs/assets/screenshots/settings_en.png" width="480" alt="Settings menu"
title="Settings menu PowerSetSetup">
<img src="docs/assets/screenshots/settings2_en.png" width="480" alt="Advanced scheme settings"
title="Advanced scheme settings PowerSetSetup">

</details>

</div>


## 💡 Why PowerSetSetup

- **One screen, one click.** The main modes are always in front of you.
- **Focused on one job.** It only manages power plans. It is not a "PC optimizer" that edits hundreds of unrelated settings, and it does not run background services.
- **Safe cleanup.** Find extra and hidden plans. The active plan can't be deleted by mistake.
- **Works in English and Russian.** Plans are identified by GUID, not by their translated names.
- **Free for personal use** under the PolyForm Noncommercial License.

## ✨ Features

- 🔍 View all power plans and see which one is active
- 🔄 **Activate** a plan: Maximum performance, Balanced or Power saving
- 🗑️ **Delete** unneeded plans one by one or find them by GUID
- ♻️ **Reset** to Windows default plans
- 🆔 Get the **ID (GUID)** of any plan
- 🎨 Two interface languages
- 🔔 Update check right inside the app (portable version too)

## 🚀 Installation

1. **▶** Download `PowerSetSetup_installer.exe` from [Releases](https://github.com/BrocatScript/PowerSetSetup/releases/latest)
2. **📁** Choose the install path
3. **⏳** Wait for the installation to finish
4. **✅** Launch the app and pick your power plan

**Requirements:** Windows 10 or 11.

## ⚠️ Important Notes

| | Note |
|---|---|
| 🔁 | Resetting to defaults can remove your custom plans |
| 🪟 | Requires **Windows 10/11**, older versions are not supported |
| 🛡️ | Download only from the official [Releases](https://github.com/BrocatScript/PowerSetSetup/releases) page. If SmartScreen or your antivirus warns about a new unsigned program, check that the file came from this page before allowing it |

## 🛠️ Troubleshooting

1. Close resource-intensive programs and try again
2. Make sure you are on Windows 10 or 11
3. If the installer is blocked, see the note above about SmartScreen / antivirus
4. Still stuck? [Open an issue](https://github.com/BrocatScript/PowerSetSetup/issues) or write to **[brocatscript.support@gmail.com](mailto:brocatscript.support@gmail.com)**

## 📊 Statistics

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="stats/stats_dashboard_en_dark.png">
  <source media="(prefers-color-scheme: light)" srcset="stats/stats_dashboard_en_light.png">
  <img alt="PowerSetSetup Stats" src="stats/stats_dashboard_en_dark.png">
</picture>

*Updates within an hour or more...*

## 📜 License

[PolyForm Noncommercial License](https://github.com/BrocatScript/PowerSetSetup/blob/main/docs/LICENSE.md). Free for noncommercial use.

> Copyright © 2025-2026 BrocatScript.

## 💝 Support the Author

If the tool is useful to you, you can support its development:

[![Support](https://img.shields.io/badge/Support-Developer-FF6B6B?style=for-the-badge&logo=heart)](https://pay.cloudtips.ru/p/0cdee068)

Questions, ideas or collaboration: **[brocatscript.support@gmail.com](mailto:brocatscript.support@gmail.com)**

<div align="center">

**Made with ❤️ by BrocatScript**

</div>

---

<a id="русский"></a>

# Русский

> **Переключайте схемы электропитания Windows в один клик и удаляйте ненужные. Без поисков по панели управления и без команд `powercfg`.**

<div align="center">

[![Download](https://img.shields.io/badge/⬇️%20Скачать-brightgreen?style=for-the-badge&logo=windows)](https://github.com/BrocatScript/PowerSetSetup/releases/latest)

[![Releases](https://img.shields.io/badge/🚀%20Релизы-Доступные%20Версии-blue?style=for-the-badge&logo=github)](https://github.com/BrocatScript/PowerSetSetup/releases)
[![Issues](https://img.shields.io/badge/🐞%20Проблемы-Сообщить-red?style=for-the-badge&logo=github)](https://github.com/BrocatScript/PowerSetSetup/issues)
[![Pull Requests](https://img.shields.io/badge/🔀%20PRs-Слияния-green?style=for-the-badge&logo=github)](https://github.com/BrocatScript/PowerSetSetup/pulls)
[![Wiki](https://img.shields.io/badge/📚%20Wiki-Документация-lightgrey?style=for-the-badge&logo=readthedocs)](https://github.com/BrocatScript/PowerSetSetup/wiki)
[![News](https://img.shields.io/badge/📰%20Новости-lightgrey?style=for-the-badge&logo=readthedocs)](https://github.com/BrocatScript/PowerSetSetup/blob/main/docs/NEWS.md)
[![Source](https://img.shields.io/badge/📁%20Source-Код-black?style=for-the-badge&logo=github)](https://github.com/BrocatScript/PowerSetSetup)

</div>

## 🤔 Что это и для кого

В Windows есть схемы электропитания: они определяют, что важнее для компьютера: скорость или экономия энергии. Переключаться между ними неудобно: нужная схема часто спрятана в панели управления, вообще отсутствует или доступна только через `powercfg` с длинными GUID.

**PowerSetSetup** выводит на один экран три режима, которыми реально пользуются:

| Режим | Когда нужен |
|---|---|
| ⚡ **Максимальная производительность** | Игры, рендер, сборка проектов: когда важна скорость |
| ⚖️ **Сбалансированная** | Повседневная работа |
| 🔋 **Экономия энергии** | Ноутбук вдали от розетки: когда важна автономность |

Выбрали режим и готово. Программа управляет теми же стандартными схемами Windows через встроенную утилиту `powercfg` и не меняет скрытые системные параметры.

**Она подойдёт вам, если** вы переключаетесь между игровым и экономным режимами, список схем засорён производителями ноутбуков или вы просто не хотите работать с командной строкой.

## 🖼️ Скриншоты

<div align="center">

<img src="docs/assets/screenshots/main_ru.png" width="720" alt="Главное окно: выбор схемы электропитания"
title="Главное меню PowerSetSetup">

<br><br>

<img src="docs/assets/screenshots/automode_ru.png" width="720" alt="Автоматическая настройка"
title="Автоматические настройки PowerSetSetup">

<br><br>

<img src="docs/assets/screenshots/advanced_ru.png" width="720" alt="Расширенные параметры"
title="Расширенные параметры PowerSetSetup">

<details>
<summary>Другие экраны: «Настройки» и «Дополнительные настройки схемы»</summary>

<img src="docs/assets/screenshots/settings_ru.png" width="480" alt="Меню Настройки"
title="Меню настроек PowerSetSetup">
<img src="docs/assets/screenshots/settings2_ru.png" width="480" alt="Расширенные настройки схем"
title="Расширенные настройки схем PowerSetSetup">

</details>

</div>

## 💡 Почему PowerSetSetup

- **Один экран, один клик.** Основные режимы всегда перед глазами.
- **Одна задача.** Только схемы электропитания. Это не «оптимизатор ПК», который правит сотни посторонних параметров, и у программы нет фоновых служб.
- **Безопасная очистка.** Найдите лишние схемы и скрытые. Активную схему нельзя удалить по ошибке.
- **Работает на Русском и Английском.** Схемы определяются по GUID, а не по переведённому названию.
- **Бесплатно для личного использования** по лицензии PolyForm Noncommercial.

## ✨ Возможности

- 🔍 Просмотр всех схем и отметка активной
- 🔄 **Активация** схемы: Максимальная производительность, Сбалансированная или Экономия энергии
- 🗑️ **Удаление** ненужных схем по одной или поиск по GUID
- ♻️ **Сброс** до стандартных схем Windows
- 🆔 Получение **ID (GUID)** любой схемы
- 🎨 Два языка интерфейса
- 🔔 Проверка обновлений прям в приложении(для портативных тоже)

## 🚀 Установка

1. **▶** Скачайте `PowerSetSetup_installer.exe` из [Релизов](https://github.com/BrocatScript/PowerSetSetup/releases/latest)
2. **📁** Выберите путь установки
3. **⏳** Дождитесь завершения установки
4. **✅** Запустите программу и выберите схему питания

**Требования:** Windows 10 или 11.

## ⚠️ Важные примечания

| | Примечание |
|---|---|
| 🔁 | Сброс до стандартных настроек может удалить ваши пользовательские схемы |
| 🪟 | Нужна **Windows 10/11**, более ранние версии не поддерживаются |
| 🛡️ | Скачивайте только со страницы [Релизов](https://github.com/BrocatScript/PowerSetSetup/releases). Если SmartScreen или антивирус предупреждает о новой программе без подписи, убедитесь, что файл скачан именно оттуда, и только потом разрешайте запуск |

## 🛠️ Если что-то не работает

1. Закройте ресурсоёмкие программы и повторите попытку
2. Убедитесь, что у вас Windows 10 или 11
3. Если установщик блокируется, см. примечание выше про SmartScreen и антивирус
4. Не помогло? [Создайте Issue](https://github.com/BrocatScript/PowerSetSetup/issues) или напишите на **[brocatscript.support@gmail.com](mailto:brocatscript.support@gmail.com)**

## 📊 Статистика

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="stats/stats_dashboard_ru_dark.png">
  <source media="(prefers-color-scheme: light)" srcset="stats/stats_dashboard_ru_light.png">
  <img alt="PowerSetSetup Stats" src="stats/stats_dashboard_ru_dark.png">
</picture>

*Обновляется в течение часа или более...*

## 📜 Лицензия

[PolyForm Noncommercial License](https://github.com/BrocatScript/PowerSetSetup/blob/main/docs/LICENSE.md). Бесплатно для некоммерческого использования.

> Copyright © 2025-2026 BrocatScript.

## 💝 Поддержите автора

Если программа вам полезна, можно поддержать её разработку:

[![Support](https://img.shields.io/badge/Поддержать-Разработчика-FF6B6B?style=for-the-badge&logo=heart)](https://pay.cloudtips.ru/p/0cdee068)

Вопросы, идеи, сотрудничество: **[brocatscript.support@gmail.com](mailto:brocatscript.support@gmail.com)**

<div align="center">

**Сделано с ❤️ BrocatScript**

</div>
