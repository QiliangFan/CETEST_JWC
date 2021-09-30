import pandas as pd
from PyQt5.QtWidgets import QFileDialog, QWidget, QPushButton
from typing import Union, List, cast

map_k = {
    "jinnan4": "津南四级",
    "jinnan6": "津南六级",
    "balitai4": "八里台四级",
    "balitai6": "八里台六级"
}

def __read_file(parent, sheet_name: Union[int, List] = 0) -> Union[pd.DataFrame, dict, None]:
    file_selector = QFileDialog(parent, filter="Table (*.csv, *.xlsx, *.xls)")
    file_path = file_selector.getOpenFileName()[0]
    if len(file_path.strip()) == 0:
        return None
    if file_path.endswith(".xlsx") or file_path.endswith(".xls"):
        csv = pd.read_excel(file_path, sheet_name)
    else:
        csv = pd.read_csv(file_path)
    if isinstance(csv, pd.DataFrame):
        csv = csv.applymap(lambda x: str(x).strip() if isinstance(x, str) else str(x), na_action="ignore")
    elif isinstance(csv, dict):
        for key in csv:
            csv[key] = csv[key].applymap(lambda x: str(x).strip() if isinstance(x, str) else str(x).strip(), na_action="ignore")
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
    if dt is not None:
        parent.update_sign(dt)

@add_right
def main_monitors(parent, widget: QPushButton):
    dt = __read_file(parent)
    if dt is not None:
        parent.update_mm(dt)

@add_right
def candidates(parent, widget: QPushButton):
    dt = __read_file(parent)
    if dt is not None:
        parent.update_candidate(dt)

@add_right
def exam_room(parent, widget: QPushButton):
    dt: dict = __read_file(
        parent,
        sheet_name=["津南四级", "津南六级", "八里台四级", "八里台六级"]
    )
    if dt is not None:
        parent.update_exam_room(
            dt["津南四级"],
            dt["津南六级"],
            dt["八里台四级"],
            dt["八里台六级"]
        )

def submit(parent):
    from .body import Body
    parent = cast(Body, parent)
    result = {}
    if parent.jin_nan4_dt is not None:
        try:
            result["jinnan4"] = parent.get_status(campus="津南校区", exam_type="4")
        except:
            import traceback
            traceback.print_exc()
    if parent.jin_nan6_dt is not None:
        try:
            result["jinnan6"] = parent.get_status(campus="津南校区", exam_type="6")
        except:
            import traceback
            traceback.print_exc()

    if parent.balitai4_dt is not None:
        try:
            result["balitai4"] = parent.get_status(campus="八里台校区", exam_type="4")
        except:
            import traceback
            traceback.print_exc()


    if parent.balitai6_dt is not None:
        try:
            result["balitai6"] = parent.get_status(campus="八里台校区", exam_type="6")
        except:
            import traceback
            traceback.print_exc()

    execel_writer = pd.ExcelWriter("考场分配.xlsx")
    total = pd.DataFrame()
    for k in result:
        if result[k] is not None:
            dt = result[k]
            total = total.append(dt, ignore_index=True)
            dt.to_excel(execel_writer, sheet_name=map_k[k], index=False)
    total.to_excel(execel_writer, sheet_name="全部", index=False)
    execel_writer.close()
    print("debug")