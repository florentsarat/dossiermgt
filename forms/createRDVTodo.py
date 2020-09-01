from PySide2 import QtCore
from PySide2.QtWidgets import QDialog, QDialogButtonBox


from datamodel.models import todoRDV

from PySide2.QtUiTools import loadUiType


class CreateRDVTodo(QDialog, loadUiType('UI/RDVTodo.ui')[0]):
    addsignal = QtCore.Signal()

    def __init__(self, parent, dossier, session):
        super(CreateRDVTodo, self).__init__(parent)
        self.setupUi(self)
        self.session = session
        self.validateRDVtodo = self.findChild(QDialogButtonBox, "validateRDVtodo")
        self.validateRDVtodo.accepted.connect(self.addRDV2todo)
        self.dossier =dossier

    def addRDV2todo(self):
        newtodoRDV = todoRDV(self.NomRDVal.text(), self.AvecVal.text(), self.typeRDVVal.text(), self.dateLimitEditRDV.dateTime().toPython())
        newtodoRDV.dossier_id= self.dossier.id
        self.session.add(newtodoRDV)
        self.session.commit()
        self.addsignal.emit()