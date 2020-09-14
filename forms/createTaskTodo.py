from PySide2 import QtCore

from PySide2.QtWidgets import QDialog, QDialogButtonBox


from datamodel.models import Todoelement

from PySide2.QtUiTools import QUiLoader


class CreateTaskTodo(QDialog):
    addsignal = QtCore.Signal()

    def __init__(self, parent, dossier, session):
        super(CreateTaskTodo, self).__init__(parent)

        ui_file = ":UI\\UI\\TaskTodo.ui"
        ui_file = QtCore.QFile(ui_file)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()
        # self.setupUi(self)

        self.session = session
        # self.dateLimitEditRDV.setDate(QtCore.QDate.currentDate())
        self.validateTasktodo = self.ui.findChild(QDialogButtonBox, "validateTasktodo")
        self.validateTasktodo.accepted.connect(self.addTask2todo)
        self.dossier =dossier

    def addTask2todo(self):
        newtaskRDV = Todoelement(self.ui.NomTaskVal.text())
        newtaskRDV.dossier_id= self.dossier.id
        self.session.add(newtaskRDV)
        self.session.commit()
        self.addsignal.emit()