from PySide6 import QtCore
from PySide6.QtCore import QSize, QDir, QFileInfo
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QDialog, QGridLayout, QLineEdit, QPushButton, QLabel, QDialogButtonBox, QFileDialog


class NewProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._error = ""
        self._template = "TestProject"

        self._nameEdit = QLineEdit()
        self._nameEdit.textChanged.connect(self._checkPathAndName)
        self._pathEdit = QLineEdit()
        self._pathEdit.textChanged.connect(self._checkPathAndName)
        self._browseBtn = QPushButton("...")
        self._browseBtn.setFixedWidth(30)
        self._browseBtn.clicked.connect(self.onBrowseClicked)
        self._buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self._buttonBox.clicked.connect(self.onButtonBoxClicked)

        self._layout = QGridLayout(self)
        self._layout.addWidget(QLabel("项目名称"), 0, 0)
        self._layout.addWidget(self._nameEdit, 0, 1, 1, 2)
        self._layout.addWidget(QLabel("项目路径"), 1, 0)
        self._layout.addWidget(self._pathEdit, 1, 1)
        self._layout.addWidget(self._browseBtn, 1, 2)
        self._layout.addWidget(self._buttonBox, 2, 0, 1, 3)

        self.setWindowTitle("创建项目")

    def exec(self):
        path = QDir.currentPath()
        name = self._calcProjectName(path)
        self._nameEdit.setText(name)
        self._pathEdit.setText(path)

        super().exec()
        if self.result() == self.DialogCode.Accepted:
            return self._pathEdit.text(), self._nameEdit.text()
        return None, None

    def sizeHint(self):
        return QSize(400, 128)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen("red")
        if btn := self._buttonBox.button(QDialogButtonBox.StandardButton.Ok):
            pos = btn.mapTo(self, btn.pos())
            painter.drawText(15, 15 + int(pos.y()), self._error)
        super().paintEvent(event)

    @QtCore.Slot()
    def onBrowseClicked(self):
        path = self._pathEdit.text()
        path = QFileDialog.getExistingDirectory(self, "选择目录", path)
        if len(path):
            self._pathEdit.setText(path)

    @QtCore.Slot()
    def onButtonBoxClicked(self, button):
        role = self._buttonBox.standardButton(button)
        if role == QDialogButtonBox.StandardButton.Ok:
            if self._checkPathAndName():
                self.accept()
        else:
            self.reject()

    def _calcProjectName(self, path):
        result = self._template
        qtDir = QDir(path)
        if qtDir.exists():
            if qtDir.exists(result):
                for index in range(1, 999999):
                    temp = f"{self._template}{index}"
                    if not qtDir.exists(temp):
                        result = temp
                        break
        return result

    def _checkPathAndName(self):

        name = self._nameEdit.text()
        path = self._pathEdit.text()
        qtDir = QDir(path)
        if not qtDir.exists():
            self._error = "目录不存在"
            self.update()
            return False
        if qtDir.exists(name):
            self._error = "项目已存在"
            self.update()
            return False

        self._error = ""
        self.update()
        return True
