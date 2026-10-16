import requests
from collections import defaultdict
import os
from time import sleep
import json
import datetime
import sys
import subprocess
import glob
import platform
import math  # добавлено для округления
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
 
REPO_OWNER = "BrocatScript"
REPO_NAME = "PowerSetSetup"
API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases"
 
# Пути к файлам внутри папки проекта
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(SCRIPT_DIR, "stats_database.json")
TXT_FILE = os.path.join(SCRIPT_DIR, "stats_history.txt")
CONFIG_FILE = os.path.join(SCRIPT_DIR, "stats_config.json")
 
def clear():
    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() == "Linux":
        os.system("clear")
    elif platform.system() == "MacOS":
        os.system("clean")
 
def log_message(text):
    """Выводит чистый и аккуратный лог работы со временем."""
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{current_time}] {text}")
 
def load_config():
    """Загружает файл настроек автоматического открытия файла."""
    default_config = {"auto_open_on_exit": "dark_image"} # Допустимые: dark_image, light_image, text_log, none
    if not os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(default_config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            log_message(f"Предупреждение: Не удалось создать конфиг: {e}")
        return default_config
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default_config
 
def open_file_by_config(config, today_str):
    """Автоматически открывает выбранный в конфиге файл при выходе из программы."""
    choice = config.get("auto_open_on_exit", "none")
    target_file = None
    
    if choice == "dark_image":
        target_file = os.path.join(SCRIPT_DIR, f"stats_dashboard_{today_str}_dark.png")
    elif choice == "light_image":
        target_file = os.path.join(SCRIPT_DIR, f"stats_dashboard_{today_str}_light.png")
    elif choice == "text_log":
        target_file = TXT_FILE
 
    if target_file and os.path.exists(target_file):
        log_message(f"Автоматическое открытие файла: {os.path.basename(target_file)}...")
        try:
            if sys.platform == "win32":
                os.startfile(target_file)
            elif sys.platform == "darwin":
                subprocess.run(["open", target_file])
            else:
                subprocess.run(["xdg-open", target_file])
        except Exception as e:
            log_message(f"Ошибка при автоматическом открытии файла: {e}")
 
DB_FORMAT = 2
 
def _encode_history(history):
    """Полная история -> компактный формат: по каждому дню только изменения.
 
    {"_format": 2, "days": {"2026-10-16": {"t": 346, "d": {"файл": +8}, "r": ["удалённый"]}}}
    d — изменение счётчика файла за день (для нового файла — его значение),
    r — файлы, исчезшие из релизов. Стартовые значения (initial_*) нужны только первому дню.
    """
    days = {}
    prev = {}
    for idx, d_str in enumerate(sorted(history.keys())):
        rec = history[d_str]
        assets = rec.get("assets", {})
        entry = {"t": rec["total"]}
        changes = {n: c - prev.get(n, 0) for n, c in assets.items()
                   if n not in prev or c != prev[n]}
        if changes:
            entry["d"] = changes
        removed = [n for n in prev if n not in assets]
        if removed:
            entry["r"] = removed
        if idx == 0:
            # Стартовые значения пишем только если они отличаются от значений самого дня
            if rec.get("initial_total", rec["total"]) != rec["total"]:
                entry["it"] = rec["initial_total"]
            if rec.get("initial_assets", assets) != assets:
                entry["ia"] = rec["initial_assets"]
        days[d_str] = entry
        prev = assets
    return days
 
def _decode_history(days):
    """Компактный формат -> полная история в памяти (с ней работает весь остальной код)."""
    history = {}
    cur = {}
    for idx, d_str in enumerate(sorted(days.keys())):
        entry = days[d_str]
        cur = dict(cur)
        for n in entry.get("r", []):
            cur.pop(n, None)
        for n, delta in entry.get("d", {}).items():
            cur[n] = cur.get(n, 0) + delta
        rec = {"total": entry["t"], "assets": dict(cur)}
        if idx == 0:
            rec["initial_total"] = entry.get("it", entry["t"])
            rec["initial_assets"] = entry.get("ia", dict(cur))
        history[d_str] = rec
    return history
 
def load_history():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        log_message(f"Ошибка чтения базы данных: {e}")
        return {}
 
    if isinstance(data, dict) and data.get("_format") == DB_FORMAT:
        return _decode_history(data.get("days", {}))
 
    # Старый формат (полные данные за каждый день): один раз делаем резервную копию.
    # Сама миграция произойдёт при ближайшем сохранении.
    backup = os.path.join(SCRIPT_DIR, "stats_database.backup_v1.json")
    if not os.path.exists(backup):
        try:
            with open(backup, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
            log_message("База в старом формате: резервная копия stats_database.backup_v1.json создана.")
        except Exception as e:
            log_message(f"Предупреждение: не удалось создать резервную копию: {e}")
    return data
 
def save_history(history):
    """Сохраняет историю в компактном формате: один день — одна строка."""
    try:
        days = _encode_history(history)
        lines = [f"  {json.dumps(k)}: {json.dumps(v, ensure_ascii=False, separators=(',', ':'))}"
                 for k, v in days.items()]
        text = '{\n "_format": %d,\n "days": {\n%s\n }\n}\n' % (DB_FORMAT, ",\n".join(lines))
        tmp = DB_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, DB_FILE)  # атомарная замена: файл не повредится при сбое
    except Exception as e:
        log_message(f"Ошибка сохранения базы данных: {e}")
 
def update_text_log(history):
    """Текстовый лог: по каждому дню только файлы, у которых что-то изменилось.
    Для самого первого дня выводится полный стартовый список."""
    try:
        with open(TXT_FILE, "w", encoding="utf-8") as f:
            f.write("=== ИСТОРИЯ ЗАГРУЗОК PowerSetSetup (ОБНОВЛЯЕМЫЙ ЛОГ) ===\n")
            f.write("Этот файл обновляется автоматически при каждом запуске скрипта.\n")
            f.write("Для каждого дня показаны только файлы, у которых изменился счётчик.\n")
 
            all_dates = sorted(history.keys())
            changes_by_day = []
            for idx, d_str in enumerate(all_dates):
                record = history[d_str]
                if idx > 0:
                    prev_record = history[all_dates[idx-1]]
                    day_change = record["total"] - prev_record["total"]
                    prev_assets = prev_record["assets"]
                else:
                    day_change = record["total"] - record.get("initial_total", record["total"])
                    prev_assets = record.get("initial_assets", record["assets"])
                changes_by_day.append((d_str, record, day_change, prev_assets))
 
            if changes_by_day:
                best = max(changes_by_day, key=lambda x: x[2])
                if best[2] > 0:
                    best_date = datetime.date.fromisoformat(best[0]).strftime("%d.%m.%Y")
                    f.write(f"Рекордный день: {best_date} (+{best[2]})\n")
            f.write("\n")
 
            for idx, (d_str, record, day_change, prev_assets) in enumerate(changes_by_day):
                formatted_date = datetime.date.fromisoformat(d_str).strftime("%d.%m.%Y")
                sign = "+" if day_change >= 0 else ""
                f.write(f"[{formatted_date}] Всего установок: {record['total']} ({sign}{day_change} за день)\n")
 
                for asset_name, count in sorted(record["assets"].items(), key=lambda x: x[1], reverse=True):
                    a_change = count - prev_assets.get(asset_name, 0)
                    if a_change == 0 and idx > 0:
                        continue
                    a_sign = "+" if a_change >= 0 else ""
                    f.write(f"   -> {asset_name}: {count} ({a_sign}{a_change})\n")
                f.write("\n")
    except Exception as e:
        log_message(f"Ошибка записи в текстовый лог: {e}")
 
def get_period_start(period):
    """Дата начала текущего календарного периода: 'week' (с понедельника), 'month', 'year'."""
    today_dt = datetime.date.today()
    if period == "week":
        return today_dt - datetime.timedelta(days=today_dt.weekday())
    if period == "month":
        return today_dt.replace(day=1)
    if period == "year":
        return today_dt.replace(month=1, day=1)
    raise ValueError(period)
 
def get_period_baseline(history, period):
    """Базовая точка для календарного периода: последняя запись ДО его начала
    (итог предыдущего воскресенья / последнего дня прошлого месяца / прошлого года).
    Если истории до периода нет, берём стартовые значения самой первой записи.
    Возвращает (total, assets).
    """
    if not history:
        return 0, {}
    start = get_period_start(period).isoformat()
    before = sorted(d for d in history.keys() if d < start)
    if before:
        rec = history[before[-1]]
        return rec["total"], rec.get("assets", {})
    first = history[sorted(history.keys())[0]]
    return (first.get("initial_total", first["total"]),
            first.get("initial_assets", first.get("assets", {})))
 
def get_week_baseline(history):
    return get_period_baseline(history, "week")
 
def get_delta_numeric(history, current_total, days_ago):
    # Все периоды календарные: неделя — с понедельника, месяц — с 1-го числа, год — с 1 января.
    period = {7: "week", 30: "month", 365: "year"}[days_ago]
    base_total, _ = get_period_baseline(history, period)
    return current_total - base_total
 
def save_single_dashboard(style_name, file_path, is_dark, lang, history, current_assets, current_total, today_formatted):
    """Внутренний метод генерации структуры графиков под конкретную тему и язык."""
    t = {
        "ru": {
            "title": f"Аналитический дашборд PowerSetSetup ({today_formatted})",
            "downloads": "Установки",
            "g1_title": "Динамика новых скачиваний по дням (последние 7 дней)",
            "g1_x": "Дни (Дата)",
            "g1_y": "Прирост установок",
            "periods": ['Неделя', 'Месяц', 'Год', 'Всё время'],
            "g2_title": "Сравнение показателей за периоды",
            "g2_y": "Число скачиваний",
            "g3_title": "Доли популярности файлов от общего объема скачиваний",
            "g3_leg_title": "Файлы (Полные имена и прирост за неделю):",
            "g3_pcs": "шт.",
            "g3_other": "Другие файлы",
            "no_data": "Нет данных",
            "weekly_label": "за неделю"
        },
        "en": {
            "title": f"PowerSetSetup Analytical Dashboard ({today_formatted})",
            "downloads": "Downloads",
            "g1_title": "Daily Download Dynamics (last 7 days)",
            "g1_x": "Days (Date)",
            "g1_y": "Downloads Growth",
            "periods": ['Week', 'Month', 'Year', 'Total'],
            "g2_title": "Period Comparison",
            "g2_y": "Number of Downloads",
            "g3_title": "File Popularity Share of Total Downloads",
            "g3_leg_title": "Files (Full names & weekly growth):",
            "g3_pcs": "pcs",
            "g3_other": "Other files",
            "no_data": "No data",
            "weekly_label": "weekly"
        }
    }[lang]
 
    with plt.style.context(style_name):
        fig = plt.figure(figsize=(16, 12), facecolor='#121212' if is_dark else '#ffffff')
        fig.suptitle(t["title"], fontsize=18, fontweight='bold', y=0.96, color='#ffffff' if is_dark else '#000000')
 
        # --- ГРАФИК 1: Линейная динамика (последние N дней) ---
        ax1 = plt.subplot(2, 2, 1, facecolor='#1e1e1e' if is_dark else '#fbfbfb')
        
        DAYS_TO_SHOW = 7
        MIN_Y_MAX = 5
        
        all_keys = sorted(history.keys())
        chart_dates = all_keys[-DAYS_TO_SHOW:] if len(all_keys) >= DAYS_TO_SHOW else all_keys
        dates_labels = [datetime.date.fromisoformat(d).strftime("%d.%m") for d in chart_dates]
        
        growth_values = []
        for d_str in chart_dates:
            idx = all_keys.index(d_str)
            if idx > 0:
                growth_values.append(history[d_str]["total"] - history[all_keys[idx-1]]["total"])
            else:
                growth_values.append(history[d_str]["total"] - history[d_str].get("initial_total", history[d_str]["total"]))
        
        ax1.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True, nbins=8))
        
        if growth_values:
            data_min = min(growth_values)
            data_max = max(growth_values)
 
            if data_min >= 0:
                # Обычный случай (нет отрицательных значений): держим ноль
                # почти у самого низа графика — небольшой фиксированный
                # отступ, которого достаточно, чтобы точку было видно,
                # но недостаточно, чтобы визуально "поднимать" график.
                y_min = -0.1
            else:
                # Если есть провалы ниже нуля, отступ считаем от разброса
                # данных, чтобы самая нижняя точка не обрезалась по краю.
                data_range = data_max - data_min
                margin = max(0.5, data_range * 0.12)
                y_min = data_min - margin
 
            y_max = max(data_max + 1, MIN_Y_MAX)
 
            # "Красивое" округление вниз — но не раздуваем маленький
            # отступ у нуля (иначе ноль опять визуально уедет вверх).
            if y_min < -0.1:
                y_min = math.floor(y_min * 2) / 2
            y_max = math.ceil(y_max)
 
            if y_max - y_min < 2:
                y_max = y_min + 2
 
            ax1.set_ylim(y_min, y_max)
        else:
            ax1.set_ylim(-0.1, MIN_Y_MAX)
 
        # --- НОВАЯ ЛОГИКА ПОДБОРА ТИКОВ ---
        y_min, y_max = ax1.get_ylim()
        range_val = y_max - y_min
        
        # Выбираем "красивый" шаг
        if range_val <= 5:
            step = 1
        elif range_val <= 20:
            step = 2
        elif range_val <= 50:
            step = 5
        elif range_val <= 200:
            step = 25
        else:
            step = 50
        
        # Первый тик — округляем вниз, последний — вниз (чтобы не выходить за пределы)
        # Для положительной серии не показываем отрицательные тики:
        # отрицательный предел остаётся только как небольшой визуальный запас.
        first_tick = 0 if min(growth_values, default=0) >= 0 else math.floor(y_min / step) * step
        last_tick = math.floor(y_max / step) * step
        # Если last_tick == first_tick, добавляем один шаг вверх
        if last_tick <= first_tick:
            last_tick = first_tick + step
        # Генерируем список тиков
        ticks = list(range(int(first_tick), int(last_tick) + 1, int(step)))
        # Если тиков больше 10, увеличиваем шаг (пересчитываем)
        if len(ticks) > 10:
            # Увеличиваем шаг в 2 раза и пересчитываем
            step *= 2
            first_tick = math.floor(y_min / step) * step
            last_tick = math.floor(y_max / step) * step
            if last_tick <= first_tick:
                last_tick = first_tick + step
            ticks = list(range(int(first_tick), int(last_tick) + 1, int(step)))
        
        ax1.set_yticks(ticks)
        ax1.set_yticklabels([str(t) for t in ticks])
        
        line_color = '#00adb5' if is_dark else '#1f77b4'
        ax1.plot(dates_labels, growth_values, marker='o', linewidth=2.5, color=line_color, label=t["downloads"])
        ax1.fill_between(dates_labels, growth_values, color=line_color, alpha=0.15)
        
 
        
        ax1.set_title(t["g1_title"], fontsize=12, fontweight='bold', color='#ffffff' if is_dark else '#000000', pad=10)
        ax1.set_xlabel(t["g1_x"], color='#aaaaaa' if is_dark else '#555555')
        ax1.set_ylabel(t["g1_y"], color='#aaaaaa' if is_dark else '#555555')
        ax1.grid(True, linestyle='--', alpha=0.2 if is_dark else 0.5, color='#ffffff' if is_dark else '#cccccc')
        ax1.tick_params(colors='#ffffff' if is_dark else '#000000')
 
        # --- ГРАФИК 2: Сравнение периодов ---
        ax2 = plt.subplot(2, 2, 2, facecolor='#1e1e1e' if is_dark else '#fbfbfb')
        p_values = [
            get_delta_numeric(history, current_total, 7),
            get_delta_numeric(history, current_total, 30),
            get_delta_numeric(history, current_total, 365),
            current_total
        ]
        
        bar_colors = ['#00e676', '#9b5de5', '#ff9f43', '#ff2e63'] if is_dark else ['#2ca02c', '#9467bd', '#ff7f0e', '#d62728']
        bars = ax2.bar(t["periods"], p_values, color=bar_colors, width=0.5)
        ax2.set_title(t["g2_title"], fontsize=12, fontweight='bold', color='#ffffff' if is_dark else '#000000', pad=10)
        ax2.set_ylabel(t["g2_y"], color='#aaaaaa' if is_dark else '#555555')
        ax2.grid(axis='y', linestyle='--', alpha=0.2 if is_dark else 0.5, color='#ffffff' if is_dark else '#cccccc')
        ax2.tick_params(colors='#ffffff' if is_dark else '#000000')
 
        max_val = max(p_values) if p_values else 10
        ax2.set_ylim(0, max_val * 1.2 if max_val > 0 else 10)
        
        for i, bar in enumerate(bars):
            height = bar.get_height()
            if t["periods"][i] in ['Всё время', 'Total']:
                label_text = f'{height}'
            else:
                label_text = f'+{height}' if height > 0 else f'{height}'
                
            ax2.annotate(label_text, xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 4), textcoords="offset points",
                        ha='center', va='bottom', fontweight='bold', color='#ffffff' if is_dark else '#000000')
 
        # --- ГРАФИК 3: Круговая диаграмма ---
        ax3 = plt.subplot(2, 1, 2, facecolor='#121212' if is_dark else '#ffffff')
        sorted_files = sorted(current_assets.items(), key=lambda x: x[1], reverse=True)
        
        _, prev_assets = get_week_baseline(history)
 
        pie_values = []
        legend_labels = []
        other_sum = 0
        other_change_sum = 0
        
        for idx, (name, count) in enumerate(sorted_files):
            prev_count = prev_assets.get(name, 0)  # новый файл: все его скачивания — новые
            asset_change = count - prev_count
            change_str = f" (+{asset_change} {t['weekly_label']})" if asset_change > 0 else ""
            
            if idx < 5:
                pie_values.append(count)
                legend_labels.append(f"{name} ({count} {t['g3_pcs']}){change_str}")
            else:
                other_sum += count
                other_change_sum += asset_change
                
        if other_sum > 0:
            pie_values.append(other_sum)
            other_change_str = f" (+{other_change_sum} {t['weekly_label']})" if other_change_sum > 0 else ""
            legend_labels.append(f"{t['g3_other']} ({other_sum} {t['g3_pcs']}){other_change_str}")
            
        if sum(pie_values) > 0:
            pie_colors = ['#00adb5', '#ff2e63', '#00e676', '#f8b500', '#9b5de5', '#ff9f43'] if is_dark else ['#5dade2', '#e74c3c', '#2ecc71', '#f1c40f', '#9b5de5', '#e67e22']
            
            # Адаптивные подписи процентов: слишком маленькие сектора
            # не получают текст, а для небольших секторов шрифт уменьшается.
            def adaptive_autopct(pct):
                # Показываем даже маленькие, но реально читаемые сектора.
                # Совсем крошечные (меньше 2%) лучше оставить без текста.
                if pct < 2.0:
                    return ""
                return f"{pct:.1f}%"
 
            wedges, texts, autotexts = ax3.pie(
                pie_values, labels=None, autopct=adaptive_autopct, startangle=140,
                colors=pie_colors[:len(pie_values)], pctdistance=0.68,
                textprops={
                    'color': '#ffffff' if is_dark else '#000000',
                    'fontsize': 11,
                    'weight': 'bold'
                }
            )
 
            for wedge, autotext in zip(wedges, autotexts):
                pct = (wedge.theta2 - wedge.theta1) / 360.0 * 100.0
                if not autotext.get_text():
                    continue
 
                if pct >= 50:
                    fontsize = 14
                elif pct >= 20:
                    fontsize = 11
                elif pct >= 10:
                    fontsize = 9.5
                elif pct >= 6:
                    fontsize = 8
                elif pct >= 4:
                    fontsize = 7
                else:
                    fontsize = 6.2
 
                autotext.set_fontsize(fontsize)
 
            leg = ax3.legend(wedges, legend_labels, title=t["g3_leg_title"], loc="center left", bbox_to_anchor=(1.0, 0.5), 
                             facecolor='#1e1e1e' if is_dark else '#f5f5f5', edgecolor='#333333' if is_dark else '#cccccc', fontsize=10)
            plt.setp(leg.get_texts(), color='#ffffff' if is_dark else '#000000')
            plt.setp(leg.get_title(), color='#ffffff' if is_dark else '#000000')
            
            ax3.set_title(t["g3_title"], fontsize=12, fontweight='bold', color='#ffffff' if is_dark else '#000000', pad=15)
        else:
            ax3.text(0.5, 0.5, t["no_data"], ha='center', va='center', color='#ffffff' if is_dark else '#000000')
            ax3.axis('off')
 
        plt.tight_layout(rect=[0, 0.02, 0.98, 0.93])
        fig.subplots_adjust(hspace=0.45, wspace=0.35) 
        plt.savefig(file_path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close()
 
def generate_visual_dashboards(history, current_assets, current_total):
    """Генерирует 4 независимые картинки: (RU/EN) x (Dark/Light)."""
    try:
        today_formatted = datetime.date.today().strftime("%d.%m.%Y")
        
        save_single_dashboard('dark_background', os.path.join(SCRIPT_DIR, "stats_dashboard_ru_dark.png"), True, "ru", history, current_assets, current_total, today_formatted)
        save_single_dashboard('default', os.path.join(SCRIPT_DIR, "stats_dashboard_ru_light.png"), False, "ru", history, current_assets, current_total, today_formatted)
        
        save_single_dashboard('dark_background', os.path.join(SCRIPT_DIR, "stats_dashboard_en_dark.png"), True, "en", history, current_assets, current_total, today_formatted)
        save_single_dashboard('default', os.path.join(SCRIPT_DIR, "stats_dashboard_en_light.png"), False, "en", history, current_assets, current_total, today_formatted)
        
        log_message("Все 4 дашборда (RU/EN, Dark/Light) успешно обновлены.")
                        
    except Exception as e:
        log_message(f"КРИТИЧЕСКАЯ ОШИБКА генерации графиков: {e}")
 
def get_all_releases():
    releases = []
    url = API_URL
    while url:
        response = requests.get(url)
        response.raise_for_status()
        releases.extend(response.json())
        if "next" in response.links:
            url = response.links["next"]["url"]
        else:
            url = None
    return releases
 
def status():
    log_message("Запрос актуальных данных с GitHub API...")
    try:
        releases = get_all_releases()
    except requests.exceptions.RequestException as e:
        log_message(f"ОШИБКА API: Не удалось связаться с сервером: {e}")
        return
 
    if not releases:
        log_message("ОШИБКА API: Список релизов пуст.")
        return
 
    asset_downloads = defaultdict(int)
    total_downloads = 0
 
    for release in releases:
        for asset in release.get("assets", []):
            name = asset["name"]
            count = asset.get("download_count", 0)
            asset_downloads[name] += count
            total_downloads += count
 
    current_total = total_downloads
    current_assets = dict(asset_downloads)
    today_str = datetime.date.today().isoformat()
 
    history = load_history()
    past_dates = sorted([d for d in history.keys() if d < today_str])
 
    if past_dates:
        baseline_total = history[past_dates[-1]]["total"]
        baseline_assets = history[past_dates[-1]]["assets"]
    else:
        if today_str in history:
            baseline_total = history[today_str].get("initial_total", history[today_str]["total"])
            baseline_assets = history[today_str].get("initial_assets", history[today_str]["assets"])
        else:
            baseline_total = current_total
            baseline_assets = current_assets
 
    if today_str in history:
        history[today_str]["total"] = current_total
        history[today_str]["assets"] = current_assets
    else:
        history[today_str] = {
            "total": current_total,
            "assets": current_assets,
            "initial_total": baseline_total if past_dates else current_total,
            "initial_assets": baseline_assets if past_dates else current_assets
        }
    
    save_history(history)
    log_message("База данных локальной истории (JSON) обновлена.")
    
    update_text_log(history)
    log_message("Текстовый лог-файл (stats_history.txt) успешно перезаписан.")
    
    # Генерация графических панелей
    generate_visual_dashboards(history, current_assets, current_total)
 
    # ВЫВОД СПИСКА СКАЧИВАНИЙ ЗА НЕДЕЛЮ В КОНСОЛЬ
    print("\n" + "="*70)
    log_message("СТАТИСТИКА СКАЧИВАНИЙ ПО ВЕРСИЯМ ЗА ТЕКУЩУЮ НЕДЕЛЮ (с понедельника):")
    _, ref_assets_7d = get_week_baseline(history)
 
    for name, count in sorted(current_assets.items(), key=lambda x: x[1], reverse=True):
        prev_count = ref_assets_7d.get(name, 0)
        diff = count - prev_count
        print(f"  • {name}: {count} шт. (За неделю: +{diff})")
    print("="*70 + "\n")
 
def main():
    status()
 
if __name__ == "__main__":
    main()
