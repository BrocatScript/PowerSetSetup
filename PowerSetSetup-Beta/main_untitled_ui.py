# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_untitled.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QLabel, QLineEdit, QMainWindow, QProgressBar,
    QPushButton, QSizePolicy, QStackedWidget, QVBoxLayout,
    QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1100, 700)
        MainWindow.setMinimumSize(QSize(650, 550))
        icon = QIcon()
        icon.addFile(u":/Icons_svg/data/icons/PowerSetSetup.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"QMainWindow {\n"
"    background-color: rgb(14, 22, 33);\n"
"    font-family: \"Segoe UI\", \"Arial\", sans-serif;\n"
"}")
        MainWindow.setIconSize(QSize(24, 24))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 262, 701))
        self.Layout_menu_bar = QVBoxLayout(self.verticalLayoutWidget)
        self.Layout_menu_bar.setObjectName(u"Layout_menu_bar")
        self.Layout_menu_bar.setContentsMargins(0, 0, 0, 0)
        self.frame_menu_bar = QFrame(self.verticalLayoutWidget)
        self.frame_menu_bar.setObjectName(u"frame_menu_bar")
        self.frame_menu_bar.setMinimumSize(QSize(260, 600))
        self.frame_menu_bar.setStyleSheet(u"QFrame {\n"
"    background-color: #17212b;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: #1b2d3f;\n"
"    color: #ffffff;\n"
"    border-width: 2px;\n"
"    border-style: solid;\n"
"    border-color: #11212f;\n"
"    border-radius: 16px;\n"
"    padding: 8px;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"    text-align: left;\n"
"    padding-left: 65px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #233950;\n"
"    border-color: #11212f;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    color: #ffffff;\n"
"    background-color: #172937 !important;\n"
"    border-color: #11212f;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    background-color: #1b2d3f;\n"
"    color: #ffffff;\n"
"    border: 2px solid #162a3c;\n"
"    border-radius: 10px;\n"
"    padding: 4px 24px;\n"
"    font-size: 16px;\n"
"    selection-background-color: #5288c1; \n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: #203f5a;\n"
"}\n"
"\n"
"QLineEdit::placeholder {\n"
"    color: #6e7d8d;\n"
"}")
        self.frame_menu_bar.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_menu_bar.setFrameShadow(QFrame.Shadow.Raised)
        self.layoutWidget = QWidget(self.frame_menu_bar)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 80, 221, 191))
        self.Layout_menu_bar_button = QVBoxLayout(self.layoutWidget)
        self.Layout_menu_bar_button.setObjectName(u"Layout_menu_bar_button")
        self.Layout_menu_bar_button.setContentsMargins(0, 0, 0, 0)
        self.pushButton_main = QPushButton(self.layoutWidget)
        self.pushButton_main.setObjectName(u"pushButton_main")
        self.pushButton_main.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u":/Icons_svg/data/icons/main.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_main.setIcon(icon1)
        self.pushButton_main.setIconSize(QSize(24, 24))

        self.Layout_menu_bar_button.addWidget(self.pushButton_main)

        self.pushButton_aboit = QPushButton(self.layoutWidget)
        self.pushButton_aboit.setObjectName(u"pushButton_aboit")
        self.pushButton_aboit.setMinimumSize(QSize(169, 39))
        self.pushButton_aboit.setAutoFillBackground(False)
        self.pushButton_aboit.setStyleSheet(u"")
        icon2 = QIcon()
        icon2.addFile(u":/Icons_svg/data/icons/about.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_aboit.setIcon(icon2)
        self.pushButton_aboit.setIconSize(QSize(24, 24))
        self.pushButton_aboit.setFlat(False)

        self.Layout_menu_bar_button.addWidget(self.pushButton_aboit)

        self.pushButton_settings = QPushButton(self.layoutWidget)
        self.pushButton_settings.setObjectName(u"pushButton_settings")
        self.pushButton_settings.setStyleSheet(u"")
        icon3 = QIcon()
        icon3.addFile(u":/Icons_svg/data/icons/settings.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_settings.setIcon(icon3)
        self.pushButton_settings.setIconSize(QSize(24, 24))

        self.Layout_menu_bar_button.addWidget(self.pushButton_settings)

        self.verticalLayoutWidget_2 = QWidget(self.frame_menu_bar)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 0, 241, 51))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.lineEdit = QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setStyleSheet(u"")

        self.verticalLayout.addWidget(self.lineEdit)


        self.Layout_menu_bar.addWidget(self.frame_menu_bar)

        self.verticalLayoutWidget_3 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(260, 0, 841, 701))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.verticalLayoutWidget_3)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"QComboBox {\n"
"    background-color: #1b2d3f;\n"
"    color: #ffffff;\n"
"    border: 2px solid #ffffff;\n"
"    border-radius: 8px;\n"
"    padding: 2px 12px;\n"
"    font-size: 12px;\n"
"    selection-background-color: #5288c1; \n"
"}\n"
"/*#162a3c*/\n"
"\n"
"QComboBox:focus {\n"
"    border-color: #2b4764;\n"
"}\n"
"\n"
"QComboBox::placeholder {\n"
"    color: #6e7d8d;\n"
"}\n"
"\n"
"QComboBox {\n"
"    background-color: #1b2d3f;\n"
"    color: #ffffff;\n"
"    border: 2px solid #162a3c;\n"
"    border-radius: 10px;\n"
"    padding: 4px 14px;\n"
"    font-size: 16px;\n"
"    selection-background-color: #5288c1;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    background: none;      /* \u0443\u0431\u0438\u0440\u0430\u0435\u043c \u0444\u043e\u043d \u043a\u043e\u043d\u0442\u0435\u0439\u043d\u0435\u0440\u0430 */\n"
"    border: none;          /* \u0443\u0431\u0438\u0440\u0430\u0435\u043c \u0440\u0430\u043c\u043a\u0443 \u043a\u043e\u043d\u0442\u0435\u0439\u043d\u0435\u0440\u0430 */\n"
"    subcontrol-position: rig"
                        "ht center;\n"
"    subcontrol-origin: padding;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(:/Icons_svg/data/icons/arrow_down.svg);\n"
"    width: 24px;\n"
"    height: 24px;\n"
"    subcontrol-position: right center;\n"
"    subcontrol-origin: padding;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item {\n"
"    min-height: 20px;   /* \u041c\u0438\u043d\u0438\u043c\u0430\u043b\u044c\u043d\u0430\u044f \u0432\u044b\u0441\u043e\u0442\u0430 \u043f\u0443\u043d\u043a\u0442\u0430. \u042d\u043a\u0441\u043f\u0435\u0440\u0438\u043c\u0435\u043d\u0442\u0438\u0440\u0443\u0439\u0442\u0435 \u0441 \u044d\u0442\u0438\u043c \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435\u043c (\u043d\u0430\u043f\u0440\u0438\u043c\u0435\u0440, 20, 24, 28) */\n"
"    padding: 2px 8px;   /* \u0412\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u0438\u0435 \u043e\u0442\u0441\u0442\u0443\u043f\u044b \u0434\u043b\u044f \u0442\u0435\u043a\u0441\u0442\u0430, \u0447\u0442\u043e\u0431\u044b \u043e\u043d \u043d\u0435 \u043f\u0440\u0438\u043b\u0438"
                        "\u043f\u0430\u043b \u043a \u043a\u0440\u0430\u044f\u043c */\n"
"}")
        self.page_main = QWidget()
        self.page_main.setObjectName(u"page_main")
        self.verticalLayoutWidget_5 = QWidget(self.page_main)
        self.verticalLayoutWidget_5.setObjectName(u"verticalLayoutWidget_5")
        self.verticalLayoutWidget_5.setGeometry(QRect(0, 0, 841, 41))
        self.verticalLayout_4 = QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.verticalLayoutWidget_5)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"background-color:  #1b2d3f")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(380, 0, 87, 41))
        self.label_2.setStyleSheet(u"QLabel{\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"    color: #ffffff;\n"
"    font-weight: bold;\n"
"    font-size: 16px;\n"
"}")

        self.verticalLayout_4.addWidget(self.frame)

        self.frame_4 = QFrame(self.page_main)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setGeometry(QRect(90, 150, 201, 121))
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.stackedWidget.addWidget(self.page_main)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2.setStyleSheet(u"")
        self.progressBar = QProgressBar(self.page_2)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(200, 340, 341, 20))
        self.progressBar.setValue(24)
        self.lineEdit_2 = QLineEdit(self.page_2)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(280, 170, 181, 71))
        self.lineEdit_2.setStyleSheet(u"font: 30pt \"Segoe UI\";")
        self.label = QLabel(self.page_2)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(280, 50, 211, 89))
        self.label.setStyleSheet(u"font: 50pt \"Segoe UI\";")
        self.verticalLayoutWidget_6 = QWidget(self.page_2)
        self.verticalLayoutWidget_6.setObjectName(u"verticalLayoutWidget_6")
        self.verticalLayoutWidget_6.setGeometry(QRect(0, 0, 841, 41))
        self.verticalLayout_5 = QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.verticalLayoutWidget_6)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setStyleSheet(u"background-color:  #1b2d3f")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.label_6 = QLabel(self.frame_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(380, 0, 87, 41))
        self.label_6.setStyleSheet(u"QLabel{\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"    color: #ffffff;\n"
"    font-weight: bold;\n"
"    font-size: 16px;\n"
"}")

        self.verticalLayout_5.addWidget(self.frame_2)

        self.stackedWidget.addWidget(self.page_2)
        self.page_settings = QWidget()
        self.page_settings.setObjectName(u"page_settings")
        self.verticalLayoutWidget_4 = QWidget(self.page_settings)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(510, 70, 331, 41))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.comboBox = QComboBox(self.verticalLayoutWidget_4)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.verticalLayout_3.addWidget(self.comboBox)

        self.verticalLayoutWidget_7 = QWidget(self.page_settings)
        self.verticalLayoutWidget_7.setObjectName(u"verticalLayoutWidget_7")
        self.verticalLayoutWidget_7.setGeometry(QRect(0, 0, 841, 41))
        self.verticalLayout_6 = QVBoxLayout(self.verticalLayoutWidget_7)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.verticalLayoutWidget_7)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setStyleSheet(u"background-color:  #1b2d3f")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.label_4 = QLabel(self.frame_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(380, 0, 87, 41))
        self.label_4.setStyleSheet(u"QLabel{\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"    color: #ffffff;\n"
"    font-weight: bold;\n"
"    font-size: 16px;\n"
"}")

        self.verticalLayout_6.addWidget(self.frame_3)

        self.verticalLayoutWidget_8 = QWidget(self.page_settings)
        self.verticalLayoutWidget_8.setObjectName(u"verticalLayoutWidget_8")
        self.verticalLayoutWidget_8.setGeometry(QRect(30, 260, 121, 251))
        self.verticalLayout_7 = QVBoxLayout(self.verticalLayoutWidget_8)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.checkBox_2 = QCheckBox(self.verticalLayoutWidget_8)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.verticalLayout_7.addWidget(self.checkBox_2)

        self.checkBox_3 = QCheckBox(self.verticalLayoutWidget_8)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.verticalLayout_7.addWidget(self.checkBox_3)

        self.checkBox_4 = QCheckBox(self.verticalLayoutWidget_8)
        self.checkBox_4.setObjectName(u"checkBox_4")

        self.verticalLayout_7.addWidget(self.checkBox_4)

        self.checkBox = QCheckBox(self.verticalLayoutWidget_8)
        self.checkBox.setObjectName(u"checkBox")

        self.verticalLayout_7.addWidget(self.checkBox)

        self.checkBox_5 = QCheckBox(self.verticalLayoutWidget_8)
        self.checkBox_5.setObjectName(u"checkBox_5")

        self.verticalLayout_7.addWidget(self.checkBox_5)

        self.stackedWidget.addWidget(self.page_settings)

        self.verticalLayout_2.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"PowerSetSetup", None))
        self.pushButton_main.setText(QCoreApplication.translate("MainWindow", u"Main", None))
        self.pushButton_aboit.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.pushButton_settings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
#if QT_CONFIG(tooltip)
        self.lineEdit.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit.setText("")
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0438\u0441\u043a", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Main Menu", None))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u043e\u0434", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Label", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"System", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Dark", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Light", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"Galaxy", None))

        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"Test", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"Test2", None))
        self.checkBox_4.setText(QCoreApplication.translate("MainWindow", u"Test3", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"Test4", None))
        self.checkBox_5.setText(QCoreApplication.translate("MainWindow", u"Test5", None))
    # retranslateUi

