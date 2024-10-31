from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, \
    QFileDialog
from interface.record_interface import RecordInterface
from interface.settings_interface import SettingsInterface


class StartInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.record_interface = None
        self.settings_interface = None
        self.save_path = f'./script/'

    def initUI(self):
        # 创建一个网格布局
        grid_layout = QGridLayout()

        # 创建标签和按钮
        # label = QLabel('这是一个标签')
        record_button = QPushButton('录制')
        record_button.clicked.connect(self.StartRecord)

        select_button = QPushButton('选择脚本')
        select_button.clicked.connect(self.SelectFile)

        config_button = QPushButton('设置脚本保存路径')
        config_button.clicked.connect(self.SelectPath)

        # 将控件添加到网格布局中
        grid_layout.addWidget(record_button, 1, 0)
        grid_layout.addWidget(select_button, 1, 1)
        grid_layout.addWidget(config_button, 2, 0, 1, 2)

        # 设置布局到窗口
        self.setLayout(grid_layout)

        # 设置窗口的标题和大小
        self.setWindowTitle('布局示例')
        self.setGeometry(100, 100, 300, 200)
        self.show()

    def StartRecord(self):
        print(f'当前保存路径: {self.save_path}')  # 打印当前路径
        self.record_interface = RecordInterface(self.save_path)
        self.record_interface.show()

    def SelectFile(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, '选择脚本文件', '', '脚本文件 (*.bog);;所有文件 (*)', options=options)
        if filename:
            self.settings_interface = SettingsInterface(filename)
            self.settings_interface.show()
        # if filename:
        #     print(f'选择的文件: {filename}')
        #     wait_time = 3
        #     for i in range(wait_time, 0, -1):
        #         print(f'在{i}秒后开始执行......')
        #         time.sleep(1)
        #     process_instructions(filename)
        #     print('执行完毕')

    def SelectPath(self):
        path = QFileDialog.getExistingDirectory(self, '选择保存路径')
        if path:
            self.save_path = path

