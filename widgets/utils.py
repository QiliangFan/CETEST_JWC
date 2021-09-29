import pandas as pd
from PyQt5.QtWidgets import QFileDialog, QWidget, QPushButton
from typing import Union, List


def __read_file(parent, sheet_name: Union[int, List] = 0) -> Union[pd.DataFrame, dict]:
    file_selector = QFileDialog(parent, filter="Table (*.csv)")
    file_path = file_selector.getOpenFileName()[0]
    csv = pd.read_excel(file_path, sheet_name)
    if isinstance(csv, pd.DataFrame):
        csv = csv.applymap(lambda x: str(x).strip() if isinstance(x, str) else x, na_action="ignore")
    elif isinstance(csv, dict):
        for key in csv:
            csv[key] = csv[key].applymap(lambda x: str(x).strip() if isinstance(x, str) else x, na_action="ignore")
    else:
        raise ValueError()
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
def signed_teachers(parent, widget: QPushButton):
    dt = __read_file(parent)
    parent.update_sign(dt)

@add_right
def main_monitors(parent, widget: QPushButton):
    dt = __read_file(parent)
    parent.update_mm(dt)

@add_right
def candidates(parent, widget: QPushButton):
    dt = __read_file(parent)
    parent.update_candidate(dt)

@add_right
def exam_room(parent, widget: QPushButton):
    dt: dict = __read_file(
        parent,
        sheet_name=["津南四级", "津南六级", "八里台四级", "八里台六级"]
    )
    parent.update_exam_room(
        dt["津南四级"],
        dt["津南六级"],
        dt["八里台四级"],
        dt["八里台六级"]
    )



