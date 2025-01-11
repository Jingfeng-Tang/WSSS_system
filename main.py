"""@name:     WSSS_system
   @author:   tang jingfeng
   @date:     2025/01/10"""


#显示ui
import main_win
import sys
import time

from PyQt5 import QtCore
from PyQt5.Qt import *
from PyQt5.QtCore import Qt, QFile, QTextStream, QIODevice, QByteArray, QUrl
import csv
import re
from PyQt5.Qt import QFileDialog
from qt_material import apply_stylesheet

class QSSLoader:
    def __init__(self):
        pass

    @staticmethod
    def read_qss_file(qss_file_name):
        with open(qss_file_name, 'r',  encoding='UTF-8') as file:
            return file.read()



def Select_a_single_directory():
    dir_path = QFileDialog.getExistingDirectory(None, "选择目录", "C:/", QFileDialog.ShowDirsOnly)
    if dir_path:
        print("选择的目录路径：", dir_path)
    else:
        print("未选择目录路径！")


def update_time(label):
    # 获取当前时间
    current_time = QDateTime.currentDateTime()
    # 格式化时间
    time_display = current_time.toString("yyyy-MM-dd hh:mm:ss dddd")
    # 更新 QLabel 的文本
    label.setText(time_display)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = main_win.Ui_MainWindow()
    ui.setupUi(MainWindow)

    # qss
    style_file = './style.qss'
    style_sheet = QSSLoader.read_qss_file(style_file)
    MainWindow.setStyleSheet(style_sheet)

    # 槽函数
    ui.pushButton_dataset_dir.clicked.connect(Select_a_single_directory)
    # 创建定时器
    timer = QTimer()
    timer.timeout.connect(lambda: update_time(ui.label_time))  # 连接定时器的 timeout 信号到 update_time 函数
    timer.start(1000)  # 每隔1秒更新一次时间


    MainWindow.show()
    sys.exit(app.exec_())


