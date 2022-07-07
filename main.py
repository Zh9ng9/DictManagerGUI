import os
import sys
import time

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QWidget, QDialog, QLabel
from MainWindow import Ui_MainWindow
import subprocess
import sys

class Quchong:
    def __init__(self, rootpath, filename):
        text = ""
        # txt去重
        text += "[+]对文件" + str(filename) + "进行去重" + "\n"
        fullpath = rootpath + filename
        old_hosts = []
        with open(fullpath, "r", encoding="utf-8") as f:
            for line in f.readlines():
                old_hosts.append(line)
        old_count = len(old_hosts)
        text += "去重前的数据量：" + str(old_count) + "; "
        new_hosts = []
        for line in old_hosts:
            if line not in new_hosts:
                new_hosts.append(line)
        new_count = len(new_hosts)
        text += "去重后的数据量：" + str(new_count) + ";\n"
        with open(fullpath, "w", encoding="utf-8") as f:
            for line in new_hosts:
                f.write(line)
        # text += "对文件" + str(filename) + "去重完毕" + "\n"
        # 弹窗功能 待实现
        # Dialog(text)



class Dialog(QDialog):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Dialog')
        self.resize(300, 200)  # set dialog size to 400*300
        self.lb = QLabel(self.text, self)  # add a label to this dialog
        self.lb.setGeometry(QtCore.QRect(70, 40, 201, 51))  # set label position and size
        self.show()


class MainCode(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        with open('./ADD.txt', "r") as f:
            str = f.read()
        self.text = str
        self.textEdit_1.setText(self.text)
        self.pushButton_3.setDisabled(True)

        listdir = os.listdir("./")
        listdir_txt = []
        for i in listdir:
            if i == "ADD.txt":
                continue
            if i.endswith("txt"):
                listdir_txt.append(i)

        for i in listdir_txt:
            item = QListWidgetItem()  # 创建QListWidgetItem对象
            item.setSizeHint(QSize(300, 30))  # 设置QListWidgetItem大小
            item.setText(i)
            self.listWidget_2.addItem(item)  # 添加item

        # 点击事件
        self.listWidget_2.itemClicked.connect(self.clickedList2)
        self.listWidget_3.itemClicked.connect(self.clickedList3)
        # 按钮的槽函数
        self.pushButton_1.clicked.connect(self.pushButton_1_clicked_func)
        self.pushButton_2.clicked.connect(self.pushButton_2_clicked_func)
        self.pushButton_3.clicked.connect(self.pushButton_3_clicked_func)
        # 右键菜单
        self.listWidget_2.customContextMenuRequested.connect(self.custom_right_menu_2)
        self.listWidget_3.customContextMenuRequested.connect(self.custom_right_menu_3)

    def custom_right_menu_2(self):
        # 第二栏删除
        item = self.listWidget_2.currentItem()
        # print(self.listWidget_2.row(item))
        self.listWidget_2.takeItem(self.listWidget_2.row(item))
        # 第三栏增加
        self.listWidget_3.addItem(item)
        self.listWidget_3.sortItems()

    def custom_right_menu_3(self):
        # 第三栏删除
        item = self.listWidget_3.currentItem()
        # print(self.listWidget_3.row(item))
        self.listWidget_3.takeItem(self.listWidget_3.row(item))
        # 第二栏增加
        self.listWidget_2.addItem(item)
        self.listWidget_3.sortItems()

    def clickedList2(self):
        sh = "notepad ./" + self.listWidget_2.currentItem().text()
        res = subprocess.run(sh, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

    def clickedList3(self):
        sh = "notepad ./" + self.listWidget_3.currentItem().text()
        res = subprocess.run(sh, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

    def pushButton_1_clicked_func(self):
        # 清空输入框
        self.text = ""
        self.textEdit_1.setText(self.text)

    def pushButton_2_clicked_func(self):
        # textEdit_1的内容写入self.text
        self.text = self.textEdit_1.toPlainText()
        # 写入ADD.txt
        with open("./ADD.txt", "w") as f:
            f.write(self.text)
        # 启用第三个按钮
        self.pushButton_3.setEnabled(True)

    def pushButton_3_clicked_func(self):
        # 获取第三栏所有
        count = self.listWidget_3.count()
        listdir_input = []
        for i in range(count):
            listdir_input.append(self.listWidget_3.item(i).text())
        for i in listdir_input:
            with open(i, "a+") as f:
                f.write(self.text)
                f.write("\n")
        for i in listdir_input:
            Quchong("./", i)
        # 禁用第三个按钮
        self.pushButton_3.setDisabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainCode()
    main_window.show()
    sys.exit(app.exec_())
