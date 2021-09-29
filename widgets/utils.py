import pandas as pd
from PyQt5.QtWidgets import QFileDialog, QWidget, QPushButton

from widgets.body import Body


def __read_file(parent) -> pd.DataFrame:
    file_selector = QFileDialog(parent, filter="Table (*.csv)")
    file_path = file_selector.getOpenFileName()[0]
    csv = pd.read_csv(file_path)
    return csv

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
def signed_teachers(parent: Body, widget: QPushButton):
    dt = __read_file(parent)
    parent.update_sign(dt)

@add_right
def main_monitors(parent: Body, widget: QPushButton):
    dt = __read_file(parent)
    parent.update_mm(dt)

@add_right
def candidates(parent: Body, widget: QPushButton):
    dt = __read_file(parent)
    parent.update_candidate(dt)

@add_right
def jin_nan(parent: Body, widget: QPushButton):
    dt = __read_file(parent)
    parent.update_jinnan(dt)

@add_right
def balitai(parent: Body, widget: QPushButton):
    dt = __read_file(parent)
    parent.update_balitai(dt)

