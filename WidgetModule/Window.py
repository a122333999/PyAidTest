from PySide6.QtWidgets import QMainWindow
from WidgetModule.ui_window import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("PyGuiTest")
        self.resize(1000, 600)
