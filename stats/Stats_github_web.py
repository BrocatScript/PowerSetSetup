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

def load_history():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_history(history):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4, ensure_ascii=False)
    except Exception as e:
        log_message(f"Ошибка сохранения базы данных: {e}")

def update_text_log(history):
    try:
        with open(TXT_FILE, "w", encoding="utf-8") as f:
            f.write("=== ИСТОРИЯ ЗАГРУЗОК PowerSetSetup (ОБНОВЛЯЕМЫЙ ЛОГ) ===\n")
            f.write("Этот файл обновляется автоматически при каждом запуске скрипта.\n\n")
            
            all_dates = sorted(history.keys())
            for idx, d_str in enumerate(all_dates):
                record = history[d_str]
                d_obj = datetime.date.fromisoformat(d_str)
                formatted_date = d_obj.strftime("%d.%m.%Y")
                
                if idx > 0:
                    prev_record = history[all_dates[idx-1]]
                    day_change = record["total"] - prev_record["total"]
                    prev_assets = prev_record["assets"]
                else:
                    day_change = record["total"] - record.get("initial_total", record["total"])
                    prev_assets = record.get("initial_assets", record["assets"])
                    
                sign = "+" if day_change >= 0 else ""
                f.write(f"[{formatted_date}] Всего установок: {record['total']} ({sign}{day_change} за день)\n")
                
                for asset_name, count in sorted(record["assets"].items(), key=lambda x: x[1], reverse=True):
                    prev_count = prev_assets.get(asset_name, count)
                    a_change = count - prev_count
                    a_sign = "+" if a_change >= 0 else ""
                    f.write(f"   -> {asset_name}: {count} ({a_sign}{a_change})\n")
                f.write("\n")
    except Exception as e:
        log_message(f"Ошибка записи в текстовый лог: {e}")

def get_delta_numeric(history, current_total, days_ago):
    today_dt = datetime.date.today()
    target_date = (today_dt - datetime.timedelta(days=days_ago)).isoformat()
    past_dates = sorted([d for d in history.keys() if d <= target_date])
    if not past_dates:
        all_dates = sorted(history.keys())
        if all_dates:
            return current_total - history[all_dates[0]]["total"]
        return 0
    ref_date = past_dates[-1]
    return current_total - history[ref_date]["total"]

def save_single_dashboard(style_name, file_path, is_dark, history, current_assets, current_total, today_formatted):
    """Внутренний метод генерации структуры графиков под конкретную тему оформления."""
    with plt.style.context(style_name):
        fig = plt.figure(figsize=(16, 12), facecolor='#121212' if is_dark else '#ffffff')
        fig.suptitle(f"Аналитический дашборд PowerSetSetup ({today_formatted})", 
                     fontsize=18, fontweight='bold', y=0.96, color='#ffffff' if is_dark else '#000000')

        # --- ГРАФИК 1: Линейная динамика ---
        ax1 = plt.subplot(2, 2, 1, facecolor='#1e1e1e' if is_dark else '#fbfbfb')
        all_keys = sorted(history.keys())
        
        # Ограничение до 15 промежутков: самый первый остается всегда, старые в центре скрываются
        if len(all_keys) <= 15:
            chart_dates = all_keys
        else:
            chart_dates = [all_keys[0]] + all_keys[-14:]
            
        dates_labels = [datetime.date.fromisoformat(d).strftime("%d.%m") for d in chart_dates]
        
        growth_values = []
        for d_str in chart_dates:
            idx = all_keys.index(d_str)
            if idx > 0:
                growth_values.append(history[d_str]["total"] - history[all_keys[idx-1]]["total"])
            else:
                growth_values.append(history[d_str]["total"] - history[d_str].get("initial_total", history[d_str]["total"]))
        
        # ЖЕСТКАЯ ФИКСАЦИЯ ЦЕЛЫХ ЧИСЕЛ (убирает любые точки, сотые и тысячные)
        ax1.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
        ax1.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%d'))
        
        # Управление границами оси Y, чтобы точки левитировали и не резались рамкой
        max_g = max(growth_values) if growth_values else 5
        min_g = min(growth_values) if growth_values else 0
        
        if max_g == min_g:
            # Если всё плоско (например, везде нули), поднимаем линию на 0.5 вверх
            ax1.set_ylim(min_g - 0.015, max_g + 4.5) 
        else:
            # Даем полушаг вниз и запас вверх, чтобы маркеры точек плавали в воздухе
            ax1.set_ylim(min_g - 0.015, max_g + 1.5)
            
        line_color = '#00adb5' if is_dark else '#1f77b4'
        ax1.plot(dates_labels, growth_values, marker='o', linewidth=2.5, color=line_color, label='Установки')
        ax1.fill_between(dates_labels, growth_values, color=line_color, alpha=0.15)
        ax1.set_title("Динамика новых скачиваний по дням", fontsize=12, fontweight='bold', color='#ffffff' if is_dark else '#000000', pad=10)
        ax1.set_xlabel("Дни (Дата)", color='#aaaaaa' if is_dark else '#555555')
        ax1.set_ylabel("Прирост установок", color='#aaaaaa' if is_dark else '#555555')
        ax1.grid(True, linestyle='--', alpha=0.2 if is_dark else 0.5, color='#ffffff' if is_dark else '#cccccc')
        ax1.tick_params(colors='#ffffff' if is_dark else '#000000')

        # --- ГРАФИК 2: Сравнение периодов ("Башенки") ---
        ax2 = plt.subplot(2, 2, 2, facecolor='#1e1e1e' if is_dark else '#fbfbfb')
        periods = ['Неделя', 'Месяц', 'Год', 'Всё время']
        p_values = [
            get_delta_numeric(history, current_total, 7),
            get_delta_numeric(history, current_total, 30),
            get_delta_numeric(history, current_total, 365),
            current_total
        ]
        
        bar_colors = ['#00e676', '#9b5de5', '#ff9f43', '#ff2e63'] if is_dark else ['#2ca02c', '#9467bd', '#ff7f0e', '#d62728']
        bars = ax2.bar(periods, p_values, color=bar_colors, width=0.5)
        ax2.set_title("Сравнение показателей за периоды", fontsize=12, fontweight='bold', color='#ffffff' if is_dark else '#000000', pad=10)
        ax2.set_ylabel("Число скачиваний", color='#aaaaaa' if is_dark else '#555555')
        ax2.grid(axis='y', linestyle='--', alpha=0.2 if is_dark else 0.5, color='#ffffff' if is_dark else '#cccccc')
        ax2.tick_params(colors='#ffffff' if is_dark else '#000000')

        # АВТОМАТИЧЕСКИЙ ЛИМИТ ОСИ Y (добавляет 20% запаса сверху, чтобы столбики и текст красиво помещались)
        max_val = max(p_values) if p_values else 10
        ax2.set_ylim(0, max_val * 1.2 if max_val > 0 else 10)
        
        for i, bar in enumerate(bars):
            height = bar.get_height()
            # Для "Всё время" плюс не ставим, для остальных — только при изменении > 0
            if periods[i] == 'Всё время':
                label_text = f'{height}'
            else:
                label_text = f'+{height}' if height > 0 else f'{height}'
                
            ax2.annotate(label_text,
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 4),  
                        textcoords="offset points",
                        ha='center', va='bottom', fontweight='bold', color='#ffffff' if is_dark else '#000000')

        # --- ГРАФИК 3: Круговая диаграмма долей популярных файлов ---
        ax3 = plt.subplot(2, 1, 2, facecolor='#121212' if is_dark else '#ffffff')
        sorted_files = sorted(current_assets.items(), key=lambda x: x[1], reverse=True)
        
        # Получаем данные за прошлый запуск для вычисления сегодняшнего изменения (+число)
        all_dates = sorted(history.keys())
        prev_assets = {}
        if len(all_dates) > 1:
            prev_assets = history[all_dates[-2]].get("assets", {})
        else:
            today_str = all_dates[0] if all_dates else ""
            if today_str:
                prev_assets = history[today_str].get("initial_assets", history[today_str].get("assets", {}))

        pie_values = []
        legend_labels = []
        other_sum = 0
        other_change_sum = 0
        
        for idx, (name, count) in enumerate(sorted_files):
            prev_count = prev_assets.get(name, count)
            asset_change = count - prev_count
            change_str = f" +{asset_change}" if asset_change > 0 else ""
            
            if idx < 5:
                pie_values.append(count)
                legend_labels.append(f"{name} ({count} шт.){change_str}")
            else:
                other_sum += count
                other_change_sum += asset_change
                
        if other_sum > 0:
            pie_values.append(other_sum)
            other_change_str = f" +{other_change_sum}" if other_change_sum > 0 else ""
            legend_labels.append(f"Другие файлы ({other_sum} шт.){other_change_str}")
            
        if sum(pie_values) > 0:
            pie_colors = ['#00adb5', '#ff2e63', '#00e676', '#f8b500', '#9b5de5', '#ff9f43'] if is_dark else ['#5dade2', '#e74c3c', '#2ecc71', '#f1c40f', '#9b5de5', '#e67e22']
            
            wedges, texts, autotexts = ax3.pie(
                pie_values, 
                labels=None, 
                autopct='%1.1f%%', 
                startangle=140, 
                colors=pie_colors[:len(pie_values)],
                pctdistance=0.7,
                textprops={'color': '#ffffff' if is_dark else '#000000', 'fontsize': 11, 'weight': 'bold'}
            )
            
            leg = ax3.legend(
                wedges, 
                legend_labels, 
                title="Файлы (Полные имена):", 
                loc="center left", 
                bbox_to_anchor=(1.0, 0.5), 
                facecolor='#1e1e1e' if is_dark else '#f5f5f5', 
                edgecolor='#333333' if is_dark else '#cccccc',
                fontsize=10
            )
            plt.setp(leg.get_texts(), color='#ffffff' if is_dark else '#000000')
            plt.setp(leg.get_title(), color='#ffffff' if is_dark else '#000000')
            
            ax3.set_title("Доли популярности файлов от общего объема скачиваний", fontsize=12, fontweight='bold', color='#ffffff' if is_dark else '#000000', pad=15)
        else:
            ax3.text(0.5, 0.5, "Нет данных", ha='center', va='center', color='#ffffff' if is_dark else '#000000')
            ax3.axis('off')

        plt.tight_layout(rect=[0, 0.02, 0.98, 0.93])
        # hspace — расстояние по вертикали, wspace — по горизонтали между 1 и 2 графиком
        fig.subplots_adjust(hspace=0.45, wspace=0.35) 
        
        plt.savefig(file_path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
        
        plt.savefig(file_path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close()

def generate_visual_dashboards(history, current_assets, current_total):
    """Генерирует две независимые картинки с постоянными именами, перезаписывая старые."""
    try:
        today_formatted = datetime.date.today().strftime("%d.%m.%Y")
        
        # Жестко фиксируем имена БЕЗ даты
        img_dark_path = os.path.join(SCRIPT_DIR, "stats_dashboard_dark.png")
        img_light_path = os.path.join(SCRIPT_DIR, "stats_dashboard_light.png")
        
        # 1. Генерируем Тёмный Дашборд
        save_single_dashboard('dark_background', img_dark_path, True, history, current_assets, current_total, today_formatted)
        
        # 2. Генерируем Светлый Дашборд
        save_single_dashboard('default', img_light_path, False, history, current_assets, current_total, today_formatted)
        
        log_message("Графика успешно обновлена и перезаписана:")
        log_message(f" -> Тёмная тема: {os.path.basename(img_dark_path)}")
        log_message(f" -> Светлая тема: {os.path.basename(img_light_path)}")
                        
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

def main():
    status()

if __name__ == "__main__":
    main()