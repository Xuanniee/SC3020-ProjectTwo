from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QTableView, QGridLayout
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import Qt, QModelIndex
import pandas as pd
from Database.database import Database
import sys


class TupleWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self, relationName, rOut, blockNum):
        super().__init__()
        self.setWindowTitle("TUPLES IN THE BLOCK")
        self.allRelations = relationName
        self.bNo = blockNum
        self._rOut = rOut
        
        # self.AllRelations = []
        layout = QVBoxLayout()
        
        
            #get data from the getAllTuplesByBlockNumber() using the database
            # data = [
            #     {'First Name': 'John', 'Last Name': 'Doe', 'Age': 25},
            #     {'First Name': 'Jane', 'Last Name': 'Doe', 'Age': 22},
            #     {'First Name': 'Alice', 'Last Name': 'Doe', 'Age': 22},
            #     {'First Name': 'Jane', 'Last Name': 'Lim', 'Age': 24}
            # ]
        data = DataRetriever().getTuples(self.allRelations, blockNum)
            #if that relation doesnt has that block number --> skip
        for i in range(len(self.allRelations)):
            if data[self.allRelations[i]]:
                df1 = pd.DataFrame(data[self.allRelations[i]])
                print("df1", df1)
                df2 = pd.DataFrame(self._rOut)
                print("df2", df2)
                merged = pd.merge(df1, df2, how='inner')
                indices = df1[df1.isin(merged.to_dict('list')).all(axis=1)].index.tolist()
                print("indices: ",indices)

                model = TupleTable(data[self.allRelations[i]], indices)
                # # set color
                # model.setRowColor(row, (Qt.GUI.QColor(255, 0, 0, 127) or (0,0,0,127)) 
                table = QTableView()
                table.setModel(model)
                label = QLabel("Relation "+ self.allRelations[i], alignment = Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(label)
                layout.addWidget(table)
            
        self.setLayout(layout)

class TupleTable(QtCore.QAbstractTableModel):
    def __init__(self, data, condition):
        '''colorArr: index is the row no and value is 1/0'''
        super(TupleTable, self).__init__()
        df = pd.DataFrame(data)
        self._data = df
        self.filterCond = condition
        '''filterTuples will be a list of tuples in each block for scans but for others it will just be the row number'''
    
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)
        if role == Qt.ItemDataRole.BackgroundRole:
            # row = index.row()
            print(self.filterCond)
            row = index.row()
            if self.filterCond == None:
                return QtGui.QColor(255, 255, 255)
            if self.filterCond and row in self.filterCond:
                return QtGui.QColor(255, 0, 0, 127)
            else:
                return QtGui.QColor(0, 0, 0, 127)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])
    
    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        # Update the data in your model
        # Example: updating the data at the specified index
        if role == Qt.ItemDataRole.EditRole:
            self._data.iloc[index.row()][index.column()] = value
            return True
        return False
    
    def setRowColor(self, row, color):
        self.colors[row] = color
        # Notify the view that data has changed for the given role
        self.dataChanged.emit(self.index(row, 0), self.index(row, self.columnCount(None) - 1), [Qt.ItemDataRole.BackgroundRole])

class BlockTable(QtCore.QAbstractTableModel):
    #pandas dataframe
    def __init__(self, data, condition):
        super(BlockTable, self).__init__()
        # data = pd.read_csv('')
        df = pd.DataFrame(data)
        self._data = df
        self.filterCond = condition

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)
        if role == Qt.ItemDataRole.BackgroundRole:
            # row = index.row()
            print(self.filterCond)
            row = index.row()
            if self.filterCond == None:
                return QtGui.QColor(255, 255, 255)
            if self.filterCond and row in self.filterCond:
                return QtGui.QColor(255, 0, 0, 127)
            else:
                return QtGui.QColor(0, 0, 0, 127)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])
            
    # Method to set data in the model
    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        # Update the data in your model
        # Example: updating the data at the specified index
        if role == Qt.ItemDataRole.EditRole:
            self._data.iloc[index.row()][index.column()] = value
            return True
        return False

class OutTable(QtCore.QAbstractTableModel):
    #pandas dataframe
    def __init__(self, data):
        super(OutTable, self).__init__()
        # data = pd.read_csv('')
        df = pd.DataFrame(data)
        self._data = df

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)
        # if role == Qt.ItemDataRole.BackgroundRole:
        #     # row = index.row()
        #     print(self.filterCond)
        #     row = index.row()
        #     if self.filterCond and row in self.filterCond:
        #         return QtGui.QColor(255, 0, 0, 127)
        #     else:
        #         return QtGui.QColor(0, 0, 0, 127)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])
            
    # Method to set data in the model
    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        # Update the data in your model
        # Example: updating the data at the specified index
        if role == Qt.ItemDataRole.EditRole:
            self._data.iloc[index.row()][index.column()] = value
            return True
        return False
    

class MainWindow(QMainWindow):

    def __init__(self, first, r1Name, relation1, relationOut, r2Name=None, relation2=None):
        super().__init__()
        '''first: boolean'''
        self.w = None  # No external window yet.
        self.firstOp = first
        self.data1 = relation1
        self._rOut = relationOut
        
        self.r1Relations = r1Name
        self.r2Relations = r2Name
        self._r1Name = r1Name[0]
        i=1
        while i < len(r1Name):
            self._r1Name += '+'
            self._r1Name += r1Name[i]
            i+=1
        
        title = QLabel("BLOCKS VISUALISATION", alignment = Qt.AlignmentFlag.AlignCenter)
        table1Label = QLabel("Relation " + self._r1Name, alignment = Qt.AlignmentFlag.AlignCenter)
        outLabel = QLabel("Generated Output" , alignment = Qt.AlignmentFlag.AlignCenter)

        self.table1 = QTableView()

        self.outName = self._r1Name 
        
        self.outTable = QTableView()

        if not self.firstOp:
            df1 = pd.DataFrame(self.data1)
            df2 = pd.DataFrame(self._rOut)
            merged = pd.merge(df1, df2, how='inner')
            indices = df1[df1.isin(merged.to_dict('list')).all(axis=1)].index.tolist()
            print("indices: ",indices)
        else:
            indices = None

        #create table for relation 1
        self.model1 = BlockTable(self.data1, indices)
        self.table1.setModel(self.model1)
        
        # Add event bindings for row click
        if self.firstOp:
            self.table1.clicked.connect(self.show_new_window1)

        #create table for output 
        self.modelOut = OutTable(self._rOut)
        self.outTable.setModel(self.modelOut)


        
        
        #layout
        layout = QGridLayout()
        layout.addWidget(title, 0, 0, 1, 2)
        layout.addWidget(table1Label, 1, 0)
        layout.addWidget(self.table1, 2, 0)
        

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        if r2Name:
            self.data2 = relation2
            self.table2 = QTableView()
            self._r2Name = r2Name[0]
            i=1
            while i < len(r2Name):
                self._r2Name += '+'
                self._r2Name += r2Name[i]
                i+=1

            table2Label = QLabel("Relation "+ self._r2Name)
            self.model2 = BlockTable(self.data2, None)
            self.table2.setModel(self.model2)
            table2Label = QLabel("Relation " + self._r2Name, alignment = Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(table2Label, 3, 0)
            layout.addWidget(self.table2, 4, 0)

            # Add event bindings for row click
            self.table2.clicked.connect(self.show_new_window2)

            layout.addWidget(outLabel, 1, 1)
            layout.addWidget(self.outTable, 2, 1, 3, 1)
            
        else:
            self.model2 = None
            self.table2 = None
            layout.addWidget(outLabel, 1, 1)
            layout.addWidget(self.outTable, 2, 1)


    def show_new_window1(self, index: QModelIndex):
        if self.w is None:
            if index.isValid():
            # Get the row and column index from the clicked QModelIndex
                row = index.row()
                print("blk", row)
                self.w = TupleWindow(self.r1Relations, self._rOut, row)
                self.w.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.

    def show_new_window2(self, index: QModelIndex):
        if self.w is None:
            if index.isValid():
            # Get the row and column index from the clicked QModelIndex
                row = index.row()
                self.w = TupleWindow(self.r2Relations, self._rOut, row)
                self.w.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.


class DataRetriever():
    def __init__(self):
        self.database = Database()
        
    def getBlockNumber(self, relationName):
        '''
        relationName : (list of strings) '''
        data = self.database.getAllBlocksByRelation(relationName[0])
        maxBlk = max([int(t[0]) for t in data])
        if len(relationName) > 1:
            for i in range(1, len(relationName)):
                data = self.database.getAllBlocksByRelation(relationName[i])
                if max([int(t[0]) for t in data])>maxBlk:
                    maxBlk = max([int(t[0]) for t in data])

        return [{'Block Number': num} for num in range(maxBlk+1)]
    
    def getTuples(self, relation, blk):
        '''blk : (int) starts from 0 to length -1
        relation: (list of str)'''
        indRelations = {}
        data = Database().getAllTuplesByBlockNumber(relation, blk)
        for i in range(len(relation)):
            if data[relation[i]]:
                headers = data[relation[i]][0][1:]
                processed_data = []
                for entry in data[relation[i]][1:]:
                    processed_data.append(dict(zip(headers, entry[1:])))

                # print("processed:", relation[i], processed_data)
                indRelations[relation[i]] = processed_data
        return indRelations
    
    def getInterData(self, filename):
        #read in csv
        outData = pd.read_csv(filename)
        return outData
        
    # def getFilterData(self, scan=False, filenameIn = None, filenameOut = None, relationName = None, blkNum = None):
    #     if scan:
    #         merged = pd.merge(self.getTuples(relationName, blkNum), self.getInterData(filenameOut), how='inner', indicator=True)
    #     else:
    #         merged = pd.merge(self.getInterData(filenameIn), self.getInterData(filenameOut), how='inner', indicator=True)
    #     indices = merged[merged['_merge'] == 'both'].index.tolist()
    #     return indices

app = QApplication(sys.argv)

data2 = [
            {'Block Number': 0, 'Tuple Count': 25},
            {'Block Number': 1, 'Tuple Count': 22},
            {'Block Number': 2, 'Tuple Count': 22},
            {'Block Number': 3, 'Tuple Count': 20}
        ]
dataOut = [
            {'Block Number': 1, 'Tuple Count': 22},
            {'Block Number': 3, 'Tuple Count': 20}
        ]

# data = pd.read_csv('_17001883723227320.csv')
# print(data)


#compare the new data and old data
w = MainWindow(False,  ["orders"], DataRetriever().getInterData('_17001883712372842.csv'), DataRetriever().getInterData('_17001883723227320.csv'))
# w = MainWindow("scan", ["region"], parsedData, dataOut, ["Data3", 'Data4'], data2)
# w = MainWindow(False, ["orders"], DataRetriever().getInterData('_17001883703263180.csv'), DataRetriever().getInterData('_17001883241385750.csv'))
w.show()
app.exec()

#TODO 
    # Color filtered rows from select and join --> need to create a logic to compare tuples from this block and tuples from the resulting tuples 
    # read from csv
    # a logic to differentiate the different operator and read from different sources
    # put the screen into the interface.py
    # aggregate function --> set column colors 
    # output Tuple Table --> process csv and insert into TableView


    # Only the first operator -- scan + filter --> if there is a ctid --> means need to use BLOCKTABLE
    # else --> just display the p