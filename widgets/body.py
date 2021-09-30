from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtWidgets import QApplication
from .utils import signed_teachers, main_monitors, candidates, exam_room, submit
import pandas as pd

button_style = """
QPushButton {
    background-color: aquamarine;
    border-radius: 4px;
    height: 20%;
    width: 33%;
    color: blueviolet;
}
QPushButton:hover {
    background-color: aqua;
    border-radius: 4px;
}
"""

class Body(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(100, 100, QApplication.desktop().width() // 2, QApplication.desktop().height() // 2)
        self.init()

    def init(self):
        # 报名的老师
        self.sign_up = QPushButton(self)
        self.sign_up.setText("报名老师名单")
        self.sign_up.setStyleSheet(button_style)
        self.sign_up.clicked.connect(lambda : signed_teachers(self, self.sign_up))

        # 担任过主考官的老师
        self.main_monitor = QPushButton(self)
        self.main_monitor.setText("担任过主考官的名单")
        self.main_monitor.setStyleSheet(button_style)
        self.main_monitor.clicked.connect(lambda : main_monitors(self, self.main_monitor))

        # 候选的老师
        self.candidate = QPushButton(self)
        self.candidate.setText("候选老师名单")
        self.candidate.setStyleSheet(button_style)
        self.candidate.clicked.connect(lambda : candidates(self, self.candidate))
        # 考场
        self.exam_room = QPushButton(self)
        self.exam_room.setText("考场名单(津南四级|津南六级|八里台四级|八里台六级)")
        self.exam_room.setStyleSheet(button_style)
        self.exam_room.clicked.connect(lambda : exam_room(self, self.exam_room))

        # 提交
        self.submit = QPushButton(self)
        self.submit.setText("提交")
        self.submit.setStyleSheet(button_style)
        self.submit.clicked.connect(lambda : submit(self))

        # teacher layout
        teacher_horizontal = QHBoxLayout()
        teacher_horizontal.setSpacing(20)

        room_horizontal = QHBoxLayout()

        teacher_horizontal.addWidget(self.sign_up)
        teacher_horizontal.addWidget(self.main_monitor)
        teacher_horizontal.addWidget(self.candidate)
        room_horizontal.addWidget(self.exam_room)

        main_vertical = QVBoxLayout()
        main_vertical.addLayout(teacher_horizontal)
        main_vertical.addLayout(room_horizontal)
        main_vertical.addWidget(self.submit)
        self.setLayout(main_vertical)

    # 报名老师名单
    def update_sign(self, dt: pd.DataFrame):
        self.sign_list = dt

    # 当过主考官的老师列表
    def update_mm(self, dt: pd.DataFrame):
        self.mm_list = dt

    # 候选老师列表
    def update_candidate(self, dt: pd.DataFrame):
        self.candidate_list = dt

    # 考场名单
    def update_exam_room(
            self,
            jin_nan4_dt: pd.DataFrame,
            jin_nan6_dt: pd.DataFrame,
            balitai4_dt: pd.DataFrame,
            balitai6_dt: pd.DataFrame
    ):
        self.jin_nan4_dt = jin_nan4_dt if len(jin_nan4_dt) > 0 and "发卷点" in jin_nan4_dt.columns else None
        self.jin_nan6_dt = jin_nan6_dt if len(jin_nan6_dt) > 0 and "发卷点" in jin_nan6_dt.columns else None
        self.balitai4_dt = balitai4_dt if len(balitai4_dt) > 0 and "发卷点" in balitai4_dt.columns else None
        self.balitai6_dt = balitai6_dt if len(balitai6_dt) > 0 and "发卷点" in balitai6_dt.columns else None

    def get_status(self, campus: str = "津南校区", exam_type: str = "4"):
        print(f"===> {campus} ==== {exam_type}")
        assert campus in ['津南校区', '八里台校区']
        assert exam_type in ["4", "6"]
        used = set()

        if exam_type == "4":
            room_in_campus = self.jin_nan4_dt if campus == "津南校区" else self.balitai4_dt
        else:
            room_in_campus = self.jin_nan6_dt if campus == '津南校区' else self.balitai6_dt
        num_of_mm_needed = len(room_in_campus)

        # 对应校区、对应考试等级的报名老师
        sign_in_campus = self.sign_list[(self.sign_list["校区"]==campus) & (self.sign_list["级别"].str.contains(exam_type))]
        mm_in_campus = sign_in_campus[sign_in_campus["监考教师姓名"].isin(self.mm_list["姓名"].tolist())]
        # 在该校区的报名老师但不是当过主监考的老师
        candidates_in_campus = self.candidate_list[
            (self.candidate_list["姓名"].isin(sign_in_campus["监考教师姓名"].tolist())) & \
            ~(self.candidate_list["姓名"].isin(mm_in_campus["监考教师姓名"].tolist()))
        ]

        # 男 / 女 -> 单位
        mm_dict = {}
        not_mm_dict = {}

        # 不同单位尽量不要在一起
        num = 0
        for (gender, danwei), group in mm_in_campus.groupby(["性别", "所在单位"], dropna=False):
            if str(gender) not in mm_dict:
                mm_dict[gender] = {}
            if danwei not in mm_dict[gender]:
                mm_dict[gender][danwei] = set()
            num_left = num_of_mm_needed - num
            teacher_set = set(group["监考教师姓名"].tolist()[:num_left])
            mm_dict[gender][danwei].update(teacher_set)
            used.update(teacher_set)
            num += len(teacher_set)

        # 从候选里面选择
        if num < num_of_mm_needed:
            candidate = sign_in_campus[sign_in_campus["监考教师姓名"].isin(candidates_in_campus["姓名"].tolist())]
            for (gender, danwei), group in candidate.groupby(["性别", "所在单位"], dropna=False):
                if str(gender) not in mm_dict:
                    mm_dict[gender] = {}
                if danwei not in mm_dict[gender]:
                    mm_dict[gender][danwei] = set()
                num_left = num_of_mm_needed - num
                teacher_set = set(group["监考教师姓名"].tolist()[:num_left])
                mm_dict[gender][danwei].update(teacher_set)
                used.update(teacher_set)
                num += len(teacher_set)
                if num >= num_of_mm_needed:
                    break

        # 从参加过的老师里面选
        if num < num_of_mm_needed:
            exped = sign_in_campus[(~sign_in_campus["监考教师姓名"].isin(used)) & (sign_in_campus["是否参加过"] == "参加过")]
            for (gender, danwei), group in exped.groupby(["性别", "所在单位"], dropna=False):
                if str(gender) not in mm_dict:
                    mm_dict[gender] = {}
                if danwei not in mm_dict[gender]:
                    mm_dict[gender][danwei] = set()
                num_left = num_of_mm_needed - num
                teacher_set = set(group["监考教师姓名"].tolist()[:num_left])
                mm_dict[gender][danwei].update(teacher_set)
                used.update(teacher_set)
                num += len(teacher_set)
                if num >= num_of_mm_needed:
                    break
        print(f"mm_len: {num}")

        # 从所有未安排为主考官的老师里面选择
        not_mm = sign_in_campus[
            ~(sign_in_campus["监考教师姓名"].isin(self.mm_list["姓名"].tolist())) & \
            ~(sign_in_campus["监考教师姓名"].isin(candidates_in_campus["姓名"].tolist())) & \
            ~(sign_in_campus["监考教师姓名"].isin(used))
        ]
        not_num = 0

        for (gender, danwei), group in not_mm.groupby(["性别", "所在单位"], dropna=False):
            if gender not in not_mm_dict:
                not_mm_dict[gender] = {}
            if danwei not in not_mm_dict[gender]:
                not_mm_dict[gender][danwei] = set()
            teacher_set = set(group["监考教师姓名"].tolist())
            not_mm_dict[gender][danwei].update(teacher_set)
            not_num += len(teacher_set)
        print(f"not_mm_len: {not_num} |  total: {len(not_mm)}")

        result = set()
        used.clear()
        for gender in ["男", "女"]:
            for campus_tmp in mm_dict[gender]:
                for teacher in mm_dict[gender][campus_tmp]:
                    if teacher not in used:
                        _pair = None
                        for _gender in not_mm_dict:
                            if _pair is not None: break
                            if _gender != gender:
                                for _campus in not_mm_dict[_gender]:
                                    if _pair is not None: break
                                    if _campus != campus_tmp:
                                        for _teacher in not_mm_dict[_gender][_campus]:
                                            if _teacher not in used:
                                                _pair = _teacher
                                                break
                        if _pair is None:  # 如果不能男女搭配, 就女女搭配
                            for _campus in not_mm_dict["女"]:
                                if _pair is not None: break
                                if _campus != campus_tmp:
                                    for _teacher in not_mm_dict["女"][_campus]:
                                        if _teacher not in used:
                                            _pair = _teacher
                                            break
                        if _pair is not None:
                            result.add((teacher, _pair))
                            used.add(teacher)
                            used.add(_pair)
                            _pair = None
                        else:
                            print("未匹配教师: ", teacher, gender)
        assert len(result) == len(room_in_campus), f"分配配对数{len(result)}, 所需的配对数{len(room_in_campus)}"
        assign = {}
        for room, (t1, t2) in zip(room_in_campus["考场地址及名称"].tolist(), result):
            assign[str(room)] = [t1, t2]
        print(f"{campus} - {exam_type} - Finish!")

        rooms = list(assign.keys())
        mm = [v[0] for v in assign.values()]
        vice_mm = [v[1] for v in assign.values()]
        room_ids = []
        campus_ids = []
        fajuandian = []
        locations = []
        types = []

        # 主考官
        mm_danwei = []
        mm_name = []
        mm_gender = []
        mm_gongzihao = []
        mm_tag = []
        mm_phone_number = []
        mm_take_bus = []

        # 副监考
        vice_danwei = []
        vice_name = []
        vice_gender = []
        vice_gongzihao = []
        vice_tag = []
        vice_phone_number = []
        vice_take_bus = []

        for r, m, v in zip(rooms, mm, vice_mm):
            r_obj = room_in_campus[room_in_campus["考场地址及名称"] == r]
            m_obj = sign_in_campus[sign_in_campus["监考教师姓名"] == m]
            v_obj = sign_in_campus[sign_in_campus["监考教师姓名"] == v]
            room_ids.append(r_obj["考场号"].item())
            campus_ids.append(r_obj["校区代码"].item())
            fajuandian.append(r_obj["发卷点"].item())
            locations.append(r_obj["考场地址及名称"].item())
            types.append(r_obj["科目级别"].item())

            mm_danwei.append(m_obj["所在单位"].item())
            mm_name.append(m_obj["监考教师姓名"].item())
            mm_gender.append(m_obj["性别"].item())
            mm_gongzihao.append(m_obj["工资号"].item())
            mm_tag.append("主监考")
            mm_phone_number.append(m_obj["手机号码"].item())
            mm_take_bus.append(m_obj["是否乘车"].item())

            vice_danwei.append(v_obj["所在单位"].item())
            vice_name.append(v_obj["监考教师姓名"].item())
            vice_gender.append(v_obj["性别"].item())
            vice_gongzihao.append(v_obj["工资号"].item())
            vice_tag.append("副监考")
            vice_phone_number.append(v_obj["手机号码"].item())
            vice_take_bus.append(v_obj["是否乘车"].item())


        dt = pd.DataFrame({
            "考场号": room_ids,
            "校区代码": campus_ids,
            "发卷点": fajuandian,
            "考场地址及名称": locations,
            "科目级别": types,
            "所在单位": mm_danwei,
            "监考教师姓名": mm_name,
            "性别": mm_gender,
            "工资号": mm_gongzihao,
            "主监考": mm_tag,
            "手机号码": mm_phone_number,
            "是否乘车": mm_take_bus,
            "所在单位1": vice_danwei,
            "监考教师姓名1": vice_name,
            "性别1": vice_gender,
            "工资号1": vice_gongzihao,
            "主监考1": vice_tag,
            "手机号码1": vice_phone_number,
            "是否乘车1": vice_take_bus,

        })

        return dt