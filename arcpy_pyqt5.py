# coding=utf-8
import arcpy_crete_xml
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
class picture(QWidget):
    def __init__(self):
        super(picture, self).__init__()

        self.resize(600, 400)
        self.setWindowTitle("label显示图片")



        self.label = QLabel(self)

        self.label.setStyleSheet("QLabel{background:white;}"
                                 "QLabel{color:rgb(300,300,300,120);font-size:10px;font-weight:bold;font-family:宋体;}"
                                 )
     #选择图像
        select_img = QPushButton(self)
        select_img.setText("选择图像")
        select_img.move(10, 30)
        select_img.clicked.connect(self.SelectImage)
     #生成xml的名字
        open_xml = QPushButton(self)
        open_xml.setText("输入生成xml的路径与名字")
        open_xml.move(10, 90)
        open_xml.clicked.connect(self.OpenXml)
    #执行按钮
        create_xml = QPushButton(self)
        create_xml.setText("点击生成xml")
        create_xml.move(10, 150)
        create_xml.resize(80,40)
        create_xml.clicked.connect(self. ImplementXml)
    def SelectImage(self):
        global imgName
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图像", "", "All Files(*)")
        self.label.setText(imgName)
        self.label.move(120,40)
        self.label.adjustSize()
    def OpenXml(self):
         global fileName2
         fileName2 = QFileDialog.getSaveFileName(self,
                                                      "文件保存",
                                                      "C:/",
                                                      " *.xml")
    def ImplementXml(self):
        arcpy_crete_xml.Createxml(imgName,fileName2[0])
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    my = picture()
    my.show()
    sys.exit(app.exec_())