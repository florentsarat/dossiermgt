from PySide2 import QtCore
from PySide2.QtWidgets import QDialog, QDialogButtonBox

from datetime import datetime

from datamodel.models import Dossier

from PySide2.QtUiTools import QUiLoader

import ressources


class CreateForm(QDialog):
    mySignal = QtCore.Signal(Dossier)

    def __init__(self, parent, session):
        super(CreateForm, self).__init__(parent)

        # ui_file = ":UI\\UI\\FormCreate.ui"
        ui_file = "UI\\FormCreate.ui"
        ui_file = QtCore.QFile(ui_file)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        self.session = session

        self.ui.provanceDrop.currentIndexChanged.connect(self.manageAvantContratFromDropProvenance)
        self.validatedossierButton = self.ui.findChild(QDialogButtonBox, "validatenewdossier")
        self.validatedossierButton.accepted.connect(self.clickedBtnCreateDossier)

    def manageAvantContratFromDropProvenance(self):
        if self.ui.provanceDrop.currentText() != "Agence":
            self.ui.statusAvantContrat.hide()
            self.ui.statusAvantContratComb.hide()
        else:
            self.ui.statusAvantContrat.show()
            self.ui.statusAvantContratComb.show()

    def clickedBtnCreateDossier(self):
        if self.ui.provanceDrop.currentText() != "Agence":
            statusAvantContrat = "A faire"
            status = "PUV en préparation"
        else:
            statusAvantContrat = self.ui.statusAvantContratComb.currentText()
            status = "Sign Compro en cours"

        anewdossier = Dossier(self.ui.namedossier.text(), self.ui.typeDossier.currentText(),
                              self.ui.provanceDrop.currentText(), self.ui.NotaireVendeur.text(),
                              self.ui.NotaireAc.text(), statusAvantContrat,
                              self.ui.textComment.toPlainText(), datetime.today(), status)
        self.session.add(anewdossier)
        self.session.commit()
        self.mySignal.emit(anewdossier)