import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtGui import QIntValidator, QDoubleValidator
import time
from action import process_instructions


class SettingsInterface(QWidget):
    def __init__(self, filename):
        super().__init__()
        self.initUI()
        self.filename = filename

    def initUI(self):
        self.layout = QVBoxLayout()

        # 创建多个输入框
        self.loop_amount = QLineEdit(self)
        self.loop_amount.setValidator(QIntValidator())
        self.loop_amount.setText('1')

        self.loop_gap_time = QLineEdit(self)
        self.loop_gap_time.setValidator(QDoubleValidator())
        self.loop_gap_time.setText('0')

        self.time_speed = QLineEdit(self)
        self.time_speed.setValidator(QDoubleValidator())
        self.time_speed.setText('1')

        # 创建确定按钮
        submit_button = QPushButton('启动', self)
        submit_button.clicked.connect(self.print_inputs)

        # 将输入框和按钮添加到布局中
        self.layout.addWidget(QLabel('循环次数:'))
        self.layout.addWidget(self.loop_amount)
        self.layout.addWidget(QLabel('循环间隔(秒):'))
        self.layout.addWidget(self.loop_gap_time)
        self.layout.addWidget(QLabel('倍速:'))
        self.layout.addWidget(self.time_speed)
        self.layout.addWidget(submit_button)
        self.setLayout(self.layout)
        self.setWindowTitle('脚本设置')
        self.setGeometry(100, 100, 300, 200)

    def print_inputs(self):
        # 获取输入框中的内容并打印
        loop_amount = self.loop_amount.text()
        loop_gap_time = self.loop_gap_time.text()
        time_speed = self.time_speed.text()
        print(f'循环次数: {loop_amount}')
        print(f'循环间隔: {loop_gap_time}')
        print(f'倍速: {time_speed}')
        if self.filename:
            print(f'选择的文件: {self.filename}')
            wait_time = 3
            for i in range(wait_time, 0, -1):
                print(f'在{i}秒后开始执行......')
                time.sleep(1)
            process_instructions(self.filename, int(loop_amount), float(loop_gap_time), float(time_speed))
            print('执行完毕')
