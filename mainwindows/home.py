from PySide2 import QtCore
from PySide2.QtWidgets import QMainWindow, QPushButton, QTableView, QCheckBox
from PySide2.QtUiTools import QUiLoader

from datamodel.models import Dossier, Todoelement

from viewmodels import mainTaskView, mainDossierView, viewdelegates as viewdelegates

from forms import createdossierForm, createTaskV2Todo, editdossierForm, aboutform

from customclasses.multifilterproxymodel import MultiFilterProxyModel
import resources


class Home(QMainWindow):

    def __init__(self, session):
        super(Home, self).__init__()

        ui_file =":UI\\UI\\mainwindow.ui"
        # ui_file = "UI\\mainwindow.ui"
        ui_file = QtCore.QFile(ui_file)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        self.session = session

        self.dossiers = []
        self.mytasksTodos = []

        self.ui.button = self.ui.findChild(QPushButton, "addNewCase")
        self.ui.button.clicked.connect(self.clickednewdossierbtn)

        self.ui.checkboxOldDossier = self.ui.findChild(QCheckBox, "checkboxdisplayClosDossier")
        self.ui.checkboxOldDossier.stateChanged.connect(self.displayolddossier)

        self.ui.searchbutton = self.ui.findChild(QPushButton, 'searchbutton')
        self.ui.searchbutton.clicked.connect(self.searchfordossier)

        self.ui.doatasksearch.clicked.connect(self.searchfortask)

        self.ui.statusfiltertask.currentIndexChanged.connect(self.filterbystatus)

        self.ui.searchcontent.returnPressed.connect(self.searchfordossier)

        self.ui.mytabs.currentChanged.connect(self.managemangeTab)

        self.ui.menuA_propos.triggered.connect(self.displayabout)

        self.setdossiertable()
        self.settasktable()
        self.manageprogressbar()
        self.ui.showMaximized()
        # self.ui.show()

    def managemangeTab(self):
        if self.ui.mytabs.currentIndex()== 0:
            self.ui.searchcontent.returnPressed.connect(self.searchfordossier)
        else:

            self.ui.recherchetaskvalue.returnPressed.connect(self.searchfortask)

    ###########################
    # Dossiers
    ###########################

    def load_dossier(self):
        self.dossiers = self.session.query(Dossier).all()

    # Filters
    def searchfordossier(self):
        self.sortermodelDossier.setFilterByColumn(1, ".*" + self.ui.searchcontent.text())

    def displayolddossier(self, state):
        if state == QtCore.Qt.Checked:
            self.sortermodelDossier.setFilterByColumn(9, "")
        else:
            self.sortermodelDossier.setFilterByColumn(9, "^(?!Clos).*")

    def applyfilter(self):
        self.searchfordossier()
        if self.ui.checkboxOldDossier.checkState() == QtCore.Qt.Checked:
            self.sortermodelDossier.setFilterByColumn(9, "")
        else:
            self.sortermodelDossier.setFilterByColumn(9, "^(?!Clos).*")

    # Actions
    def clickednewdossierbtn(self):
        self.NewForm = createdossierForm.CreateForm(self, self.session)
        self.NewForm.mySignal.connect(self.updatewhenaddnewdossier)
        self.NewForm.ui.show()

    def handleeditdossierclicked(self, index):
        if index.isValid():
            mydossier = self.session.query(Dossier).get(
                index.model().sourceModel().mydata.item(index.row(), 0).data(QtCore.Qt.DisplayRole))
            self.EditForm = editdossierForm.EditForm(self, self.session, mydossier, index)
            self.EditForm.ui.show()
            self.EditForm.mySignal.connect(self.updatelistwhenedit)
            self.EditForm.mySignalFortasksUpdate.connect(self.updateforedittask)
            self.EditForm.mySignalForNewtask.connect(self.appendtask)

    def handlertaskcreateclicked(self, index):
        if index.isValid():
            self.CreateRDVTodo = createTaskV2Todo.CreateTaskV2Todo(self,
                                                                   self.session.query(Dossier).get(
                                                                       index.model().sourceModel().mydata.item(
                                                                           index.row(), 0).data(QtCore.Qt.DisplayRole)),
                                                                   self.session,
                                                                   index)
            self.CreateRDVTodo.addsignal.connect(self.appendtask)
            self.CreateRDVTodo.ui.show()

    # Display
    def setdossiertable(self):
        self.mydossiersTable = self.ui.findChild(QTableView, "tabledesdossiers")
        self.load_dossier()

        self.model = mainDossierView.DossiersTableView(self.dossiers)

        self.sortermodelDossier = MultiFilterProxyModel(self)
        self.sortermodelDossier.setSourceModel(self.model)

        self.mydossiersTable.setModel(self.sortermodelDossier)

        self.mydossiersTable.setSortingEnabled(True)
        self.mydossiersTable.sortByColumn(0, QtCore.Qt.AscendingOrder)

        self.applyfilter()

        self.mydossiersTable.resizeColumnsToContents()

        delegateCreateRDV = viewdelegates.PushButtonDelegate(self.mydossiersTable)
        self.mydossiersTable.setItemDelegateForColumn(16, delegateCreateRDV)
        delegateCreateRDV.clicked.connect(self.handlertaskcreateclicked)

        delegateEditDossier = viewdelegates.PushButtonDelegate(self.mydossiersTable)
        self.mydossiersTable.setItemDelegateForColumn(15, delegateEditDossier)
        delegateEditDossier.clicked.connect(self.handleeditdossierclicked)

    def updatewhenaddnewdossier(self, dossiertoadd):
        self.sortermodelDossier.sourceModel().appenddossier(dossiertoadd)
        self.mydossiersTable.resizeColumnsToContents()

    def updatelistwhenedit(self, index, dossiertodupdate):
        self.sortermodelDossier.sourceModel().updateadossier(index, dossiertodupdate)
        self.mydossiersTable.resizeColumnsToContents()

    ###########################
    # Tasks
    ###########################

    def load_tasks(self):
        self.mytasksTodos = self.session.query(Todoelement).all()

    def getTaskKPI(self):
        self.totalnboftask = self.session.query(Todoelement).count()
        self.nbtaskstodo = self.session.query(Todoelement).filter(Todoelement.status == 'A Faire').count()


    # Filter
    def searchfortask(self):
        self.sortermodeltask.setFilterByColumn(1, ".*" +self.ui.recherchetaskvalue.text())

    def filterbystatus(self):
        if self.ui.statusfiltertask.currentText() == "Tous":
            self.sortermodeltask.setFilterByColumn(4, "")
        elif self.ui.statusfiltertask.currentText() == "A Faire":
            self.sortermodeltask.setFilterByColumn(4, "A Faire")
        elif self.ui.statusfiltertask.currentText() == "Réalisée":
            self.sortermodeltask.setFilterByColumn(4, "Réalisée")

    def applyfilterfortasks(self):
        self.searchfortask()
        if self.ui.statusfiltertask.currentText() == "Tous":
            self.sortermodeltask.setFilterByColumn(4, "")
        elif self.ui.statusfiltertask.currentText() == "A Faire":
            self.sortermodeltask.setFilterByColumn(4, "A Faire")
        elif self.ui.statusfiltertask.currentText() == "Réalisée":
            self.sortermodeltask.setFilterByColumn(4, "Réalisée")

    # Actions
    def marktaskasdone(self, index):
        if index.isValid():
            mytask = self.session.query(Todoelement).get(index.row() + 1)
            mytask.status = 'Réalisée'
            self.session.commit()
            self.updateTasklistwhenedit(index, mytask)
            self.getTaskKPI()
            self.manageprogressbar()

    # Display
    def settasktable(self):
        self.mytasktable = self.ui.findChild(QTableView, 'listedeRDV')

        self.mytasktable.setSortingEnabled(True)

        self.load_tasks()
        self.getTaskKPI()
        self.manageprogressbar()

        self.modeltasks = mainTaskView.TaskTableView(self.mytasksTodos)

        self.sortermodeltask = MultiFilterProxyModel(self)
        self.sortermodeltask.setSourceModel(self.modeltasks)

        self.mytasktable.setModel(self.sortermodeltask)

        self.applyfilterfortasks()

        self.mytasktable.resizeColumnsToContents()

        delegatetaskpris = viewdelegates.PushButtonDelegate(self.mytasktable)
        self.mytasktable.setItemDelegateForColumn(5, delegatetaskpris)
        delegatetaskpris.clicked.connect(self.marktaskasdone)

    def manageprogressbar(self):
        self.ui.TacheEnCours.display(self.nbtaskstodo)
        if self.nbtaskstodo > 10:
            self.ui.TacheEnCours.setStyleSheet("QLCDNumber { background-color: red }")
        elif self.nbtaskstodo > 5:
            self.ui.TacheEnCours.setStyleSheet("QLCDNumber { background-color: yellow }")
        else:
            self.ui.TacheEnCours.setStyleSheet("QLCDNumber { background-color: green }")

    def updateTasklistwhenedit(self, index, tasktoupdate):
        self.sortermodeltask.sourceModel().updateatask(index, tasktoupdate)

    def updateforedittask(self):
        self.load_tasks()
        self.mytasktable.model().sourceModel().resetdata(self.mytasksTodos)
        self.getTaskKPI()
        self.manageprogressbar()

    def appendtask(self, tasktoadd):
        self.sortermodeltask.sourceModel().appendtask(tasktoadd)
        self.mytasktable.resizeColumnsToContents()
        self.getTaskKPI()
        self.manageprogressbar()

    ###########################
    # About
    ###########################

    def displayabout(self):
        print('here')
        self.aboutform = aboutform.aboutForm(self)
        self.aboutform.ui.show()
