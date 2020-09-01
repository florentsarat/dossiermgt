from PySide2 import QtCore, QtGui
from PySide2.QtCore import Qt,QAbstractTableModel, QDate
from PySide2.QtGui import QBrush

class dossiersTableView(QAbstractTableModel):
    def __init__(self, datain, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.mydata = QtGui.QStandardItemModel(0, 3)
        self.getData(datain)
        self.header = ['ID','Dossier', 'Type','Provenance', 'Statut Avant Contrat', 'Notaire Revendeur', 'Notaire Acquéreur', 'Statut', 'Date','' , '']

    def getData(self, datain):
        if datain is not None:
            self.datain = datain
        self.mydata.clear()
        for dossier in self.datain:

            dossierID = QtGui.QStandardItem()
            dossierID.setData(dossier.id, QtCore.Qt.DisplayRole)

            dossiername = QtGui.QStandardItem()
            dossiername.setData(dossier.nameDossier, QtCore.Qt.DisplayRole)

            dossiertype = QtGui.QStandardItem()
            dossiertype.setData(dossier.typeDossier, QtCore.Qt.DisplayRole)

            dossierprovenance = QtGui.QStandardItem()
            dossierprovenance.setData(dossier.dossierprovenance, QtCore.Qt.DisplayRole)

            statusavantContrat = QtGui.QStandardItem()
            statusavantContrat.setData(dossier.statusavantContrat, QtCore.Qt.DisplayRole)

            notairevendeurDossier = QtGui.QStandardItem()
            notairevendeurDossier.setData(dossier.notairevendeurDossier, QtCore.Qt.DisplayRole)

            notaireacquereurDossier = QtGui.QStandardItem()
            notaireacquereurDossier.setData(dossier.notaireacquereurDossier, QtCore.Qt.DisplayRole)

            dossierstatus = QtGui.QStandardItem()
            dossierstatus.setData(dossier.statusDossier, QtCore.Qt.DisplayRole)

            dossierdate = QtGui.QStandardItem()
            dossierdate.setData(dossier.dateDossier, QtCore.Qt.DisplayRole)

            dossierdate = QtGui.QStandardItem()
            dossierdate.setData(dossier.dateDossier, QtCore.Qt.DisplayRole)

            editAction = QtGui.QStandardItem()
            editAction.setData('Editer', QtCore.Qt.DisplayRole)

            actionbutton = QtGui.QStandardItem()
            actionbutton.setData('+RDV', QtCore.Qt.DisplayRole)

            self.mydata.appendRow([dossierID, dossiername, dossiertype, dossierprovenance, statusavantContrat, notairevendeurDossier, notaireacquereurDossier, dossierstatus, dossierdate, editAction,actionbutton])

    def rowCount(self, index):
        return self.mydata.rowCount()

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == 8:
                return QDate(self.mydata.item(index.row(), index.column()).data(QtCore.Qt.DisplayRole))
            else:
                return self.mydata.item(index.row(), index.column()).data(QtCore.Qt.DisplayRole)

    def columnCount(self, index):
        # if self.mydata is None:
            return len(self.header)
        # else:
        #     return 6

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[section]


class rdvTableView(QAbstractTableModel):
    def __init__(self, rdvData, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.mydata = QtGui.QStandardItemModel(0, 3)
        self.getData(rdvData)


    def getData(self, rdvdatain):
        if rdvdatain is not None:
            self.rdvData = rdvdatain
        else :
            pass
        self.mydata.clear()
        for rdv in self.rdvData:

            rdvID = QtGui.QStandardItem()
            rdvID.setData(rdv.id, QtCore.Qt.DisplayRole)

            rdvname = QtGui.QStandardItem()
            rdvname.setData(rdv.name, QtCore.Qt.DisplayRole)

            rdvdossier = QtGui.QStandardItem()
            rdvdossier.setData(rdv.dossier.nameDossier, QtCore.Qt.DisplayRole)

            rdvdatelim = QtGui.QStandardItem()
            rdvdatelim.setData(rdv.datelimit, QtCore.Qt.DisplayRole)

            rdvavec = QtGui.QStandardItem()
            rdvavec.setData(rdv.avec, QtCore.Qt.DisplayRole)

            rdvtype = QtGui.QStandardItem()
            rdvtype.setData(rdv.typedeRDV, QtCore.Qt.DisplayRole)

            rdvstatus = QtGui.QStandardItem()
            rdvstatus.setData(rdv.status, QtCore.Qt.DisplayRole)

            rdvIsdone = QtGui.QStandardItem()
            rdvIsdone.setData('RDV Pris', QtCore.Qt.DisplayRole)

            self.mydata.appendRow([rdvID, rdvname, rdvdossier, rdvdatelim, rdvavec, rdvtype, rdvstatus, rdvIsdone])


    def rowCount(self, index):
        return self.mydata.rowCount()

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == 3:
                return QDate(self.mydata.item(index.row(), index.column()).data(QtCore.Qt.DisplayRole))
            else :
                return self.mydata.item(index.row(), index.column()).data(QtCore.Qt.DisplayRole)
        if role == Qt.BackgroundRole:
            if self.mydata.item(index.row(), 6).data(QtCore.Qt.DisplayRole)== "Pris":
                return QBrush(Qt.darkGreen)
            else:
                return QBrush(Qt.white)

    def columnCount(self, index):
        if self.mydata is None:
            return len(self.mydata.item(0))
        else:
            return 8

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        header = ['ID','RDV Name', 'Dossier', 'Date limite', 'Avec', 'Type de RDV', 'Status', '']
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return header[section]