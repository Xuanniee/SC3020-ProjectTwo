from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QTableView, QGridLayout, QLineEdit
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
    def __init__(self, relationName, rOut, blockNum, ctidArr):
        super().__init__()
        self.setWindowTitle("TUPLES IN THE BLOCK")
        self.allRelations = relationName
        self.bNo = blockNum
        self._rOut = rOut
        self.ctid = ctidArr
        
        
        # create a layout
        layout = QVBoxLayout()
        
        data = DataRetriever(dataBase).getTuples(self.allRelations, blockNum)
            
        for i in range(len(self.allRelations)):
            if data[self.allRelations[i]]:
                df1 = pd.DataFrame(data[self.allRelations[i]])
                # print(df1.head(5))
                # df2 = pd.DataFrame(self._rOut)
                # # print(df2.head(5))
                
                # merged = pd.merge(df1,df2, how="inner")

                # indices = df1[df1.isin(merged.to_dict('list')).all(axis=1)].index.tolist()
                indices = []
                if blockNum in self.ctid.keys():
                    indices = self.ctid[blockNum]
                print("indices: ",indices)

                filterLabel = QLabel("Number of Tuples Matched(Red) With Output: "+ str(len(indices)))
                
                model = TupleTable(data[self.allRelations[i]], indices)
                table = QTableView()
                table.setModel(model)
                label = QLabel("Relation "+ self.allRelations[i], alignment = Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(label)
                layout.addWidget(filterLabel)
                layout.addWidget(table)
            
        self.setLayout(layout)

    def on_search(self, text):
        # for row_index in range(self.modelOut.rowCount()):
        #     visible = any(text.lower() in self.modelOut.index(row_index, col_index).text().lower() for col_index in range(self.outTable.columnCount()))
        #     self.outTable.setRowHidden(row_index, not visible)
        print(self.modelOut.rowCount(None))
        for row in range(self.modelOut.rowCount(None)):
            print(row)
            visible = any(
                text in self.modelOut.index(row, col).data(role=Qt.ItemDataRole.DisplayRole).lower()
                for col in range(self.modelOut.columnCount(None))
            )
            print(visible)

        self.outTable.setRowHidden(row, not visible)


class TupleTable(QtCore.QAbstractTableModel):
    def __init__(self, data, condition):
        super(TupleTable, self).__init__()
        df = pd.DataFrame(data)
        self._data = df
        self.filterCond = condition
    
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)
        if role == Qt.ItemDataRole.BackgroundRole:
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
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])
    
    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if role == Qt.ItemDataRole.EditRole:
            self._data.iloc[index.row()][index.column()] = value
            return True
        return False
    

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
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])
            
    # Method to set data in the model
    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if role == Qt.ItemDataRole.EditRole:
            self._data.iloc[index.row()][index.column()] = value
            return True
        return False

class OutTable(QtCore.QAbstractTableModel):
    #pandas dataframe
    def __init__(self, data):
        super(OutTable, self).__init__()
        df = pd.DataFrame(data)
        self._data = df

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

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
        if role == Qt.ItemDataRole.EditRole:
            self._data.iloc[index.row()][index.column()] = value
            return True
        return False
    

class MainWindow(QMainWindow):
    '''first: boolean first operator (scan)
    r1Name - list of names of relations that make up relation1
    relation1 - dictionary of blocks/tuples
    relationOut - always a csv from weehung
    r2Name - list of names of relations that make up relation2
    relation2 - dictionary of blocks/tuples
    '''
    def __init__(self, first, r1Name, relation1, relationOut, r2Name=None, relation2=None):
        super().__init__()
        '''first: boolean'''
        self.w = None  # No external window yet.
        self.firstOp = first
        self.data1 = relation1
        

        self.ctidArr = {}
        if relationOut.columns[0] == "ctid":
            # print(outData["ctid"])
            for item in relationOut["ctid"]:
                # print(item[1:-1])
                block_no, tuple_ind = item[1:-1].split(",")
                block_no = int(block_no)
                tuple_ind = int(tuple_ind)-1
                # Check if blockNo already exists in the dictionary
                if block_no in self.ctidArr:
                    # Append tupleInd if it's not already in the list
                    if tuple_ind not in self.ctidArr[block_no]:
                        self.ctidArr[block_no].append(tuple_ind)
                else:
                    # Create a new list with the tupleInd
                    self.ctidArr[block_no] = [tuple_ind]
            # print(arr)
            self._rOut = relationOut.drop(columns=relationOut.columns[0])
        else:
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


        #layout
        layout = QGridLayout()
        layout.addWidget(title, 0, 0, 1, 2)


        #create table view for table 1, 2 and out
        self.table1 = QTableView()        
        self.outTable = QTableView()

        #filtering 
        if not self.firstOp:
            df1 = pd.DataFrame(self.data1)
            df2 = pd.DataFrame(self._rOut)
            merged = pd.merge(df1, df2, how='inner')
            indices = df1[df1.isin(merged.to_dict('list')).all(axis=1)].index.tolist()
            filterLabel1 = QLabel("Number of Tuples Matched(Red) with Output: " + str(len(indices)))
            
        else:
            indices = None
            filterLabel1 = QLabel("Number of Blocks: " + str(len(self.data1)))
        

        #insert data into table 1
        self.model1 = BlockTable(self.data1, indices)
        self.table1.setModel(self.model1)
        
        # Add event bindings for row click
        if self.firstOp: #allow to click for block format
            self.table1.clicked.connect(self.show_new_window1)

        #insert into layout
        layout.addWidget(table1Label, 1, 0)
        layout.addWidget(filterLabel1, 2, 0)
        layout.addWidget(self.table1, 3, 0)


        #insert data into table output 
        self.modelOut = OutTable(self._rOut)
        self.outTable.setModel(self.modelOut)
        layout.addWidget(outLabel, 1, 1)
        resLabel = QLabel("Number of Tuples Generated: " + str(len(self._rOut)))
        layout.addWidget(resLabel, 2, 1)

        # Add search filter line edit for output
        # self.searchBar = QLineEdit()
        # self.searchBar.setPlaceholderText("Search...")
        # self.searchBar.textChanged.connect(self.on_search)
        # layout.addWidget(self.searchBar, 3, 1)


        #if relation 2 exist
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
            if not self.firstOp:
                df1 = pd.DataFrame(self.data2)
                df2 = pd.DataFrame(self._rOut)
                merged = pd.merge(df1, df2, how='inner')
                indices = df1[df1.isin(merged.to_dict('list')).all(axis=1)].index.tolist()
                filterLabel2 = QLabel("Number of Tuples Matched(Red) with Output: " + str(len(indices)))
                # print("indices: ",indices)
            else:
                indices = None
            
            
            self.model2 = BlockTable(self.data2, indices)
            self.table2.setModel(self.model2)
            table2Label = QLabel("Relation " + self._r2Name, alignment = Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(table2Label, 4, 0)
            layout.addWidget(filterLabel2, 5, 0)
            layout.addWidget(self.table2, 6, 0)

            # Add event bindings for row click
            if self.firstOp:
                self.table2.clicked.connect(self.show_new_window2)
            
            layout.addWidget(self.outTable, 3, 1, 4, 1)
            
        else:
            self.model2 = None
            self.table2 = None
            
            layout.addWidget(self.outTable, 3, 1)


        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


    def show_new_window1(self, index: QModelIndex):
        if self.w is None:
            if index.isValid():
            # Get the row and column index from the clicked QModelIndex
                row = index.row()
                print("blk", row, "clicked")
                self.w = TupleWindow(self.r1Relations, self._rOut, row, self.ctidArr)
                self.w.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.

    def show_new_window2(self, index: QModelIndex):
        if self.w is None:
            if index.isValid():
            # Get the row and column index from the clicked QModelIndex
                row = index.row()
                print("blk", row, "clicked")
                self.w = TupleWindow(self.r2Relations, self._rOut, row, None)
                self.w.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.


class DataRetriever():
    def __init__(self, Database):
        self.database = Database
        
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
                indRelations[relation[i]] = processed_data
        return indRelations
    
    def getInterData(self, filename):
        #read in csv
        outData = pd.read_csv(filename)
        return outData
        
        
    

#main app running 

app = QApplication(sys.argv)


#compare the new data and old data
dataBase = Database()
'''firstOp --> getting the data tuples '''
# w = MainWindow(firstOp)
# w = MainWindow(False,  ["orders"], DataRetriever().getBlockNumber(["orders"]), DataRetriever().getBlockNumber(['nation']), ["part"],  DataRetriever().getBlockNumber(['part']))
w = MainWindow(False, ["orders"], DataRetriever(dataBase).getInterData('_17002222258294558.csv'), DataRetriever(dataBase).getInterData('_17002222094046320.csv'), ["customer"], DataRetriever(dataBase).getInterData('_17002221591810438.csv'))
# w = MainWindow(True, ["orders"], DataRetriever(dataBase).getBlockNumber(["orders"]), DataRetriever(dataBase).getInterData('_17002221524379862.csv'))
# DataRetriever(dataBase).getInterData('_17002221524379862.csv')
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