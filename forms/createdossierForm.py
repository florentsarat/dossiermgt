from PySide2 import QtCore
from PySide2.QtWidgets import QDialog, QDialogButtonBox

from datetime import datetime

from datamodel.models import dossier

from PySide2.QtUiTools import loadUiType


class CreateForm(QDialog, loadUiType('UI/FormCreate.ui')[0]):
    mySignal = QtCore.Signal()

    def __init__(self, parent, session):
        super(CreateForm, self).__init__(parent)
        self.session = session
        self.setupUi(self)
        self.validatedossierNewButton = self.findChild(QDialogButtonBox, "validatenewdossier")
        self.validatedossierNewButton.accepted.connect(self.clickedBtnCreateDossier)

    def clickedBtnCreateDossier(self):
        anewdossier = dossier(self.namedossier.text(), self.typeDossier.currentText(), self.provanceDrop.currentText(), self.NotaireVendeur.text(), self.NotaireAc.text(), self.textComment.toPlainText(), datetime.today(), 'En cours')
        self.session.add(anewdossier)
        self.session.commit()
        self.mySignal.emit()