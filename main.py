import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from widgets.body import  Body
from qt_material import apply_stylesheet
from qt_material import list_themes


def window():
   app = QApplication(sys.argv)
   main_body = Body()
   main_body.setWindowTitle("四六级监考老师排班")
   apply_stylesheet(app, theme='dark_teal.xml')
   main_body.show()
   sys.exit(app.exec_())


if __name__ == '__main__':
   list_themes()
   window()
