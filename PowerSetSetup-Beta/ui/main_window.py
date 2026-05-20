import sys
import subprocess
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QLabel, QLineEdit, QMessageBox,
    QListWidget, QListWidgetItem, QComboBox
)
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator, QIcon, QFont, QAction
from PySide6.QtCore import Signal, QObject

# ==================== Работа с электропитанием ====================
class PowerManager:
    """Класс для взаимодействия со схемами электропитания Windows через powercfg"""

    @staticmethod
    def get_power_schemes():
        """Возвращает список доступных схем: [(GUID, имя), ...]"""
        try:
            output = subprocess.check_output(
                ["powercfg", "/list"],
                encoding="cp866",  # для русской Windows
                stderr=subprocess.STDOUT
            )
            schemes = []
            for line in output.splitlines():
                if "Guid" in line or "Схема" in line:
                    # Пример: "Схема электропитания: GUID: 381b4222-f694-41f0-9685-ff5bb260df2e  (Сбалансированная)"
                    parts = line.split(":")
                    if len(parts) >= 3:
                        guid_part = parts[1].strip()
                        guid = guid_part.split()[0]
                        name = parts[2].strip().strip("()")
                        schemes.append((guid, name))
            return schemes
        except Exception as e:
            print(f"Ошибка получения схем: {e}")
            return []

    @staticmethod
    def get_active_scheme():
        """Возвращает GUID активной схемы"""
        try:
            output = subprocess.check_output(
                ["powercfg", "/getactivescheme"],
                encoding="cp866"
            )
            # Вывод: "Схема электропитания: GUID: 381b4222-f694-41f0-9685-ff5bb260df2e  (Сбалансированная)"
            parts = output.split(":")
            if len(parts) >= 2:
                guid = parts[1].strip().split()[0]
                return guid
        except Exception:
            return None

    @staticmethod
    def set_active_scheme(guid):
        """Устанавливает активную схему по GUID"""
        try:
            subprocess.run(["powercfg", "/setactive", guid], check=True)
            return True
        except Exception:
            return False

    @staticmethod
    def set_monitor_timeout(minutes):
        """Устанавливает таймаут отключения монитора (в минутах) для активной схемы"""
        try:
            seconds = minutes * 60
            subprocess.run(["powercfg", "/change", "monitor-timeout-ac", str(minutes)], check=True)
            subprocess.run(["powercfg", "/change", "monitor-timeout-dc", str(minutes)], check=True)
            return True
        except Exception:
            return False

    @staticmethod
    def set_disk_timeout(minutes):
        """Таймаут отключения диска"""
        try:
            subprocess.run(["powercfg", "/change", "disk-timeout-ac", str(minutes)], check=True)
            subprocess.run(["powercfg", "/change", "disk-timeout-dc", str(minutes)], check=True)
            return True
        except Exception:
            return False

# ==================== Панели (страницы) ====================
class BasePanel(QWidget):
    """Базовый класс для панелей с возможностью закрытия"""
    closed = Signal()

    def __init__(self, title, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        # Верхняя панель с заголовком и кнопкой закрытия
        top_bar = QHBoxLayout()
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        close_btn = QPushButton("×")
        close_btn.setFixedSize(30, 30)
        close_btn.clicked.connect(self.close_panel)

        top_bar.addWidget(title_label)
        top_bar.addStretch()
        top_bar.addWidget(close_btn)

        layout.addLayout(top_bar)
        self.content_layout = QVBoxLayout()
        layout.addLayout(self.content_layout)
        layout.addStretch()

    def close_panel(self):
        self.closed.emit()

    def add_widget(self, widget):
        self.content_layout.addWidget(widget)


class MainPanel(BasePanel):
    """Главное меню: отображение и управление схемами"""
    def __init__(self):
        super().__init__("Главное меню")
        self.setup_ui()

    def setup_ui(self):
        # Выпадающий список схем
        self.scheme_combo = QComboBox()
        self.schemes = PowerManager.get_power_schemes()
        active = PowerManager.get_active_scheme()
        for guid, name in self.schemes:
            self.scheme_combo.addItem(name, guid)
            if guid == active:
                self.scheme_combo.setCurrentIndex(self.scheme_combo.count() - 1)

        self.apply_btn = QPushButton("Применить схему")
        self.apply_btn.clicked.connect(self.apply_scheme)

        # Настройка таймаутов
        self.monitor_spin = QLineEdit()
        self.monitor_spin.setPlaceholderText("Таймаут монитора (мин)")
        self.disk_spin = QLineEdit()
        self.disk_spin.setPlaceholderText("Таймаут диска (мин)")
        self.set_timeouts_btn = QPushButton("Установить таймауты")
        self.set_timeouts_btn.clicked.connect(self.set_timeouts)

        self.add_widget(QLabel("Выберите схему электропитания:"))
        self.add_widget(self.scheme_combo)
        self.add_widget(self.apply_btn)
        self.add_widget(QLabel("Дополнительные настройки:"))
        self.add_widget(self.monitor_spin)
        self.add_widget(self.disk_spin)
        self.add_widget(self.set_timeouts_btn)

    def apply_scheme(self):
        idx = self.scheme_combo.currentIndex()
        guid = self.schemes[idx][0]
        if PowerManager.set_active_scheme(guid):
            QMessageBox.information(self, "Успех", "Схема электропитания применена.")
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось применить схему.")

    def set_timeouts(self):
        try:
            mon = int(self.monitor_spin.text())
            PowerManager.set_monitor_timeout(mon)
        except ValueError:
            pass
        try:
            disk = int(self.disk_spin.text())
            PowerManager.set_disk_timeout(disk)
        except ValueError:
            pass
        QMessageBox.information(self, "Успех", "Таймауты установлены.")


class AdvancedPanel(BasePanel):
    """Дополнительные настройки (оптимизация системы)"""
    def __init__(self):
        super().__init__("Дополнительные настройки")
        self.setup_ui()

    def setup_ui(self):
        # Пример: очистка временных файлов
        self.clean_btn = QPushButton("Очистить временные файлы")
        self.clean_btn.clicked.connect(self.clean_temp)
        self.add_widget(self.clean_btn)

    def clean_temp(self):
        # Здесь можно добавить логику очистки
        QMessageBox.information(self, "Очистка", "Временные файлы очищены (заглушка).")


class SettingsPanel(BasePanel):
    """Настройки приложения"""
    def __init__(self):
        super().__init__("Настройки")
        self.setup_ui()

    def setup_ui(self):
        # Например, настройка автозапуска
        self.autostart_check = QPushButton("Добавить в автозагрузку (заглушка)")
        self.autostart_check.clicked.connect(lambda: QMessageBox.information(self, "Автозагрузка", "Функция в разработке"))
        self.add_widget(self.autostart_check)


class AboutPanel(BasePanel):
    """О программе"""
    def __init__(self):
        super().__init__("О программе")
        self.setup_ui()

    def setup_ui(self):
        info = QLabel(
            "Оптимизатор системы v1.0\n"
            "Разработан на Python + PySide6\n"
            "Управление схемами электропитания Windows"
        )
        info.setAlignment(Qt.AlignCenter)
        self.add_widget(info)


# ==================== Поиск функций ====================
class SearchDialog(QWidget):
    """Всплывающее окно поиска (можно заменить на выпадающий список)"""
    function_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Popup)
        self.setStyleSheet("background-color: #2C2F33; border: 1px solid #7289DA;")
        layout = QVBoxLayout(self)
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Введите название функции...")
        self.search_edit.textChanged.connect(self.filter_functions)
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        layout.addWidget(self.search_edit)
        layout.addWidget(self.list_widget)
        self.all_functions = [
            ("Сменить схему электропитания", "main"),
            ("Очистить временные файлы", "advanced"),
            ("Настройки таймаутов", "main"),
            ("Добавить в автозагрузку", "settings"),
        ]
        self.update_list()

    def update_list(self):
        self.list_widget.clear()
        for name, page in self.all_functions:
            self.list_widget.addItem(name)

    def filter_functions(self, text):
        self.list_widget.clear()
        for name, page in self.all_functions:
            if text.lower() in name.lower():
                self.list_widget.addItem(name)

    def on_item_clicked(self, item):
        # Находим страницу по имени функции
        for name, page in self.all_functions:
            if item.text() == name:
                self.function_selected.emit(page)
                self.close()
                break

    def show_search(self):
        self.search_edit.clear()
        self.update_list()
        self.show()
        self.search_edit.setFocus()


# ==================== Главное окно ====================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Оптимизатор системы")
        self.setMinimumSize(1000, 600)
        self.setStyleSheet(self.get_dark_stylesheet())

        # Центральный виджет
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        # Боковая панель (меню)
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(250)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setAlignment(Qt.AlignTop)

        # Кнопки меню
        self.btn_main = QPushButton("Главное меню")
        self.btn_advanced = QPushButton("Дополнительные настройки")
        self.btn_settings = QPushButton("Настройки")
        self.btn_about = QPushButton("О программе")

        for btn in [self.btn_main, self.btn_advanced, self.btn_settings, self.btn_about]:
            btn.setFixedHeight(40)
            btn.clicked.connect(self.on_menu_clicked)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        # Основная область (стек панелей)
        self.stack = QStackedWidget()
        # Создаём панели
        self.panel_main = MainPanel()
        self.panel_advanced = AdvancedPanel()
        self.panel_settings = SettingsPanel()
        self.panel_about = AboutPanel()

        # Подключаем сигналы закрытия панелей
        for panel in [self.panel_main, self.panel_advanced, self.panel_settings, self.panel_about]:
            panel.closed.connect(lambda: self.stack.setCurrentWidget(self.empty_widget))

        self.stack.addWidget(self.panel_main)
        self.stack.addWidget(self.panel_advanced)
        self.stack.addWidget(self.panel_settings)
        self.stack.addWidget(self.panel_about)

        # Пустой виджет (когда все панели закрыты)
        self.empty_widget = QWidget()
        empty_layout = QVBoxLayout(self.empty_widget)
        empty_layout.addWidget(QLabel("Закройте панель или выберите пункт меню"))
        self.stack.addWidget(self.empty_widget)
        self.stack.setCurrentWidget(self.empty_widget)

        # Поиск в верхней части
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Поиск функций...")
        self.search_bar.setFixedHeight(30)
        self.search_bar.setFixedWidth(300)
        self.search_bar.returnPressed.connect(self.show_search_popup)

        # Размещаем верхнюю панель с поиском
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        top_layout.addStretch()
        top_layout.addWidget(self.search_bar)
        top_layout.addStretch()

        # Компоновка: слева боковая панель, справа стек, сверху поиск
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.addWidget(top_widget)
        right_layout.addWidget(self.stack)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(right_widget, 1)

        # Поисковый диалог
        self.search_dialog = SearchDialog(self)
        self.search_dialog.function_selected.connect(self.activate_function)

    def get_dark_stylesheet(self):
        return """
            QMainWindow {
                background-color: #1E1F22;
            }
            QWidget {
                background-color: #2B2D31;
                color: #E0E0E0;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
            }
            QPushButton {
                background-color: #404249;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #5865F2, stop:1 #4752C4);
                color: white;
            }
            QPushButton:pressed {
                background-color: #3C45A5;
            }
            QLineEdit, QComboBox {
                background-color: #1E1F22;
                border: 1px solid #404249;
                border-radius: 4px;
                padding: 6px;
                selection-background-color: #5865F2;
            }
            QListWidget {
                background-color: #1E1F22;
                border: 1px solid #404249;
                outline: none;
            }
            QListWidget::item:selected {
                background-color: #5865F2;
            }
            QLabel {
                color: #E0E0E0;
            }
        """

    def on_menu_clicked(self):
        """Обработка нажатий на кнопки боковой панели"""
        sender = self.sender()
        if sender == self.btn_main:
            self.stack.setCurrentWidget(self.panel_main)
        elif sender == self.btn_advanced:
            self.stack.setCurrentWidget(self.panel_advanced)
        elif sender == self.btn_settings:
            self.stack.setCurrentWidget(self.panel_settings)
        elif sender == self.btn_about:
            self.stack.setCurrentWidget(self.panel_about)

    def show_search_popup(self):
        """Показывает всплывающее окно поиска под строкой ввода"""
        pos = self.search_bar.mapToGlobal(self.search_bar.rect().bottomLeft())
        self.search_dialog.move(pos)
        self.search_dialog.show_search()

    def activate_function(self, page_name):
        """Переход к странице по имени функции"""
        if page_name == "main":
            self.stack.setCurrentWidget(self.panel_main)
        elif page_name == "advanced":
            self.stack.setCurrentWidget(self.panel_advanced)
        elif page_name == "settings":
            self.stack.setCurrentWidget(self.panel_settings)
        elif page_name == "about":
            self.stack.setCurrentWidget(self.panel_about)


# ==================== Запуск приложения ====================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())