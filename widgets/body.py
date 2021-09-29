from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtWidgets import QApplication
from .utils import signed_teachers, main_monitors, candidates, jin_nan, balitai
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

        # 津南考场
        self.jin_nan_exam_room = QPushButton(self)
        self.jin_nan_exam_room.setText("津南考场名单")
        self.jin_nan_exam_room.setStyleSheet(button_style)
        self.jin_nan_exam_room.clicked.connect(lambda : jin_nan(self, self.jin_nan_exam_room))


        # 八里台考场
        self.balitai_exam_room = QPushButton(self)
        self.balitai_exam_room.setText("八里台考场名单")
        self.balitai_exam_room.setStyleSheet(button_style)
        self.balitai_exam_room.clicked.connect(lambda :balitai(self, self.balitai_exam_room))

        # 提交
        self.submit = QPushButton(self)
        self.submit.setText("提交")
        self.submit.setStyleSheet(button_style)

        # teacher layout
        teacher_horizontal = QHBoxLayout()
        teacher_horizontal.setSpacing(20)

        room_horizontal = QHBoxLayout()

        teacher_horizontal.addWidget(self.sign_up)
        teacher_horizontal.addWidget(self.main_monitor)
        teacher_horizontal.addWidget(self.candidate)
        room_horizontal.addWidget(self.jin_nan_exam_room)
        room_horizontal.addWidget(self.balitai_exam_room)

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

    # 津南考场名单
    def update_jinnan(self, dt: pd.DataFrame):
        self.jin_nan_list = dt

    # 八里台考场名单
    def update_balitai(self, dt: pd.DataFrame):
        self.balitai_list = dt

    def get_status(self, campus: str = "津南校区"):
        assert campus in ['津南校区', '八里台校区']
        room_in_campus = self.jin_nan_list if campus == "津南校区" else self.balitai_list
        num_of_mm = len(room_in_campus)

        sign_in_campus = self.sign_list[self.sign_list["校区"]==campus]
        mm_in_campus = sign_in_campus[sign_in_campus["监考教师姓名"].isin(self.mm_list["姓名"].tolist())]
        # 在该校区的报名老师但不是当过主监考的老师
        candidates_in_campus = self.candidate[(self.candidate["姓名"].isin(sign_in_campus["监考教师姓名"].tolist())) & ~(self.candidate["姓名"].isin(mm_in_campus["姓名"].tolist()))]


