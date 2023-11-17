import sys
import json
import pandas as pd
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QToolBar,
    QStatusBar,
    QScrollArea,
    QGridLayout,
    QVBoxLayout,
    QWidget,
    QLabel,
    QTextEdit,
    QPushButton,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsRectItem,
    QGraphicsTextItem,
    QGraphicsLineItem,
    QSizePolicy,
    QTextBrowser,
    QDialog,
    QGraphicsProxyWidget,
    QTableView,
)

from explainExample9 import qepObject
from Database.database import Database
from explore import QEP, generateTree


"""
Global Parameters
"""
SQL_WINDOW_WIDTH = 300
SQL_WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1980
WINDOW_HEIGHT = 1800


"""
Main Application Window
"""
class QueryWindowGUI(QMainWindow):
    def __init__(self, dbName, dbUser, dbPassword, dbHost, portNum, qepObject=None, parsedQepData=None):
        super().__init__(parent=None)
        self.setWindowTitle("Query Visualisations GUI")
        self.resize(WINDOW_HEIGHT, WINDOW_WIDTH)
        self.parsedQepData = parsedQepData
        # self.qepObject = qepObject
        # self.qepObjectData = QEP(self.qepObject, save=True).resolve()

        """
        Initialise the Database
        """
        self.db = Database(DB_NAME=dbName, 
                        DB_USER=dbUser, 
                        DB_PASSWORD=dbPassword, 
                        DB_HOST=dbHost, 
                        PORT=portNum)

        self._createMenu()
        self._createToolBar()
        self._createStatusBar()
        self._createCentralLayout()

    def _createMenu(self):
        fileMenu = self.menuBar().addMenu("File")
        fileMenu.addAction("Exit", self.close)

    def _createToolBar(self):
        tools = QToolBar()
        tools.addAction("Exit", self.close)
        self.addToolBar(tools)

    def _createStatusBar(self):
        status = QStatusBar(self)
        status.showMessage("Query")
        self.setStatusBar(status)

    def _createCentralLayout(self):
        centralWidget = QWidget()
        centralAppLayout = QGridLayout(centralWidget)

        # Create and add SQLQueryWindow and LabelledQEPTreeWindow
        window2 = LabelledQEPTreeWindow(self.parsedQepData)
        window1 = SQLQueryWindow(qepTreeWindow=window2, database=self.db)

        # Add instructions QLabel at the top
        instructions_label = QLabel("Instructions:\n1. Enter SQL query in the first window.\n2. View the QEP tree and result in the second window.")
        centralAppLayout.addWidget(instructions_label, 0, 0, 1, 2)  # Spanning two columns

        # Set the Various Windows required
        centralAppLayout.addWidget(window1, 1, 0)
        centralAppLayout.addWidget(window2, 1, 1)
        centralAppLayout.addWidget(BeforeWindow(False,  ["orders"], DataRetriever().getInterData('_17001997288923678.csv'), DataRetriever().getInterData('_17001998061102650.csv')), 1, 2)
        centralAppLayout.addWidget(BeforeWindow(False,  ["orders"], DataRetriever().getInterData('_17001997288923678.csv'), DataRetriever().getInterData('_17001998061102650.csv')), 1, 2)

        scrollArea = QScrollArea()
        scrollArea.setAlignment(Qt.AlignmentFlag.AlignTop)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(centralWidget)

        self.setCentralWidget(scrollArea)


"""
Window 1 - Provide SQL Query from User
"""
class SQLQueryWindow(QWidget):
    def __init__(self, database, qepTreeWindow):
        super().__init__(parent=None)

        # Initialisation of Components
        self.setWindowTitle("SQL Query")
        self.label = QLabel("Provide your SQL Query:")
        self.textEdit = QTextEdit()
        self.submitButton = QPushButton("Submit")
        self.qepTreeWindow = qepTreeWindow
        self.db = database

        # Attach an Event Listener to the Button
        self.submitButton.clicked.connect(self.submitHandler)

        # Set Dimensions & Alignment of Cursor
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.textEdit.setFixedWidth(SQL_WINDOW_WIDTH)
        self.textEdit.setFixedHeight(SQL_WINDOW_HEIGHT)
        self.textEdit.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.textEdit, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.submitButton, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

    def submitHandler(self):
        # Retrieve User Text
        userInputQuery = self.textEdit.toPlainText()
        print("Extracted User Input: ", userInputQuery)

        # Provide some backend logic to send the text to the backend
        rawQEP = self.db.explainQuery(userInputQuery)
        rawQEP = rawQEP[0][0][0]

        # Resolves the intermediate results of the QEP
        QEPExecutor =  QEP(rawQEP['Plan'], save=True)
        QEPExecutor.resolve()

        qepData = generateTree(qep=rawQEP)
        
        with open('testTree.json', 'w') as out:
            out.write(json.dumps(qepData, indent=4))
        
        QEPExecutor.cleanup()
        
        parsedQepData = qepData.get("tree", "N/A")

        # Check if parsedData is None
        if parsedQepData is "N/A":
            # TODO Print no tree printed on the screen somehow
            print("No tree should be printed")

        # Update the Window's content
        self.qepTreeWindow.updateContent(parsedQepData)

        # Clear the Text after Submission
        self.textEdit.clear()


"""
Helper Function to help Parse the JSON Object from PostgreSQL to build the QEP Tree
"""
class NodeInfoDialog(QDialog):
    def __init__(self, nodeData, parent=None):
        super(NodeInfoDialog, self).__init__(parent)
        self.setWindowTitle("Node Information")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        info_text = self.retrieveNodeInfo(nodeData)
        text_browser = QTextBrowser()
        text_browser.setPlainText(info_text)

        layout.addWidget(text_browser)

        # Add a button to Pass the Data to 3rd Window
        button = QPushButton("Visualise in Greater Detail")

        # Pass the Filename
        button.clicked.connect(self.furtherVisualise)
        
        layout.addWidget(button)

        self.setLayout(layout)

    def retrieveNodeInfo(self, nodeData):
        info = ""
        for key, value in nodeData.items():
            if key != "Query" or key != "Filename":
                info += f"{key}: {value}\n"
        return info

    def furtherVisualise(self):
        # BeforeWindow(False,  ["orders"], DataRetriever().getInterData('_17001997288923678.csv'), DataRetriever().getInterData('_17001998061102650.csv')
        # Determine if it's first
        pass

class CustomNode(QGraphicsRectItem):
    def __init__(self, x, y, width, height, nodeData):
        super().__init__(x, y, width, height)
        self.nodeData = nodeData
        # Assume it is a Leaf Node until proven otherwise
        self.isLeaf = True
        self.setAcceptHoverEvents(True)

        # Create a label widget to display node information
        self.label = QLabel()
        self.label.setStyleSheet("background-color: black; border: 1px solid white; padding: 5px;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.label.setVisible(False)

        # Create a proxy widget for the label
        self.proxyWidget = QGraphicsProxyWidget(self)
        self.proxyWidget.setWidget(self.label)

    def hoverEnterEvent(self, event):
        # Display information in a tooltip or custom widget when the mouse hovers over the rectangle
        info = self.retrieveNodeInfo(self.nodeData)
        self.label.setText(info)

        # Align the label with the cursor
        cursor_pos = event.scenePos()
        label_pos = self.mapFromScene(cursor_pos)
        self.proxyWidget.setPos(label_pos)
        self.label.setVisible(True)

    def hoverLeaveEvent(self, event):
        # Hide the displayed information when the mouse leaves the rectangle
        self.label.setVisible(False)

    def mousePressEvent(self, event):
        # Display a pop-up window when the user clicks on the rectangle
        node_info_dialog = NodeInfoDialog(self.nodeData)
        node_info_dialog.exec()

    def retrieveNodeInfo(self, nodeData):
        info = f"Node Type: {nodeData.get('Node Type', 'N/A')}\n"
        info += f"Cost: {nodeData.get('Total Cost', 'N/A')}\n"
        info += f"Output: {nodeData.get('Output', 'N/A')}\n"
        info += f"Group Key: {nodeData.get('Group Key', 'N/A')}\n"
        info += f"Rows: {nodeData.get('Actual Rows', 'N/A')}\n"
        info += f"Loops: {nodeData.get('Actual Loops', 'N/A')}"

        return info


"""
Window 2 - Display the QEP Tree received from the Backend
"""
NODE_WIDTH = 200
NODE_HEIGHT = 75
NODE_HORIZONTAL_SPACING = 20
NODE_VERTICAL_SPACING = 100

class LabelledQEPTreeWindow(QWidget):
    def __init__(self, parsedQepData, parent=None):
        super(LabelledQEPTreeWindow, self).__init__(parent)

        # Create a QVBoxLayout
        layout = QVBoxLayout(self)

        # Add a label to the layout
        label = QLabel("QEP Tree Visualiser")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignTop |   Qt.AlignmentFlag.AlignHCenter)

        # Create an instance of QEPTreeWindow and add it to the layout
        self.treeWindow = QEPTreeWindow(parsedQepData)
        layout.addWidget(self.treeWindow, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        # Manually set the sizeHint of the label to reduce the vertical gap
        label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        label.setFixedSize(label.sizeHint())

        # Manually set the geometry of the treeWindow to reduce the vertical gap
        self.treeWindow.setFixedHeight(self.treeWindow.sizeHint().height())

        # Set the layout for the window
        self.setLayout(layout)

    def updateContent(self, parsedQepData):
        # Update the content based on the new data
        self.treeWindow.updateContent(parsedQepData)


class QEPTreeWindow(QGraphicsView):
    def __init__(self, parsedQepData, parent=None):
        super(QEPTreeWindow, self).__init__(parent)
        self.parsedQepData = parsedQepData
        self.setFixedSize(SQL_WINDOW_WIDTH * 2, SQL_WINDOW_HEIGHT)

        # Create a Dictionary to Track Nodes with their Top and Bottom Coordinates
        self.topDict = {}
        self.bottomDict = {}

        # Set up the QGraphicsScene
        scene = QGraphicsScene(self)
        scene.setSceneRect(0, 0, WINDOW_HEIGHT, WINDOW_WIDTH)
        # scene.setSceneRect(0, 0, float('inf'), float('inf')) # Set infinite

        # Check if parsedQepData is None
        if parsedQepData is not None:
            # Draw the QEP Tree
            self.drawQepTree(scene, parsedQepData, x=200, y=100)

        # Set the scene for the view
        self.setScene(scene)
        scene.setBackgroundBrush(Qt.GlobalColor.white)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    def updateContent(self, parsedQepData):
        # Update the content based on the new data
        self.parsedQepData = parsedQepData
        self.scene().clear()  # Clear the existing scene
        self.drawQepTree(self.scene(), parsedQepData, x=200, y=100)

    """
    Plot a QEP Tree starting from the lowest level before moving to the root, where x and y are the initial starting coordinates
    """
    def drawQepTree(self, scene, parsedQepData, x, y):
        # x, y represents the coordinates of the top left corner of the rectangle
        currX = x
        currY = y
        firstIter = True

        # Iterate starting from the Root of the Tree
        numLevels = len(parsedQepData)
        for level in sorted(parsedQepData.keys()):
            nodesList = parsedQepData[level]

            # level represents the level of the tree, e.g. 0.0.0.0 is level 4, while nodes contains information about all nodes in the tree
            if not firstIter:
                # Went down a level
                currY += (NODE_HEIGHT + NODE_VERTICAL_SPACING)
            else:
                firstIter = False

            numNodesOnCurrLevel = len(nodesList)
            # Iterate over all the nodes in this level (if there are more than 1
            for index, node in enumerate(nodesList):
                if index != 0:
                    # As long as not first iter
                    # Determine the Location of the next Node on the same level, currY is constant on the same level
                    currX  = currX + NODE_WIDTH + NODE_HORIZONTAL_SPACING

                # Create a QGraphicsRectItem for the current node
                currNode = CustomNode(currX, currY, NODE_WIDTH, NODE_HEIGHT, node)
        
                scene.addItem(currNode)

                # Create a QGraphicsTextItem to display node information at same place 
                nodeDesc = QGraphicsTextItem(self.retrieveSimpleNodeInfo(node))
                # Set the text color to black
                nodeDesc.setDefaultTextColor(Qt.GlobalColor.black)
                nodeDesc.setPos(currX, currY)
                scene.addItem(nodeDesc)

                # Store the Top & Bottom Coordinate of each node
                currNodeID = node["NodeID"]

                # Curr Node is Key, while value is the Coordinate
                currTopX = currX + (NODE_WIDTH / 2)
                currTopY = currY
                currBotX = currTopX
                currBotY = currTopY + NODE_HEIGHT
                # print("Top: ", (currTopX, currTopY))
                # print("Bot: ", (currBotX, currBotY))
                self.topDict[currNodeID] = (currTopX, currTopY)
                self.bottomDict[currNodeID] = (currBotX, currBotY)


                # Draw line connecting parent and child nodes
                # print(level)
                if level > 0:
                    # Retrieve Parent Bottom
                    parentNodeID = node["ParentNodeID"]
                    # Handle the case when parentNodeID is 0 (root node)
                    parentX = self.bottomDict[parentNodeID][0]
                    parentY = self.bottomDict[parentNodeID][1]

                    # Create a QGraphicsLineItem
                    lineItem = QGraphicsLineItem()
                    
                    # Set the line coordinates
                    lineItem.setLine(parentX, parentY, currTopX, currTopY)

                    # Add the line to the scene
                    scene.addItem(lineItem)
                    # lineItem = QGraphicsLineItem(parentX, parentY, parentX, parentY + NODE_VERTICAL_SPACING)
                    # scene.addItem(lineItem)

                # Check if a next level exists
                if level < numLevels - 1:
                    # Determine the Next Node Position on the Next Level
                    nextLevel = sorted(parsedQepData.keys())[sorted(parsedQepData.keys()).index(level) + 1]
                    print("Next Level pls: ", nextLevel)
                    nodesListNextLevel = parsedQepData[nextLevel]
                    
                    numNodesNextLevel = len(nodesListNextLevel)
                    
                    if numNodesNextLevel > 1:
                        # If there is more than one node in the current level, calculate the position
                        # Determine the Total Distance
                        totalHoriDistance = (numNodesOnCurrLevel - 1) * (NODE_WIDTH + NODE_HORIZONTAL_SPACING) + NODE_WIDTH
                        
                        # Get the Center Position of the Current Node and Travel half the horizontal distance to the left
                        currX = currBotX - (totalHoriDistance / 2) - (NODE_WIDTH / 2)
                        
                    else:
                        # If there is only one node in the current level, don't change since it will just be vertical
                        currX = currX
                    
                    # Check if the node has child nodes at the next level
                    print("currNodeID: ", currNodeID)
                    print("nodeList: ", nodesListNextLevel)
                    print()
                    currNode.isLeaf = not self.hasChildrenInNextLevel(currNodeID, nodesListNextLevel)

                # Check if the current node is a leaf node
                if currNode.isLeaf:
                    print("It went in")
                    # Get the Relation Name from the leaf node
                    relationName = node.get('Relation Name', 'N/A')

                    # Draw another rectangle representing the relation directly below the leaf node
                    relationRect = CustomNode(currTopX - (NODE_WIDTH/2), currTopY + NODE_HEIGHT + NODE_VERTICAL_SPACING, NODE_WIDTH, NODE_HEIGHT, {'Relation Name': relationName})
                    relationRect.setBrush(Qt.GlobalColor.lightGray)
                    scene.addItem(relationRect)

                    # Draw a line connecting the leaf node and the relation rectangle
                    lineItem = QGraphicsLineItem()
                    lineItem.setLine(currTopX, currTopY + NODE_HEIGHT, currTopX, currTopY + NODE_HEIGHT + NODE_VERTICAL_SPACING)
                    scene.addItem(lineItem)

                    # Create a QGraphicsTextItem to display node information at same place 
                    nodeDesc = QGraphicsTextItem(f"Relation: {relationName}")
                    # Set the text color to black
                    nodeDesc.setDefaultTextColor(Qt.GlobalColor.black)
                    nodeDesc.setPos(currTopX - (NODE_WIDTH/2), currTopY + NODE_HEIGHT + NODE_VERTICAL_SPACING)
                    scene.addItem(nodeDesc)
                    print("It going out")
                    
        # Iterate over all the nodes and update bounding rectangle
        boundingRect = None
        for node in scene.items():
            boundingRect = boundingRect.united(node.sceneBoundingRect()) if boundingRect else node.sceneBoundingRect()

        # Set the scene rectangle to the bounding rectangle
        scene.setSceneRect(boundingRect)
        print("it's here")

    def hasChildrenInNextLevel(self, currNodeID, nodesListNextLevel):
        # Check if the node has children in the next level
        return any(node["ParentNodeID"] == currNodeID for node in nodesListNextLevel)

    def retrieveSimpleNodeInfo(self, nodeData):
        info = f"Node Type: {nodeData.get('Node Type', 'N/A')}\n"
        return info

    

"""
Window 3 - Display the Before of Data Block Visualisations
"""
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
    

class BeforeWindow(QMainWindow):
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

"""
Window 4 - Display the After of Data Block Visualisations
"""
# TODO
class AfterWindow(QWidget):
    def __init__(self):
        super().__init__(parent=None)

# """
# Main Script - To be abstracted into a different script subsequently
# """
# if __name__ == "__main__":
#     # qepData = {
#     #     1: [{
#     #         'Node Type': 'Seq Scan', 'Parent Relationship': 'Outer', 'Parallel Aware': False, 'Async Capable': False, 'Relation Name': 'nation', 'Schema': 'public', 
#     #         'Alias': 'nation', 'Startup Cost': 0.0, 'Total Cost': 12.12, 'Plan Rows': 1, 'Plan Width': 434, 'Actual Startup Time': 0.003, 'Actual Total Time': 0.004, 
#     #         'Actual Rows': 0, 'Actual Loops': 1, 'Output': ['n_nationkey', 'n_name', 'n_regionkey', 'n_comment'], 'Filter': "(nation.n_name = 'ALGERIA'::bpchar)", 
#     #         'Rows Removed by Filter': 0, 'Shared Hit Blocks': 0, 'Shared Read Blocks': 0, 'Shared Dirtied Blocks': 0, 'Shared Written Blocks': 0, 'Local Hit Blocks': 0, 
#     #         'Local Read Blocks': 0, 'Local Dirtied Blocks': 0, 'Local Written Blocks': 0, 'Temp Read Blocks': 0, 'Temp Written Blocks': 0, 'NodeID': 1, 'ParentNodeID': 0
#     #     }], 
#     #     0: [{
#     #         'Node Type': 'Sort', 'Parallel Aware': False, 'Async Capable': False, 'Startup Cost': 12.13, 'Total Cost': 12.14, 'Plan Rows': 1, 'Plan Width': 434, 
#     #         'Actual Startup Time': 0.015, 'Actual Total Time': 0.016, 'Actual Rows': 0, 'Actual Loops': 1, 'Output': ['n_nationkey', 'n_name', 'n_regionkey', 'n_comment'], 
#     #         'Sort Key': ['nation.n_nationkey'], 'Sort Method': 'quicksort', 'Sort Space Used': 25, 'Sort Space Type': 'Memory', 'Shared Hit Blocks': 3, 
#     #         'Shared Read Blocks': 0, 'Shared Dirtied Blocks': 0, 'Shared Written Blocks': 0, 'Local Hit Blocks': 0, 'Local Read Blocks': 0, 'Local Dirtied Blocks': 0, 
#     #         'Local Written Blocks': 0, 'Temp Read Blocks': 0, 'Temp Written Blocks': 0, 'NodeID': 0, 'ParentNodeID': None
#     #     }]
#     # }
#     qepData = {
#                 'tree': {
#                     1: [{'Node Type': 'Seq Scan', 'Parent Relationship': 'Outer', 'Parallel Aware': False, 'Async Capable': False, 'Relation Name': 'supplier', 'Schema': 'public',
#                         'Alias': 'supplier', 'Startup Cost': 0.0, 'Total Cost': 11.5, 'Plan Rows': 150, 'Plan Width': 512, 'Actual Startup Time': 0.005, 'Actual Total Time': 0.005, 
#                         'Actual Rows': 0, 'Actual Loops': 1, 'Output': ['supplier.s_suppkey', 'supplier.s_name', 'supplier.s_address', 'supplier.s_nationkey', 'supplier.s_phone', 
#                         'supplier.s_acctbal', 'supplier.s_comment'], 'Shared Hit Blocks': 0, 'Shared Read Blocks': 0, 'Shared Dirtied Blocks': 0, 'Shared Written Blocks': 0, 'Local Hit Blocks': 0, 'Local Read Blocks': 0, 
#                         'Local Dirtied Blocks': 0, 'Local Written Blocks': 0, 'Temp Read Blocks': 0, 'Temp Written Blocks': 0, 'NodeID': 1, 'ParentNodeID': 0}, 
                        
#                         {'Node Type': 'Hash', 'Parent Relationship': 'Inner', 'Parallel Aware': False, 'Async Capable': False, 
#                         'Startup Cost': 32.71, 'Total Cost': 32.71, 'Plan Rows': 170, 'Plan Width': 864, 'Actual Startup Time': 0.0, 'Actual Total Time': 0.0, 'Actual Rows': 0, 
#                         'Actual Loops': 0, 'Output': ['nation.n_nationkey', 'nation.n_name', 'nation.n_regionkey', 'nation.n_comment', 'region.r_regionkey', 'region.r_name', 
#                         'region.r_comment'], 'Shared Hit Blocks': 0, 'Shared Read Blocks': 0, 'Shared Dirtied Blocks': 0, 'Shared Written Blocks': 0, 'Local Hit Blocks': 0, 
#                         'Local Read Blocks': 0, 'Local Dirtied Blocks': 0, 'Local Written Blocks': 0, 'Temp Read Blocks': 0, 'Temp Written Blocks': 0, 'NodeID': 2, 
#                         'ParentNodeID': 0}], 
                        
#                     4: [{'Node Type': 'Seq Scan', 'Parent Relationship': 'Outer', 'Parallel Aware': False, 'Async Capable': False, 'Relation Name': 
#                         'nation', 'Schema': 'public', 'Alias': 'nation', 'Startup Cost': 0.0, 'Total Cost': 11.7, 'Plan Rows': 170, 'Plan Width': 434, 'Actual Startup Time': 0.0, 
#                         'Actual Total Time': 0.0, 'Actual Rows': 0, 'Actual Loops': 0, 'Output': ['nation.n_nationkey', 'nation.n_name', 'nation.n_regionkey', 'nation.n_comment'], 
#                         'Shared Hit Blocks': 0, 'Shared Read Blocks': 0, 'Shared Dirtied Blocks': 0, 'Shared Written Blocks': 0, 'Local Hit Blocks': 0, 'Local Read Blocks': 0, 
#                         'Local Dirtied Blocks': 0, 'Local Written Blocks': 0, 'Temp Read Blocks': 0, 'Temp Written Blocks': 0, 'NodeID': 5, 'ParentNodeID': 4}, 
                        
#                         {'Node Type': 'Hash', 
#                         'Parent Relationship': 'Inner', 'Parallel Aware': False, 'Async Capable': False, 'Startup Cost': 11.7, 'Total Cost': 11.7, 'Plan Rows': 170, 'Plan Width': 430, 
#                         'Actual Startup Time': 0.0, 'Actual Total Time': 0.0, 'Actual Rows': 0, 'Actual Loops': 0, 'Output': ['region.r_regionkey', 'region.r_name', 'region.r_comment'], 
#                         'Shared Hit Blocks': 0, 'Shared Read Blocks': 0, 'Shared Dirtied Blocks': 0, 'Shared Written Blocks': 0, 'Local Hit Blocks': 0, 'Local Read Blocks': 0, 
#                         'Local Dirtied Blocks': 0, 'Local Written Blocks': 0, 'Temp Read Blocks': 0, 'Temp Written Blocks': 0, 'NodeID': 6, 'ParentNodeID': 4}], 
                        
#                     5: [{'Node Type': 'Seq Scan', 
#                         'Parent Relationship': 'Outer', 'Parallel Aware': False, 'Async Capable': False, 'Relation Name': 'region', 'Schema': 'public', 'Alias': 'region', 'Startup Cost': 0.0, 
#                         'Total Cost': 11.7, 'Plan Rows': 170, 'Plan Width': 430, 'Actual Startup Time': 0.0, 'Actual Total Time': 0.0, 'Actual Rows': 0, 'Actual Loops': 0, 'Output': ['region.r_regionkey', 
#                         'region.r_name', 'region.r_comment'], 'Shared Hit Blocks': 0, 'Shared Read Blocks': 0, 'Shared Dirtied Blocks': 0, 'Shared Written Blocks': 0, 'Local Hit Blocks': 0, 
#                         'Local Read Blocks': 0, 'Local Dirtied Blocks': 0, 'Local Written Blocks': 0, 'Temp Read Blocks': 0, 'Temp Written Blocks': 0, 'NodeID': 7, 'ParentNodeID': 6}], 

#                     3: [{'Node Type': 'Hash Join', 'Parent Relationship': 'Outer', 'Parallel Aware': False, 'Async Capable': False, 'Join Type': 'Inner', 'Startup Cost': 13.82, 
#                          'Total Cost': 25.98, 'Plan Rows': 170, 'Plan Width': 864, 'Actual Startup Time': 0.0, 'Actual Total Time': 0.0, 'Actual Rows': 0, 'Actual Loops': 0, 'Output': 
#                          ['nation.n_nationkey', 'nation.n_name', 'nation.n_regionkey', 'nation.n_comment', 'region.r_regionkey', 'region.r_name', 'region.r_comment'], 'Inner Unique': True, 
#                          'Hash Cond': '(nation.n_regionkey = region.r_regionkey)', 'Shared Hit Blocks': 0, 'Shared Read Blocks': 0, 'Shared Dirtied Blocks': 0, 'Shared Written Blocks': 0, 
#                          'Local Hit Blocks': 0, 'Local Read Blocks': 0, 'Local Dirtied Blocks': 0, 'Local Written Blocks': 0, 'Temp Read Blocks': 0, 'Temp Written Blocks': 0, 'NodeID': 4, 
#                          'ParentNodeID': 3}], 
                         
#                     2: [{'Node Type': 'Sort', 'Parent Relationship': 'Outer', 'Parallel Aware': False, 'Async Capable': False, 'Startup Cost': 32.28, 'Total Cost': 32.71, 
#                         'Plan Rows': 170, 'Plan Width': 864, 'Actual Startup Time': 0.0, 'Actual Total Time': 0.0, 'Actual Rows': 0, 'Actual Loops': 0, 'Output': ['nation.n_nationkey', 
#                         'nation.n_name', 'nation.n_regionkey', 'nation.n_comment', 'region.r_regionkey', 'region.r_name', 'region.r_comment'], 'Sort Key': ['nation.n_nationkey'], 'Shared Hit Blocks': 0, 
#                         'Shared Read Blocks': 0, 'Shared Dirtied Blocks': 0, 'Shared Written Blocks': 0, 'Local Hit Blocks': 0, 'Local Read Blocks': 0, 'Local Dirtied Blocks': 0, 
#                         'Local Written Blocks': 0, 'Temp Read Blocks': 0, 'Temp Written Blocks': 0, 'NodeID': 3, 'ParentNodeID': 2}], 
                        
#                     0: [{'Node Type': 'Hash Join', 'Parallel Aware': False, 
#                         'Async Capable': False, 'Join Type': 'Inner', 'Startup Cost': 34.83, 'Total Cost': 48.39, 'Plan Rows': 150, 'Plan Width': 1376, 'Actual Startup Time': 0.005, 
#                         'Actual Total Time': 0.006, 'Actual Rows': 0, 'Actual Loops': 1, 'Output': ['nation.n_nationkey', 'nation.n_name', 'nation.n_regionkey', 'nation.n_comment', 
#                         'region.r_regionkey', 'region.r_name', 'region.r_comment', 'supplier.s_suppkey', 'supplier.s_name', 'supplier.s_address', 'supplier.s_nationkey', 'supplier.s_phone', 
#                         'supplier.s_acctbal', 'supplier.s_comment'], 'Inner Unique': False, 'Hash Cond': '(supplier.s_nationkey = nation.n_nationkey)', 'Shared Hit Blocks': 0, 
#                         'Shared Read Blocks': 0, 'Shared Dirtied Blocks': 0, 'Shared Written Blocks': 0, 'Local Hit Blocks': 0, 'Local Read Blocks': 0, 'Local Dirtied Blocks': 0, 
#                         'Local Written Blocks': 0, 'Temp Read Blocks': 0, 'Temp Written Blocks': 0, 'NodeID': 0, 'ParentNodeID': None}]}, 'additionalInfo': {'Shared Hit Blocks': 104, 
#                         'Shared Read Blocks': 8, 'Shared Dirtied Blocks': 1, 'Shared Written Blocks': 0, 'Local Hit Blocks': 0, 'Local Read Blocks': 0, 'Local Dirtied Blocks': 0, 
#                         'Local Written Blocks': 0, 'Temp Read Blocks': 0, 'Temp Written Blocks': 0, 'Ranking': [(('Seq Scan', 1), 11.5), (('Seq Scan', 5), 11.7), (('Seq Scan', 7), 11.7), 
#                         (('Hash', 6), 11.7), (('Hash Join', 4), 25.98), (('Sort', 3), 32.71), (('Hash', 2), 32.71)]}
#         }

#     queryApp = QApplication([])
#     queryWindow = QueryWindowGUI(qepObject)
#     queryWindow.show()
#     sys.exit(queryApp.exec())


