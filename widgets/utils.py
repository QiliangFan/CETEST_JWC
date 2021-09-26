import pandas as pd
from PyQt5.QtWidgets import QFileDialog, QWidget, QPushButton


def __read_file(parent):
    file_selector = QFileDialog(parent, filter="Table (*.csv)")
    file_path = file_selector.getOpenFileName()[0]
    return file_path

def add_right(func):
    def wrapper(p, w: QPushButton):
        try:
            func(p, w)
            w.setText(f"{w.text().replace(' √', '')} √")
            p.update()
        except:
            import traceback
            traceback.print_exc()
    return wrapper


@add_right
def signed_teachers(parent, widget: QPushButton):
    csv_file = __read_file(parent)


@add_right
def main_monitors(parent, widget: QWidget):
    csv_file = __read_file(parent)


@add_right
def candidates(parent, widget: QWidget):
    csv_file = __read_file(parent)

@add_right
def jin_nan(parent, widget: QWidget):
    csv_file = __read_file(parent)

@add_right
def balitai_nan(parent, widget: QWidget):
    csv_file = __read_file(parent)

