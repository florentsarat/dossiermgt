from PySide2 import QtCore
from PySide2.QtWidgets import QMainWindow, QPushButton, QTableView, QCheckBox
from PySide2.QtUiTools import loadUiType,QUiLoader

from datamodel.models import Dossier, TodoRDV, Todoelement

from viewmodels import viewModels as viewModels, viewdelegates as viewdelegates

from forms import createdossierForm, createTaskV2Todo,editdossierForm, createTaskTodo

from customclasses.multifilterproxymodel import MultiFilterProxyModel
import ressources


class Home(QMainWindow):

    def __init__(self, session):
        super(Home, self).__init__()

        # ui_file =":UI\\UI\\TestFlo.ui"
        ui_file = "UI\\TestFlo.ui"
        ui_file = QtCore.QFile(ui_file)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        self.session = session

        self.dossiers = []
        self.mytasksTodos =[]

        self.ui.button = self.ui.findChild(QPushButton, "addNewCase")
        self.ui.button.clicked.connect(self.clickednewdossierbtn)

        self.ui.checkboxOldDossier = self.ui.findChild(QCheckBox, "checkboxdisplayClosDossier")
        self.ui.checkboxOldDossier.stateChanged.connect(self.displayolddossier)

        self.ui.searchbutton = self.ui.findChild(QPushButton, 'searchbutton')
        self.ui.searchbutton.clicked.connect(self.searchfordossier)

        self.ui.searchcontent.returnPressed.connect(self.searchfordossier)

        self.setdossiertable()
        self.settasktable()
        self.ui.showMaximized()
        # self.ui.show()

    ###########################
    # Dossiers
    ###########################

    def load_dossier(self):
        self.dossiers = self.session.query(Dossier).all()

    # Filters

    def searchfordossier(self):
        self.sortermodelDossier.setFilterByColumn(1, self.ui.searchcontent.text())

    def displayolddossier(self,state):
        if state == QtCore.Qt.Checked:
            self.sortermodelDossier.setFilterByColumn(9, "")
        else:
            self.sortermodelDossier.setFilterByColumn(9, "^(?!Clos).*")

    # Actions

    def clickednewdossierbtn(self):
        self.NewForm = createdossierForm.CreateForm(self,self.session)
        self.NewForm.mySignal.connect(self.updatewhenaddnewdossier)
        self.NewForm.ui.show()

    def handleeditdossierclicked(self, index):
        if index.isValid():

            mydossier = self.session.query(Dossier).get(index.model().sourceModel().mydata.item(index.row(), 0).data(QtCore.Qt.DisplayRole))
            self.EditForm = editdossierForm.EditForm(self,self.session, mydossier, index)
            self.EditForm.ui.show()
            self.EditForm.mySignal.connect(self.updatelistwhenedit)

    def handletaskdossierclicked(self, index):
        if index.isValid():
            self.createTaskTodo = createTaskTodo.CreateTaskTodo(self,
                                                                self.session.query(Dossier).get(index.model().sourceModel().mydata.item(index.row(), 0).data(QtCore.Qt.DisplayRole)),
                                                                self.session
                                                                )
            self.createTaskTodo.addsignal.connect(self.updatetasklist)
            self.createTaskTodo.ui.show()

    def handlerdvcreateclicked(self, index):
        if index.isValid():
            self.CreateRDVTodo = createTaskV2Todo.CreateTaskV2Todo(self,
                                                                   self.session.query(Dossier).get(index.model().sourceModel().mydata.item(index.row(), 0).data(QtCore.Qt.DisplayRole)),
                                                                   self.session,
                                                                   index)
            self.CreateRDVTodo.addsignal.connect(self.appendtask)
            self.CreateRDVTodo.ui.show()

    # Display

    def setdossiertable(self):
        self.mydossiersTable = self.ui.findChild(QTableView, "tabledesdossiers")
        self.load_dossier()

        self.model = viewModels.DossiersTableView(self.dossiers)

        self.sortermodelDossier = MultiFilterProxyModel(self)
        self.sortermodelDossier.setSourceModel(self.model)

        self.mydossiersTable.setModel(self.sortermodelDossier)

        self.mydossiersTable.setSortingEnabled(True)
        self.mydossiersTable.sortByColumn(0, QtCore.Qt.AscendingOrder)

        self.applyfilter()

        self.mydossiersTable.resizeColumnsToContents()

        delegateCreateRDV = viewdelegates.PushButtonDelegate(self.mydossiersTable)
        self.mydossiersTable.setItemDelegateForColumn(16, delegateCreateRDV)
        delegateCreateRDV.clicked.connect(self.handlerdvcreateclicked)

        delegateEditDossier = viewdelegates.PushButtonDelegate(self.mydossiersTable)
        self.mydossiersTable.setItemDelegateForColumn(15, delegateEditDossier)
        delegateEditDossier.clicked.connect(self.handleeditdossierclicked)

        delegateTaskDossier = viewdelegates.PushButtonDelegate(self.mydossiersTable)
        self.mydossiersTable.setItemDelegateForColumn(17, delegateTaskDossier)
        delegateTaskDossier.clicked.connect(self.handletaskdossierclicked)

    def updatewhenaddnewdossier(self, dossiertoadd):
        self.sortermodelDossier.sourceModel().appenddossier(dossiertoadd)

    def updatelistwhenedit(self, index, dossiertodupdate):
        self.sortermodelDossier.sourceModel().updateadossier(index,dossiertodupdate)
        # self.updatelayout()

    def applyfilter(self):
        self.searchfordossier()
        if self.ui.checkboxOldDossier.checkState() == QtCore.Qt.Checked:
            self.sortermodelDossier.setFilterByColumn(9, "")
        else:
            self.sortermodelDossier.setFilterByColumn(9, "^(?!Clos).*")

    ###########################
    # RDV
    ###########################

    def load_tasks(self):
        self.mytasksTodos = self.session.query(Todoelement).all()

    def settasktable(self):
        self.mytasktable = self.ui.findChild(QTableView, 'listedeRDV')
        self.load_tasks()

        self.modeltasks = viewModels.TaskTableView(self.mytasksTodos)

        self.sortermodeltask = MultiFilterProxyModel(self)
        self.sortermodeltask.setSourceModel(self.modeltasks)

        self.mytasktable.setModel(self.sortermodeltask)

        self.mytasktable.setSortingEnabled(True)

        self.mytasktable.sortByColumn(0, QtCore.Qt.AscendingOrder)

        self.mytasktable.resizeColumnsToContents()

        delegatetaskpris = viewdelegates.PushButtonDelegate(self.mytasktable)
        self.mytasktable.setItemDelegateForColumn(5, delegatetaskpris)
        delegatetaskpris.clicked.connect(self.marktaskasdone)

    def marktaskasdone(self, index):
        if index.isValid():
            print('my base index is ' + str(index.row()))
            print('based on base index ' + str(self.session.query(Todoelement).get(index.row()+1).id))
            print('based on mapTo index ' + str(self.session.query(Todoelement).get(index.model().mapToSource(index).row() + 1).id))

            mytask = self.session.query(Todoelement).get(index.model().sourceModel().mydata.item(index.row(), 0).data(QtCore.Qt.DisplayRole))
            print(mytask.id)
            # print('based on mapFrom index ' + str(self.session.query(Todoelement).get(index.model().mapFromSource(index).row() + 1).id))
            if (index.model().sourceModel().mydata.item(index.row(), 5).data(QtCore.Qt.DisplayRole)) !='Réalisée':
                taskID = index.model().sourceModel().mydata.item(index.row(), 0)
                # print(index.model().mapToSource(index))
                # print(index.model().mapToSource(index))
                # print(index)
                if index.model().mapToSource(index).isValid():
                    taskID= index.model().mapToSource(index).row()+1
                else:
                    taskID = index.row()+1
                # print(taskID)
                task = self.session.query(Todoelement).get(taskID)
                # print(index.model().sourceModel().mydata.item(index.model().sourceModel(), 0))
                # print(taskID)
                print('my taski id is ' + str(task.id))
                print('==========================')
                # if index.model().mapToSource(index).isValid():
                #     print('ok')
                # task = self.session.query(Todoelement).get(index.model().sourceModel().mydata.item(index.row(), 0).data(QtCore.Qt.DisplayRole))
                # print(task.id)
                # task.status = 'Réalisée'
                self.session.commit()
                self.updateTasklistwhenedit(task, index)
                # self.modeltasks.layoutChanged.emit()
            else:
                pass

    def updateTasklistwhenedit(self, index, dossiertodupdate):
        self.sortermodeltask.sourceModel().updateatask(index,dossiertodupdate)

    def updatetasklist(self):
        pass

    def appendtask(self, tasktoadd):
        self.sortermodeltask.sourceModel().appendtask(tasktoadd)
