from PySide2 import QtCore

from PySide2.QtWidgets import QDialog
from PySide2.QtUiTools import QUiLoader


class aboutForm(QDialog):

    def __init__(self, parent):
        super(aboutForm, self).__init__(parent)

        ui_file = ":UI\\UI\\about.ui"
        # ui_file = "UI\\about.ui"
        ui_file = QtCore.QFile(ui_file)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

