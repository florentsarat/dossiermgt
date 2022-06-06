from PySide2 import QtCore

from PySide2.QtWidgets import QDialog, QDialogButtonBox


from datamodel.models import Todoelement

from PySide2.QtUiTools import QUiLoader


class CreateTaskV2Todo(QDialog):
    addsignal = QtCore.Signal(Todoelement, QtCore.QModelIndex)

    def __init__(self, parent, dossier, session, index):
        super(CreateTaskV2Todo, self).__init__(parent)

        ui_file = ":UI\\UI\\RDVTodo.ui"
        # ui_file = "UI\\RDVTodo.ui"
        ui_file = QtCore.QFile(ui_file)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        self.session = session

        self.index = index

        self.ui.dateLimitEditRDV.setDate(QtCore.QDate.currentDate())
        self.validateRDVtodo = self.ui.findChild(QDialogButtonBox, "validateRDVtodo")
        self.validateRDVtodo.accepted.connect(self.addRDV2todo)
        self.dossier =dossier

    def addRDV2todo(self):
        newtasktodo = Todoelement(self.ui.NomRDVal.text(), self.ui.dateLimitEditRDV.dateTime().toPython())
        newtasktodo.dossier_id= self.dossier.id
        self.session.add(newtasktodo)
        self.session.commit()
        self.addsignal.emit(newtasktodo, self.index)