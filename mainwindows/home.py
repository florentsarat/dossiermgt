
from PySide2 import QtCore
from PySide2.QtWidgets import  QMainWindow, QPushButton, QTableView

from datamodel.models import dossier, todoRDV

from viewmodels import viewModels as viewModels, viewdelegates as viewdelegates

from forms import createdossierForm, createRDVTodo,editdossierForm

from PySide2.QtUiTools import loadUiType


class Home(QMainWindow, loadUiType('UI/TestFlo.ui')[0]):
    def __init__(self, session):
        super(Home, self).__init__()
        self.session = session
        self.setupUi(self)
        self.dossiers = []
        self.myRDVTodos =[]

        self.button = self.findChild(QPushButton, "addNewCase")
        self.button.clicked.connect(self.clickedNewDossierBtn)

        # Get tables
        self.mydossiersTable = self.findChild(QTableView,"tabledesdossiers")
        self.myrdvtable = self.findChild(QTableView, 'listedeRDV')

        # Load Data
        self.loadRDV()
        self.loadDossier()

        # Create Models
        self.modelRDV = viewModels.rdvTableView(self.myRDVTodos)
        self.model = viewModels.dossiersTableView(self.dossiers)

        # Bind models
        self.myrdvtable.setModel(self.modelRDV)
        self.mydossiersTable.setModel(self.model)
        self.mydossiersTable.resizeColumnsToContents()

        delegateCreateRDV = viewdelegates.PushButtonDelegate(self.mydossiersTable)
        self.mydossiersTable.setItemDelegateForColumn(10, delegateCreateRDV)
        delegateCreateRDV.clicked.connect(self.handleRDVCreateClicked)

        delegateEditDossier = viewdelegates.PushButtonDelegate(self.mydossiersTable)
        self.mydossiersTable.setItemDelegateForColumn(9, delegateEditDossier)
        delegateEditDossier.clicked.connect(self.handleEditdossierClicked)

        delegateRDVpris = viewdelegates.PushButtonDelegate(self.myrdvtable)
        self.myrdvtable.setItemDelegateForColumn(7, delegateRDVpris)
        delegateRDVpris.clicked.connect(self.markRDVasDone)

        self.show()

    def handleEditdossierClicked(self, index):
        self.CreateForm = editdossierForm.EditForm(self,self.session)
        self.CreateForm.show()

    def markRDVasDone(self, index):
        if index.isValid():
            if (index.model().mydata.item(index.row(), 6).data(QtCore.Qt.DisplayRole)) !='Pris':
                rdv = self.session.query(todoRDV).get(index.model().mydata.item(index.row(), 0).data(QtCore.Qt.DisplayRole))
                rdv.status = 'Pris'
                self.session.commit()
                self.updateRDVList()
            else:
                pass

    def handleRDVCreateClicked(self, index):
        if index.isValid():
            self.CreateRDVTodo = createRDVTodo.CreateRDVTodo(self, self.session.query(dossier).get(index.model().mydata.item(index.row(), 0).data(QtCore.Qt.DisplayRole)), self.session)
            self.CreateRDVTodo.addsignal.connect(self.updateRDVList)
            self.CreateRDVTodo.show()

    def clickedNewDossierBtn(self):
        self.NewForm = createdossierForm.CreateForm(self,self.session)
        self.NewForm.mySignal.connect(self.updatelist)
        self.NewForm.show()

    def updatelist(self):
        self.loadDossier()
        self.model.getData(self.dossiers)
        self.model.layoutChanged.emit()

    def updateRDVList(self):
        self.loadRDV()
        self.modelRDV.getData(self.myRDVTodos)
        self.modelRDV.layoutChanged.emit()

    def loadDossier(self):
        self.dossiers = self.session.query(dossier).all()

    def loadRDV(self):
        self.myRDVTodos = self.session.query(todoRDV).all()
