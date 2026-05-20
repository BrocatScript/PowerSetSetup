import sys
import os
import psutil
from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
                               QWidget, QLabel, QProgressBar, QFrame, QMessageBox)
from PySide6.QtGui import QFont, QAction

class SystemMonitorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Монитор системы")
        self.setFixedSize(500, 650)
        self.setStyleSheet("""
            QMainWindow { background-color: #2c3e50; }
            QFrame {
                background-color: #34495e;
                border-radius: 15px;
                padding: 10px;
                margin: 5px;
            }
            QLabel {
                color: #ecf0f1;
                font-size: 14px;
                font-weight: bold;
            }
            QProgressBar {
                border-radius: 10px;
                background-color: #2c3e50;
                text-align: center;
                color: white;
                font-weight: bold;
                height: 25px;
            }
            QProgressBar::chunk {
                border-radius: 10px;
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                  stop:0 #3498db, stop:1 #2ecc71);
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("📊 Системная нагрузка")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #ecf0f1; margin-bottom: 10px;")
        main_layout.addWidget(title)

        self.cpu_card = self.create_card("🖥️  CPU", "Центральный процессор")
        self.ram_card = self.create_card("🧠  RAM", "Оперативная память")
        self.disk_card = self.create_card("💾  DISK", "Диск (системный)")

        main_layout.addWidget(self.cpu_card["frame"])
        main_layout.addWidget(self.ram_card["frame"])
        main_layout.addWidget(self.disk_card["frame"])

        # Меню
        menubar = self.menuBar()
        help_menu = menubar.addMenu("Помощь")
        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)
        self.update_stats()

    def create_card(self, icon_title, subtitle):
        frame = QFrame()
        layout = QVBoxLayout(frame)
        title_label = QLabel(icon_title)
        title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        layout.addWidget(title_label)
        sub_label = QLabel(subtitle)
        sub_label.setStyleSheet("font-size: 11px; color: #bdc3c7;")
        layout.addWidget(sub_label)
        progress_bar = QProgressBar()
        progress_bar.setRange(0, 100)
        progress_bar.setValue(0)
        progress_bar.setFormat("%p%")
        layout.addWidget(progress_bar)
        value_label = QLabel("Загрузка: 0%")
        value_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(value_label)
        return {"frame": frame, "progress": progress_bar, "value_label": value_label}

    def update_stats(self):
        # CPU
        cpu_percent = psutil.cpu_percent(interval=0.5)
        self.cpu_card["progress"].setValue(int(cpu_percent))
        self.cpu_card["value_label"].setText(f"Загрузка: {cpu_percent:.1f}%")
        self.set_progress_color(self.cpu_card["progress"], cpu_percent)

        # RAM
        mem = psutil.virtual_memory()
        ram_percent = mem.percent
        self.ram_card["progress"].setValue(int(ram_percent))
        used_gb = mem.used / (1024**3)
        total_gb = mem.total / (1024**3)
        self.ram_card["value_label"].setText(
            f"Использовано: {used_gb:.1f} / {total_gb:.1f} ГБ ({ram_percent:.1f}%)"
        )
        self.set_progress_color(self.ram_card["progress"], ram_percent)

        # Disk
        try:
            if os.name == 'nt':
                disk_path = 'C:\\'
            else:
                disk_path = '/'
            disk_usage = psutil.disk_usage(disk_path)
            disk_percent = disk_usage.percent
            self.disk_card["progress"].setValue(int(disk_percent))
            used_gb = disk_usage.used / (1024**3)
            total_gb = disk_usage.total / (1024**3)
            self.disk_card["value_label"].setText(
                f"Занято: {used_gb:.1f} / {total_gb:.1f} ГБ ({disk_percent:.1f}%)"
            )
            self.set_progress_color(self.disk_card["progress"], disk_percent)
        except Exception as e:
            self.disk_card["value_label"].setText(f"Ошибка: {str(e)}")

    def set_progress_color(self, progress_bar, value):
        if value < 50:
            color = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2ecc71, stop:1 #27ae60)"
        elif value < 80:
            color = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f39c12, stop:1 #e67e22)"
        else:
            color = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #e74c3c, stop:1 #c0392b)"
        progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border-radius: 10px;
                background-color: #2c3e50;
                text-align: center;
                color: white;
                font-weight: bold;
                height: 25px;
            }}
            QProgressBar::chunk {{
                border-radius: 10px;
                background-color: {color};
            }}
        """)

    def show_about(self):
        QMessageBox.about(self, "О программе",
                          "Монитор системы\n\n"
                          "Использует WMI для получения загрузки GPU.\n"
                          "Работает с видеокартами AMD, NVIDIA, Intel на Windows 10/11.\n\n"
                          "Для установки зависимостей:\n"
                          "pip install PySide6 psutil wmi")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SystemMonitorApp()
    window.show()
    sys.exit(app.exec())