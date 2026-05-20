import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from ui_main_untitled import Ui_MainWindow
import resources_rc

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_main.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pushButton_aboit.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.pushButton_settings.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())