import sys
import asyncio

from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QComboBox
from PyQt5.QtWidgets import QMainWindow, QDialog
from PyQt5.QtCore import Qt
from qasync import QEventLoop

from main_window import MainWindow




if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Integrate asyncio with PyQt5 event loop
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)  

    window = MainWindow()
    window.show()

    with loop:
        loop.run_forever()

