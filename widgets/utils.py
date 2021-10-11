import pandas as pd
from PyQt5.QtWidgets import QFileDialog, QWidget, QPushButton, QDialog, QMessageBox
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
    names = dt["监考教师姓名"].tolist()
    if len(names) != len(set(names)):
        QMessageBox.critical(parent, "错误信息", "存在重名老师!")
        return
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

    if_error = False

    if parent.jin_nan4_dt is not None:
        try:
            result["jinnan4"] = parent.get_status(campus="津南校区", exam_type="4")
            QMessageBox.information(parent, "津南4级", "津南4级安排完成!")
        except:
            import traceback
            traceback.print_exc()
            result["jinnan4"] = None
            QMessageBox.critical(parent, "津南4级", "津南4级安排失败!")
    else:
        result["jinnan4"] = None

    if parent.jin_nan6_dt is not None:
        try:
            result["jinnan6"] = parent.get_status(campus="津南校区", exam_type="6")
            QMessageBox.information(parent, "津南6级", "津南6级安排完成!")
        except:
            import traceback
            traceback.print_exc()
            result["jinnan6"] = None
            QMessageBox.critical(parent, "津南6级", "津南6级安排失败!")
    else:
        result["jinnan6"] = None

    if parent.balitai4_dt is not None:
        try:
            result["balitai4"] = parent.get_status(campus="八里台校区", exam_type="4")
            QMessageBox.information(parent, "八里台4级", "八里台4级安排完成!")
        except:
            import traceback
            traceback.print_exc()
            result["balitai4"] = None
            QMessageBox.critical(parent, "八里台4级", "八里台4级安排失败!")
    else:
        result["balitai4"] = None

    if parent.balitai6_dt is not None:
        try:
            result["balitai6"] = parent.get_status(campus="八里台校区", exam_type="6")
            QMessageBox.information(parent, "八里台6级", "八里台6级安排完成!")
        except:
            import traceback
            traceback.print_exc()
            result["balitai6"] = None
            QMessageBox.critical(parent, "八里台6级", "八里台6级安排失败!")
    else:
        result["balitai6"] = None

    execel_writer = pd.ExcelWriter("考场分配.xlsx")
    total = pd.DataFrame()
    for k in result:
        if result[k] is not None:
            dt = result[k]
            total = total.append(dt, ignore_index=True)
            dt.to_excel(execel_writer, sheet_name=map_k[k], index=False)
        else:
            dt = pd.DataFrame()
            dt.to_excel(execel_writer, sheet_name=map_k[k], index=False)
    total.to_excel(execel_writer, sheet_name="全部", index=False)
    execel_writer.close()


    print("debug")


def generate_contact(parent):
    file_selector = QFileDialog(parent, filter="Table (*.csv, *.xlsx, *.xls)")
    file_path = file_selector.getOpenFileName()[0]
    combination = pd.DataFrame(columns=[
        "所在单位",
        "监考教师姓名",
        "性别",
        "工资号",
        "手机号码",
        "四级级别",
        "四级发卷点",
        "四级监考",
        "六级级别",
        "六级发卷点",
        "六级监考"
    ])
    for _type in ["津南四级", "津南六级", "八里台四级", "八里台六级"]:
        try:
            dt: pd.DataFrame = pd.read_excel(file_path, sheet_name=_type)
            for idx, line in dt.iterrows():
                name = line["监考教师姓名"]
                name1 = line["监考教师姓名1"]
                if len(combination[combination["监考教师姓名"] == name]) > 0:
                    concat_dt = combination[combination["监考教师姓名"] == name]
                    combination = combination.drop(combination[combination["监考教师姓名"] == name].index)
                    assert concat_dt["所在单位"].item() == line["所在单位"]
                    if "四级" in _type:
                        concat_dt["四级级别"] = "英语四级"
                        concat_dt["四级监考"] = "主监考"
                        concat_dt["四级发卷点"] = line["发卷点"]
                    else:
                        concat_dt["六级级别"] = "英语六级"
                        concat_dt["六级监考"] = "主监考"
                        concat_dt["六级发卷点"] = line["发卷点"]
                else:
                    concat_dt = pd.DataFrame({
                        "所在单位": [line["所在单位"]],
                        "监考教师姓名": [name],
                        "性别": [line["性别"]],
                        "工资号": [line["工资号"]],
                        "手机号码": [line["手机号码"]],
                        "四级级别": ["英语四级" if "四级" in _type else ""],
                        "四级发卷点": [line["发卷点"] if "四级" in _type else ""],
                        "四级监考": ["主监考" if "四级" in _type else ""],
                        "六级级别": ["英语六级" if "六级" in _type else ""],
                        "六级发卷点": [line["发卷点"] if "六级" in _type else ""],
                        "六级监考": ["主监考" if "六级" in _type else ""]
                    })
                combination = combination.append(concat_dt, ignore_index=True)

                if len(combination[combination["监考教师姓名"] == name1]) > 0:
                    concat_dt = combination[combination["监考教师姓名"] == name1]
                    combination = combination.drop(combination[combination["监考教师姓名"] == name1].index)
                    assert concat_dt["所在单位"].item() == line["所在单位1"]
                    if "四级" in _type:
                        concat_dt["四级级别"] = "英语四级"
                        concat_dt["四级监考"] = "主监考"
                        concat_dt["四级发卷点"] = line["发卷点"]
                    else:
                        concat_dt["六级级别"] = "英语六级"
                        concat_dt["六级监考"] = "副监考"
                        concat_dt["六级发卷点"] = line["发卷点"]
                else:
                    concat_dt = pd.DataFrame({
                        "所在单位": [line["所在单位1"]],
                        "监考教师姓名": [name1],
                        "性别": [line["性别1"]],
                        "工资号": [line["工资号1"]],
                        "手机号码": [line["手机号码1"]],
                        "四级级别": ["英语四级" if "四级" in _type else ""],
                        "四级发卷点": [line["发卷点"] if "四级" in _type else ""],
                        "四级监考": ["副监考" if "四级" in _type else ""],
                        "六级级别": ["英语六级" if "六级" in _type else ""],
                        "六级发卷点": [line["发卷点"] if "六级" in _type else ""],
                        "六级监考": ["副监考" if "六级" in _type else ""]
                    })
                combination = combination.append(concat_dt, ignore_index=True)
        except:
            import traceback
            traceback.print_exc()
    with pd.ExcelWriter("联系信息.xlsx") as execl_writer:
        combination.to_excel(execl_writer, index=False)