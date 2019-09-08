'''Viewer module
'''
# ------------------------------------------------------------------------------
# IMPORTS
# ------------------------------------------------------------------------------
import sys
from PyQt5.QtGui import QIcon, QTextOption
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QDialog,
    QTextEdit,
    QHeaderView,
    QVBoxLayout,
    QHBoxLayout,
    QApplication,
    QTableWidget,
    QTableWidgetItem,
    QDialogButtonBox,
    QAbstractItemView,
)
# ------------------------------------------------------------------------------
# CLASSES
# ------------------------------------------------------------------------------
class ItemDetailsDialog(QDialog):
    '''[summary]
    '''
    def __init__(self, text):
        '''Constructor
        '''
        super().__init__()
        self._title = 'Item Details'
        self._text = text
        self._left = 10
        self._top = 10
        self._width = 640
        self._height = 480
        self._details = QTextEdit()
        self._button_box = QDialogButtonBox()
        self._layout = QVBoxLayout()
        self.init_ui()

    def init_ui(self):
        '''Initialize user interface
        '''
        self.setWindowTitle(self._title)
        self.setGeometry(self._left, self._top, self._width, self._height)
        self._layout.addWidget(self._details)
        self._layout.addWidget(self._button_box)
        self._details.setReadOnly(True)
        self._details.setPlainText(self._text)
        self._details.setWordWrapMode(QTextOption.WordWrap)
        self._details.setLineWrapMode(QTextEdit.WidgetWidth)
        self._button_box.addButton(QDialogButtonBox.Close)
        self._button_box.rejected.connect(self.accept)
        self.setLayout(self._layout)

class QueryResultViewer(QWidget):
    '''Query Result Viewer
    '''
    def __init__(self):
        '''Constructor
        '''
        super().__init__()
        self._title = 'Timeline Explorer'
        self._left = 10
        self._top = 10
        self._width = 640
        self._height = 480
        self._table = QTableWidget()
        self._row_count = QLabel()
        self._button_box = QDialogButtonBox()
        self._hlayout = QHBoxLayout()
        self._layout = QVBoxLayout()
        self.init_ui()

    def init_ui(self):
        '''Initialize user interface
        '''
        self.setWindowTitle(self._title)
        self.setGeometry(self._left, self._top, self._width, self._height)
        self._layout.addWidget(self._table)
        self._hlayout.addWidget(self._row_count)
        self._hlayout.addStretch()
        self._hlayout.addWidget(self._button_box)
        self._layout.addLayout(self._hlayout)
        self.setLayout(self._layout)
        self._button_box.addButton(QDialogButtonBox.Close)
        self._button_box.rejected.connect(self.close)
        self._table.doubleClicked.connect(self.display_item_details)
        self.show()

    def reset(self):
        '''Clear the table
        '''
        self._table.clear()

    def display(self, headers, row_gen):
        '''Refresh the table
        '''
        self.reset()
        self._table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._table.setSortingEnabled(True)
        self._table.setSelectionMode(QAbstractItemView.SingleSelection)
        self._table.setSelectionBehavior(QAbstractItemView.SelectItems)
        self._table.setColumnCount(len(headers))
        self._table.setHorizontalHeaderLabels(headers)
        self._table.verticalHeader().setVisible(False)
        tbl_headers = self._table.horizontalHeader()
        for k in range(len(tbl_headers)):
            if k == len(tbl_headers)-1:
                tbl_headers.setSectionResizeMode(k, QHeaderView.Stretch)
            else:
                tbl_headers.setSectionResizeMode(k, QHeaderView.Interactive)
        for row in row_gen:
            self._table.insertRow(self._table.rowCount())
            col_idx = 0
            row_idx = self._table.rowCount() - 1
            for col in row:
                self._table.setItem(row_idx, col_idx, QTableWidgetItem(col))
                col_idx += 1
        self._table.sortByColumn(0, Qt.AscendingOrder)
        self._row_count.setText(f'{self._table.rowCount()} rows')

    @pyqtSlot()
    def display_item_details(self):
        print("\n")
        for currentQTableWidgetItem in self._table.selectedItems():
            dialog = ItemDetailsDialog(currentQTableWidgetItem.text())
            dialog.exec_()
            break
# ------------------------------------------------------------------------------
# FUNCTIONS
# ------------------------------------------------------------------------------
def spawn_viewer(headers, row_gen, qapp_args=None):
    '''[summary]
    '''
    if not qapp_args:
        qapp_args = [sys.argv[0]]
    app = QApplication(qapp_args)
    viewer = QueryResultViewer()
    viewer.display(headers, row_gen)
    return app.exec_()
