from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtWidgets import QApplication
from .utils import signed_teachers


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

        # 候选的老师
        self.candidate = QPushButton(self)
        self.candidate.setText("候选老师名单")
        self.candidate.setStyleSheet(button_style)

        # 津南考场
        self.jin_nan_exam_room = QPushButton(self)
        self.jin_nan_exam_room.setText("津南考场名单")
        self.jin_nan_exam_room.setStyleSheet(button_style)

        # 八里台考场
        self.balitai_exam_room = QPushButton(self)
        self.balitai_exam_room.setText("八里台考场名单")
        self.balitai_exam_room.setStyleSheet(button_style)

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

