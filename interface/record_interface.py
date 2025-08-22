import os
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, \
    QFileDialog
from pynput import mouse, keyboard
import time

pressed_info = {}
time_stamp = 0


class RecordInterface(QWidget):
    def __init__(self, save_path):
        super().__init__()
        self.initUI()
        self.mouse_listener = None
        self.keyboard_listener = None
        self.is_listening = False
        self.script = None
        self.count = 1
        self.save_path = save_path
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path, exist_ok=True)

    def initUI(self):
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
        grid_layout.setContentsMargins(20, 20, 20, 20)

        start_button = QPushButton('开始')
        pause_button = QPushButton('暂停')  # 现在还不起任何作用
        end_button = QPushButton('结束')

        grid_layout.addWidget(start_button, 1, 0)
        grid_layout.addWidget(pause_button, 1, 1)
        grid_layout.addWidget(end_button, 1, 2)

        self.setLayout(grid_layout)
        self.setStyleSheet(
            """
            QWidget {
                font-family: 'Arial';
                font-size: 14px;
            }
            QPushButton {
                padding: 6px 12px;
                border-radius: 4px;
            }
            """
        )

        self.setWindowTitle('录制中')
        self.setGeometry(200, 200, 300, 200)
        self.show()

        start_button.clicked.connect(self.start_listening)
        end_button.clicked.connect(self.stop_listening)

    def on_mouse_press(self, x, y, button, pressed):
        if pressed:
            pressed_info[button] = {'time': time.time(), 'press_position': (x, y)}  # 记录按下时间和位置
        else:
            if button in pressed_info:
                duration = time.time() - pressed_info[button]['time']  # 计算持续时间
                press_position = pressed_info[button]['press_position']  # 获取按下的位置
                release_position = (x, y)  # 记录松开时的位置
                print(f'鼠标按钮 {button} 在位置 {press_position} 按下，松开在位置 {release_position}，持续了 {duration:.2f} 秒')
                del pressed_info[button]  # 移除记录

    def on_key_press(self, key):
        if key not in pressed_info:  # 仅记录一次按下事件
            pressed_info[key] = time.time()  # 记录按下时间

    def on_key_release(self, key):
        if key in pressed_info:
            duration = time.time() - pressed_info[key]  # 计算持续时间
            print(f'键 {key} 按下持续了 {duration:.2f} 秒')
            del pressed_info[key]  # 移除记录

    def start_listening(self):
        global time_stamp
        time_stamp = time.time()
        if not self.is_listening:
            while os.path.exists(f'{self.save_path}/mouse_log_{self.count}.bog'):
                self.count += 1
            self.script = open(f'{self.save_path}/mouse_log_{self.count}.bog', 'w')  # 在这里打开文件

            self.mouse_listener = mouse.Listener(
                on_click=lambda x, y, button, pressed: on_mouse_press(x, y, button, pressed, self.script))
            self.keyboard_listener = keyboard.Listener(on_press=lambda key: on_key_press(key, self.script),
                                                       on_release=lambda key: on_key_release(key, self.script))
            self.mouse_listener.start()
            self.keyboard_listener.start()
            self.is_listening = True
            print("开始录制")

    def stop_listening(self):
        if self.is_listening:
            self.mouse_listener.stop()
            self.keyboard_listener.stop()
            self.is_listening = False

            self.script.close()
            print("监听已停止")


def on_mouse_press(x, y, button, pressed, script):
    global time_stamp
    wait_duration = time.time() - time_stamp
    time_stamp = time.time()
    output = f'wait {wait_duration:.2f}\n'
    script.write(output)  # 写入文件

    if pressed:
        pressed_info[button] = {'time': time.time(), 'press_position': (x, y)}  # 记录按下时间和位置
    else:
        if button in pressed_info:
            duration = time.time() - pressed_info[button]['time']  # 计算持续时间
            press_position = pressed_info[button]['press_position']  # 获取按下的位置
            release_position = (x, y)  # 记录松开时的位置
            output = f'mouse {button} {press_position} {release_position} {duration:.2f}\n'
            print(f'鼠标按钮 {button} 在位置 {press_position} 按下，松开在位置 {release_position}，持续了 {duration:.2f} 秒')
            script.write(output)  # 写入文件
            del pressed_info[button]  # 移除记录


def on_key_press(key, script):
    global time_stamp
    wait_duration = time.time() - time_stamp
    time_stamp = time.time()
    output = f'wait {wait_duration:.2f}\n'
    script.write(output)  # 写入文件

    if key not in pressed_info:  # 仅记录一次按下事件
        pressed_info[key] = time.time()  # 记录按下时间


def on_key_release(key, script):
    if key in pressed_info:
        duration = time.time() - pressed_info[key]  # 计算持续时间
        output = f'keyboard {key} {duration:.2f}\n'
        print(f'键 {key} 按下持续了 {duration:.2f} 秒')
        script.write(output)  # 写入文件
        del pressed_info[key]  # 移除记录
