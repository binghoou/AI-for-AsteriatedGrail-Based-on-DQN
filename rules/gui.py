# -*- coding:UTF-8 -*-
from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtGui import QFontDatabase, QFont
import sys
import qtawesome
# import test_rc

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        widget = QtWidgets.QWidget(self)
        lay = QtWidgets.QVBoxLayout(widget)
        self.label = QtWidgets.QLabel('测试中ABCO0123LMNijkIJK'*2)
        lay.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit('测试中ABCO0123LMNijkIJK'*2)
        lay.addWidget(self.lineEdit)
        self.setWindowTitle('测试中ABCO0123LMNijkIJK')

        self.setWindowIcon(qtawesome.icon('fa.rocket'))
        self.setCentralWidget(widget)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    # fontDb = QFontDatabase()
    # # fontID = fontDb.addApplicationFont("msyh.ttf")  # 此处的路径为qrc文件中的字体路径
    # # fontID = fontDb.addApplicationFont(":resources/siyuanheiti.ttf")  # 此处的路径为qrc文件中的字体路径
    # fontFamilies = fontDb.applicationFontFamilies(fontID)
    # print(fontFamilies)  # ['Source Han Sans CN Bold']

    # f = QFont('Source Han Sans CN Bold', 11, QtGui.QFont.Normal, False)
    # print(f.family())
    # app.setFont(f)
    # # app.setStyleSheet('font: 14pt "Source Han Sans CN Bold";')

    mw = MyWindow()
    mw.setWindowTitle(mw.tr('测试不行吗'))
    mw.show()
    sys.exit(app.exec_())
