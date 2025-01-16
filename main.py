"""@name:     WSSS_system
   @author:   tang jingfeng
   @date:     2025/01/10"""


#显示ui
import win
import sys
import time

from PyQt5 import QtCore
from PyQt5.Qt import *
from PyQt5.QtCore import Qt, QFile, QTextStream, QIODevice, QByteArray, QUrl
import csv
import re
from PyQt5.Qt import QFileDialog
from qt_material import apply_stylesheet
import os
from PyQt5 import QtCore, QtGui, QtWidgets

class QSSLoader:
    def __init__(self):
        pass

    @staticmethod
    def read_qss_file(qss_file_name):
        with open(qss_file_name, 'r',  encoding='UTF-8') as file:
            return file.read()


def select_a_single_file():
    # 弹出文件选择对话框，让用户选择一个文件
    file_path, _ = QFileDialog.getOpenFileName(None, "选择文件", "C:/", "All Files (*);;Text Files (*.txt)")

    if file_path:
        print("选择的文件路径：", file_path)
    else:
        print("未选择文件！")

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

def load_images(ui, folder_path):
    # 获取文件夹中的所有图片文件
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

    row = 0
    col = 0
    max_cols = 4  # 每行显示 3 张图片
    ui.scroll_layout = QGridLayout(ui.scrollAreaWidgetContents_4)

    for image_file in image_files:
        # 创建 QLabel 并设置图片
        # label_preview_dataset = QtWidgets.Qlabel()
        label_preview_dataset = QtWidgets.QLabel(ui.tab_2)
        pixmap = QPixmap(os.path.join(folder_path, image_file))
        label_preview_dataset.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))  # 设置图片大小

        # 将 QLabel 添加到布局中
        ui.scroll_layout.addWidget(label_preview_dataset, row, col)

        col += 1
        if col >= max_cols:
            col = 0
            row += 1

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = win.Ui_MainWindow()
    ui.setupUi(MainWindow)

    # qss
    style_file = './style.qss'
    style_sheet = QSSLoader.read_qss_file(style_file)
    MainWindow.setStyleSheet(style_sheet)

    # 槽函数
    ui.pushButton_seg_img_dir.clicked.connect(select_a_single_file)
    # 创建定时器
    timer = QTimer()
    timer.timeout.connect(lambda: update_time(ui.label_time))  # 连接定时器的 timeout 信号到 update_time 函数
    timer.start(1000)  # 每隔1秒更新一次时间

    load_images(ui, 'E:\datasets\pascalvoc\\atest')
    # load_images(ui, 'E:\datasets\pascalvoc\JPEGImages')
    # 加载图像
    pixmap = QPixmap('E:\datasets\stochastic_img/person_plane.jpg')
    pixmap_pre = QPixmap('E:\datasets\stochastic_img/person_plane_pre.png')

    # 将图像设置到QLabel控件中
    ui.label_oriimg.setPixmap(pixmap)
    # ui.label_oriimg.setScaledContents(True)
    ui.label_pred.setPixmap(pixmap_pre)
    # ui.label_pred.setScaledContents(True)


    MainWindow.show()
    sys.exit(app.exec_())