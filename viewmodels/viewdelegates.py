from PySide2 import QtCore,  QtWidgets

class PushButtonDelegate(QtWidgets.QStyledItemDelegate):
    clicked = QtCore.Signal(QtCore.QModelIndex)

    def paint(self, painter, option, index):
        if (
            isinstance(self.parent(), QtWidgets.QAbstractItemView)
            and self.parent().model() is index.model()
        ):
            self.parent().openPersistentEditor(index)

    def createEditor(self, parent, option, index):
        button = QtWidgets.QPushButton(parent)
        button.clicked.connect(lambda *args, ix=index: self.clicked.emit(ix))
        return button

    def setEditorData(self, editor, index):
        editor.setText(index.data(QtCore.Qt.DisplayRole))

    def setModelData(self, editor, model, index):
        pass