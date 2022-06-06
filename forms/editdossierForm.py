
from PySide2.QtWidgets import QDialog,QTableView, QDialogButtonBox, QPushButton
from PySide2 import QtCore

from PySide2.QtUiTools import QUiLoader

from viewmodels import taskInDossier, viewdelegates as viewdelegates

from forms import createTaskV2Todo

from datamodel.models import Dossier, Todoelement

import resources


class EditForm(QDialog):
    mySignal = QtCore.Signal(QtCore.QModelIndex, Dossier)
    mySignalFortasksUpdate = QtCore.Signal(QtCore.QModelIndex, Todoelement)
    mySignalForNewtask = QtCore.Signal(Todoelement)

    def __init__(self, parent, session, mydossier, index):
        super(EditForm, self).__init__(parent)

        ui_file =":UI\\UI\\ViewDossier.ui"
        # ui_file = "UI\\ViewDossier.ui"
        ui_file = QtCore.QFile(ui_file)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        self.session = session

        self.dossier = mydossier
        self.index = index

        # Comboxbox management
        self.ui.combostatusdossier.currentIndexChanged.connect(self.flagasstatuschangemanually)
        self.ui.statusDia.currentIndexChanged.connect(self.diamanagement)
        self.ui.statutPC.currentIndexChanged.connect(self.pcmanagement)
        self.ui.RDVFixe.stateChanged.connect(self.managerdvfixe)
        self.ui.pretRdy.stateChanged.connect(self.pretDatemanagement)
        self.ui.venteRdy.stateChanged.connect(self.venteDatemanagement)

        self.populateview()
        self.populatetodotable()
        self.setdisplay()

        self.statuschangemant = False

        self.validatedossierButton = self.ui.findChild(QDialogButtonBox, "validatedossier")
        self.validatedossierButton.accepted.connect(self.clickedbtnsavedossier)

        self.createnewtaskbutton = self.ui.findChild(QPushButton,'addNewTaskButton')
        self.createnewtaskbutton.clicked.connect(self.addnewbuttonaction)

    def setdisplay(self):

        self.diamanagement()
        self.pcmanagement()

        if self.ui.RDVFixe.checkState() == QtCore.Qt.Checked:
            self.ui.rdvsignlab.show()
            self.ui.dateRDV.show()
        else:
            self.ui.rdvsignlab.hide()
            self.ui.dateRDV.hide()

        if self.ui.pretRdy.checkState() == QtCore.Qt.Checked:
            self.ui.datepret.show()
        else:
            self.ui.datepret.hide()

        if self.ui.venteRdy.checkState() == QtCore.Qt.Checked:
            self.ui.datevente.show()
        else:
            self.ui.datevente.hide()

    def managerdvfixe(self, state):
        if state == QtCore.Qt.Checked:
            self.ui.rdvsignlab.show()
            self.ui.dateRDV.show()
        else:
            self.ui.rdvsignlab.hide()
            self.ui.dateRDV.hide()

    def venteDatemanagement(self, state):
        if state == QtCore.Qt.Checked:
            self.ui.datevente.show()
        else:
            self.ui.datevente.hide()

    def pretDatemanagement(self, state):
        if state == QtCore.Qt.Checked:
            self.ui.datepret.show()
        else:
            self.ui.datepret.hide()

    def pcmanagement(self):
        if self.ui.statutPC.currentText() == "A Faire":
            self.ui.labeldepotPC.hide()
            self.ui.DepotPCDate.hide()
            self.ui.labelPC.hide()
            self.ui.datePC.hide()
        elif self.ui.statutPC.currentText() == "Dépôt":
            self.ui.labeldepotPC.show()
            self.ui.DepotPCDate.show()
            self.ui.labelPC.hide()
            self.ui.datePC.hide()
        else:
            self.ui.labeldepotPC.show()
            self.ui.DepotPCDate.show()
            self.ui.labelPC.show()
            self.ui.datePC.show()

    def diamanagement(self):
        if self.ui.statusDia.currentText() == "Non":
            self.ui.dateenvoilab.hide()
            self.ui.datesendDIA.hide()
            self.ui.daterecepDIALab.hide()
            self.ui.daterecDia.hide()
        elif self.ui.statusDia.currentText() == "Envoyé":
            self.ui.dateenvoilab.show()
            self.ui.datesendDIA.show()
            self.ui.daterecepDIALab.hide()
            self.ui.daterecDia.hide()
        elif self.ui.statusDia.currentText() == "Oui":
            self.ui.dateenvoilab.show()
            self.ui.datesendDIA.show()
            self.ui.daterecepDIALab.show()
            self.ui.daterecDia.show()

    def flagasstatuschangemanually(self):
        self.statuschangemant = True

    def populateview(self):
        self.ui.namedossier.setText(self.dossier.nameDossier)

        if self.dossier.dossierprovenance =="Agence":
            self.ui.provanceDrop.setCurrentIndex(0)
        else:
            self.ui.provanceDrop.setCurrentIndex(1)

        if self.dossier.statusDossier == "PUV en préparation":
            self.ui.combostatusdossier.setCurrentIndex(0)
        elif self.dossier.statusDossier == "SRU à traiter":
            self.ui.combostatusdossier.setCurrentIndex(1)
        elif self.dossier.statusDossier == "Dossier à constituer":
            self.ui.combostatusdossier.setCurrentIndex(2)
        elif self.dossier.statusDossier == "En Attente ODP":
            self.ui.combostatusdossier.setCurrentIndex(3)
        elif self.dossier.statusDossier == "RDV à fixer":
            self.ui.combostatusdossier.setCurrentIndex(4)
        elif self.dossier.statusDossier == "Vente à rédiger":
            self.ui.combostatusdossier.setCurrentIndex(5)
        elif self.dossier.statusDossier == "Sign Compro en cours":
            self.ui.combostatusdossier.setCurrentIndex(6)
        elif self.dossier.statusDossier == "Clos":
            self.ui.combostatusdossier.setCurrentIndex(7)

        self.ui.Notac.setText(self.dossier.notaireacquereurDossier)
        self.ui.NotaireVendeur.setText(self.dossier.notairevendeurDossier)

        if self.dossier.typeDossier == "Appartement":
            self.ui.typeDossierCombo.setCurrentIndex(0)
        elif self.dossier.typeDossier == "Terrain à batir(TAB)":
            self.ui.typeDossierCombo.setCurrentIndex(1)
        elif self.dossier.typeDossier == "Maison":
            self.ui.typeDossierCombo.setCurrentIndex(5)
            self.ui.typeDossierCombo.setCurrentIndex(2)
        elif self.dossier.typeDossier == "Lotissement":
            self.ui.typeDossierCombo.setCurrentIndex(3)
        elif self.dossier.typeDossier == "Garage":
            self.ui.typeDossierCombo.setCurrentIndex(4)
        elif self.dossier.typeDossier == "VEFA":
            self.ui.typeDossierCombo.setCurrentIndex(5)
        elif self.dossier.typeDossier == "SCI":
            self.ui.typeDossierCombo.setCurrentIndex(6)
        elif self.dossier.typeDossier == "Parcelle":
            self.ui.typeDossierCombo.setCurrentIndex(7)
        elif self.dossier.typeDossier == "Terrain":
            self.ui.typeDossierCombo.setCurrentIndex(8)

        if self.dossier.statusavantContrat == "A faire":
            self.ui.statusAvantContratComb.setCurrentIndex(0)
        elif self.dossier.statusavantContrat == "En cours":
            self.ui.statusAvantContratComb.setCurrentIndex(1)
        elif self.dossier.statusavantContrat == "En cours - Agence":
            self.ui.statusAvantContratComb.setCurrentIndex(2)
        elif self.dossier.statusavantContrat == "OK":
            self.ui.statusAvantContratComb.setCurrentIndex(3)
        elif self.dossier.statusavantContrat == "OK - Agence":
            self.ui.statusAvantContratComb.setCurrentIndex(4)

        self.ui.prixVente.setText(str(self.dossier.priceSalesDossier))

        if self.dossier.ODPReceived == "Pas reçu":
            self.ui.statusODP.setCurrentIndex(0)
        elif self.dossier.ODPReceived == "Reçu":
            self.ui.statusODP.setCurrentIndex(1)
        elif self.dossier.ODPReceived == "Pas de prêt":
            self.ui.statusODP.setCurrentIndex(2)

        if self.dossier.statusSRU == "A vérifier":
            self.ui.statusSRU.setCurrentIndex(0)
        elif self.dossier.statusSRU == "OK":
            self.ui.statusSRU.setCurrentIndex(1)
        elif self.dossier.statusSRU == "En cours":
            self.ui.statusSRU.setCurrentIndex(2)

        if self.dossier.pret == "Oui":
            self.ui.besoinpret.setCurrentIndex(0)
        elif self.dossier.pret == "Non":
            self.ui.besoinpret.setCurrentIndex(1)
        elif self.dossier.pret == "Je ne sais pas":
            self.ui.besoinpret.setCurrentIndex(2)

        self.ui.commentsDossier.setText(self.dossier.commentsDossier)

        if self.dossier.statusDia =="Non":
            self.ui.statusDia.setCurrentIndex(0)
        elif self.dossier.statusDia =="Envoyé":
            self.ui.statusDia.setCurrentIndex(1)
        elif self.dossier.statusDia =="Oui":
            self.ui.statusDia.setCurrentIndex(2)

        if self.dossier.statusPC == "A Faire":
            self.ui.statutPC.setCurrentIndex(0)
        elif self.dossier.statusPC == "Dépôt":
            self.ui.statutPC.setCurrentIndex(1)
        else:
            self.ui.statutPC.setCurrentIndex(2)

        if self.dossier.dossierReady:
            self.ui.checkboxDossierRdy.setCheckState(QtCore.Qt.Checked)
        else:
            self.ui.checkboxDossierRdy.setCheckState(QtCore.Qt.Unchecked)

        if self.dossier.deadlinePretRdy:
            self.ui.pretRdy.setCheckState(QtCore.Qt.Checked)
        else:
            self.ui.pretRdy.setCheckState(QtCore.Qt.Unchecked)

        if self.dossier.deadlineVenteRdy:
            self.ui.venteRdy.setCheckState(QtCore.Qt.Checked)
        else:
            self.ui.venteRdy.setCheckState(QtCore.Qt.Unchecked)

        if self.dossier.RDVFixe:
            self.ui.RDVFixe.setCheckState(QtCore.Qt.Checked)
        else:
            self.ui.RDVFixe.setCheckState(QtCore.Qt.Unchecked)

        if self.dossier.partNotaire is not None:
            self.ui.partNotaire.setValue(self.dossier.partNotaire)

        self.managedates()

    def managedates(self):

        if self.dossier.DiaSendDate is None:
            self.ui.datesendDIA.setDate(QtCore.QDate.currentDate())
        else:
            self.ui.datesendDIA.setDate(self.dossier.DiaSendDate)

        if self.dossier.DiaAnsDate is None:
            self.ui.daterecDia.setDate(QtCore.QDate.currentDate())
        else:
            self.ui.daterecDia.setDate(self.dossier.DiaAnsDate)

        if self.dossier.deadlineDepotPC is None:
            self.ui.DepotPCDate.setDate(QtCore.QDate.currentDate())
        else:
            self.ui.DepotPCDate.setDate(self.dossier.deadlineDepotPC)

        if self.dossier.deadlinePret is None:
            self.ui.datepret.setDate(QtCore.QDate.currentDate())
        else:
            self.ui.datepret.setDate(self.dossier.deadlinePret)

        if self.dossier.deadlinePC is None:
            self.ui.datePC.setDate(QtCore.QDate.currentDate())
        else:
            self.ui.datePC.setDate(self.dossier.deadlinePC)

        if self.dossier.deadlineVente is None:
            self.ui.datevente.setDate(QtCore.QDate.currentDate())
        else:
            self.ui.datevente.setDate(self.dossier.deadlineVente)

        if self.dossier.datesignature is None:
            self.ui.dateRDV.setDateTime(QtCore.QDateTime.currentDateTime())
        else:
            self.ui.dateRDV.setDateTime(self.dossier.datesignature)

    def clickedbtnsavedossier(self):
        self.dossier.nameDossier = self.ui.namedossier.text()
        self.dossier.dossierprovenance = self.ui.provanceDrop.currentText()

        if self.statuschangemant:
            self.dossier.statusDossier = self.ui.combostatusdossier.currentText()
        else:
            self.statuslogic()

        self.dossier.notaireacquereurDossier = self.ui.Notac.text()
        self.dossier.notairevendeurDossier = self.ui.NotaireVendeur.text()
        self.dossier.typeDossier = self.ui.typeDossierCombo.currentText()

        self.dossier.statusavantContrat = self.ui.statusAvantContratComb.currentText()
        self.dossier.priceSalesDossier = self.ui.prixVente.text()
        self.dossier.mobiliersDossier = self.ui.valeurMobilier.text()

        self.dossier.ODPReceived = self.ui.statusODP.currentText()
        self.dossier.statusSRU = self.ui.statusSRU.currentText()
        self.dossier.pret = self.ui.besoinpret.currentText()

        self.dossier.commentsDossier = self.ui.commentsDossier.toPlainText()

        self.dossier.statusDia = self.ui.statusDia.currentText()

        if self.ui.statusDia.currentText() == "Non":
            pass
        elif self.ui.statusDia.currentText() == "Envoyé":
            self.dossier.DiaSendDate = self.ui.datesendDIA.dateTime().toPython()
        elif self.ui.statusDia.currentText() == "Oui":
            self.dossier.DiaSendDate = self.ui.datesendDIA.dateTime().toPython()
            self.dossier.DiaAnsDate = self.ui.daterecDia.dateTime().toPython()

        self.dossier.statusPC = self.ui.statutPC.currentText()

        if self.ui.statutPC.currentText() == "A Faire":
            pass
        elif self.ui.statutPC.currentText() == "Dépôt":
            self.dossier.deadlineDepotPC = self.ui.DepotPCDate.dateTime().toPython()
        else:
            self.dossier.deadlineDepotPC = self.ui.DepotPCDate.dateTime().toPython()
            self.dossier.deadlinePC = self.ui.datePC.dateTime().toPython()

        if self.ui.checkboxDossierRdy.checkState() == QtCore.Qt.Checked:
            self.dossier.dossierReady = True
        else:
            self.dossier.dossierReady = False

        if self.ui.RDVFixe.checkState() == QtCore.Qt.Checked:
            self.dossier.RDVFixe = True
        else:
            self.dossier.RDVFixe = False

        self.dossier.partNotaire =self.ui.partNotaire.value()

        if self.ui.pretRdy.checkState() == QtCore.Qt.Checked:
            self.dossier.deadlinePretRdy = True
            self.dossier.deadlinePret = self.ui.datepret.dateTime().toPython()
        else:
            self.dossier.deadlinePretRdy = False

        if self.ui.venteRdy.checkState() == QtCore.Qt.Checked:
            self.dossier.deadlineVenteRdy = True
            self.dossier.deadlineVente = self.ui.datevente.dateTime().toPython()
        else:
            self.dossier.deadlineVenteRdy = False

        if self.ui.RDVFixe.checkState() == QtCore.Qt.Checked:
            self.dossier.RDVFixe = True
            self.dossier.datesignature = self.ui.dateRDV.dateTime().toPython()
        else:
            self.dossier.RDVFixe = False

        self.session.commit()
        self.mySignal.emit(self.index, self.dossier)

    def statuslogic(self):
        if self.ui.provanceDrop.currentText() == "Agence":
            self.dossier.statusDossier = "En cours"
        elif self.ui.provanceDrop.currentText() =="Autre":
            if self.dossier.statusDossier == "PUV en préparation" \
                    and self.ui.statusAvantContratComb.currentText() == "OK":
                self.dossier.statusDossier = "SRU à traiter"
            elif self.dossier.statusDossier == "SRU à traiter" \
                    and self.ui.statusSRU.currentText() == "OK" \
                    and self.ui.checkboxDossierRdy.checkState() == QtCore.Qt.Unchecked:
                self.dossier.statusDossier = "Dossier à constituer"
            elif self.dossier.statusDossier == "Dossier à constituer" \
                    and self.ui.checkboxDossierRdy.checkState() == QtCore.Qt.Checked \
                    and self.ui.besoinpret.currentText() !='Non':
                self.dossier.statusDossier = "En Attente ODP"
            elif self.dossier.statusDossier == "Dossier à constituer" \
                    and self.ui.checkboxDossierRdy.checkState() == QtCore.Qt.Checked \
                    and self.ui.besoinpret.currentText() == 'Non' \
                    and self.ui.RDVFixe.checkState() == QtCore.Qt.Unchecked:
                self.dossier.statusDossier = "RDV à fixer"
            elif self.dossier.statusDossier == "En Attente ODP" and self.ui.statusODP.currentText() =='Reçu' \
                    and self.ui.RDVFixe.checkState() == QtCore.Qt.Unchecked:
                self.dossier.statusDossier = "RDV à fixer"
            elif self.ui.RDVFixe.checkState() == QtCore.Qt.Checked:
                self.dossier.statusDossier = "Vente à rédiger"

    def populatetodotable(self):
        self.viewtododossier = self.ui.findChild(QTableView, "viewtododossier")
        self.model = taskInDossier.allTodoTableViewInDossier(self.dossier.todoactions)
        self.viewtododossier.setModel(self.model)
        self.viewtododossier.resizeColumnsToContents()

        delegateTask = viewdelegates.PushButtonDelegate(self.viewtododossier)
        self.viewtododossier.setItemDelegateForColumn(4, delegateTask)
        delegateTask.clicked.connect(self.updatetasks)

    def addnewbuttonactionreturn(self,todo):
        self.model.appendtask(todo)
        self.mySignalForNewtask.emit(todo)

    def addnewbuttonaction(self):
        self.createTaskTodo = createTaskV2Todo.CreateTaskV2Todo(self, self.dossier, self.session, None)
        self.createTaskTodo.addsignal.connect(self.addnewbuttonactionreturn)
        self.createTaskTodo.ui.show()

    def updatetasks(self, index):
        if index.isValid():
            todo = self.session.query(Todoelement).get(index.model().mydata.item(index.row(), 0).data(QtCore.Qt.DisplayRole))
            todo.status = 'Réalisée'
            self.session.commit()
            self.updatetodo(todo, index)

    def updatetodo(self,todo, index):
        self.model.updateatask(index,todo)
        self.model.layoutChanged.emit()
        self.mySignalFortasksUpdate.emit(index, todo)
