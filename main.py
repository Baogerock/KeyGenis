from interface.start_interface import StartInterface
import sys
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    interface = StartInterface()
    sys.exit(app.exec_())

