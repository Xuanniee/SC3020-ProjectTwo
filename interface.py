import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
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
)

from Database.database import Database


"""
Global Parameters
"""
SQL_WINDOW_WIDTH = 300
SQL_WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1980
WINDOW_HEIGHT = 1800

"""
Initialise the Database
"""
db = Database()

"""
Main Application Window
"""
class QueryWindowGUI(QMainWindow):
    def __init__(self, parsedQepData=None):
        super().__init__(parent=None)
        self.setWindowTitle("Query Visualisations GUI")
        self.resize(WINDOW_HEIGHT, WINDOW_WIDTH)
        self.parsedQepData = parsedQepData

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

        window2 = LabelledQEPTreeWindow(self.parsedQepData)
        window1 = SQLQueryWindow(qepTreeWindow=window2)

        # Set the Various Windows required
        centralAppLayout.addWidget(window1, 0, 0)
        # scene = QGraphicsScene()
        centralAppLayout.addWidget(window2, 0, 1)
        centralAppLayout.addWidget(SQLQueryWindow(QEPTreeWindow(None)), 0, 2)
        centralAppLayout.addWidget(SQLQueryWindow(QEPTreeWindow(None)), 0, 3)

        scrollArea = QScrollArea()
        scrollArea.setAlignment(Qt.AlignmentFlag.AlignTop)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(centralWidget)

        self.setCentralWidget(scrollArea)

"""
Window 1 - Provide SQL Query from User
"""
class SQLQueryWindow(QWidget):
    def __init__(self, qepTreeWindow):
        super().__init__(parent=None)

        # Initialisation of Components
        self.setWindowTitle("SQL Query")
        self.label = QLabel("Provide your SQL Query:")
        self.textEdit = QTextEdit()
        self.submitButton = QPushButton("Submit")
        self.qepTreeWindow = qepTreeWindow

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
        qepData = db.generateTree(userInputQuery)
        parsedQepData = qepData.get("tree", "N/A")

        # Check if parsedData is None
        if parsedQepData is None:
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
        self.setLayout(layout)

    def retrieveNodeInfo(self, nodeData):
        info = ""
        for key, value in nodeData.items():
            info += f"{key}: {value}\n"
        return info

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
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

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
        # Iterate over all the nodes and update bounding rectangle
        boundingRect = None
        for node in scene.items():
            boundingRect = boundingRect.united(node.sceneBoundingRect()) if boundingRect else node.sceneBoundingRect()

        # Set the scene rectangle to the bounding rectangle
        scene.setSceneRect(boundingRect)

    def hasChildrenInNextLevel(self, currNodeID, nodesListNextLevel):
        # Check if the node has children in the next level
        return any(node["ParentNodeID"] == currNodeID for node in nodesListNextLevel)

    def retrieveSimpleNodeInfo(self, nodeData):
        info = f"Node Type: {nodeData.get('Node Type', 'N/A')}\n"
        return info

    

"""
Window 3 - Display the Before of Data Block Visualisations
"""
# TODO
class BeforeWindow(QWidget):
    def __init__(self):
        super().__init__(parent=None)


"""
Window 4 - Display the After of Data Block Visualisations
"""
# TODO
class AfterWindow(QWidget):
    def __init__(self):
        super().__init__(parent=None)

"""
Main Script - To be abstracted into a different script subsequently
"""
if __name__ == "__main__":
    # qepData = {
    #     1: [{
    #         'Node Type': 'Seq Scan', 'Parent Relationship': 'Outer', 'Parallel Aware': False, 'Async Capable': False, 'Relation Name': 'nation', 'Schema': 'public', 
    #         'Alias': 'nation', 'Startup Cost': 0.0, 'Total Cost': 12.12, 'Plan Rows': 1, 'Plan Width': 434, 'Actual Startup Time': 0.003, 'Actual Total Time': 0.004, 
    #         'Actual Rows': 0, 'Actual Loops': 1, 'Output': ['n_nationkey', 'n_name', 'n_regionkey', 'n_comment'], 'Filter': "(nation.n_name = 'ALGERIA'::bpchar)", 
    #         'Rows Removed by Filter': 0, 'Shared Hit Blocks': 0, 'Shared Read Blocks': 0, 'Shared Dirtied Blocks': 0, 'Shared Written Blocks': 0, 'Local Hit Blocks': 0, 
    #         'Local Read Blocks': 0, 'Local Dirtied Blocks': 0, 'Local Written Blocks': 0, 'Temp Read Blocks': 0, 'Temp Written Blocks': 0, 'NodeID': 1, 'ParentNodeID': 0
    #     }], 
    #     0: [{
    #         'Node Type': 'Sort', 'Parallel Aware': False, 'Async Capable': False, 'Startup Cost': 12.13, 'Total Cost': 12.14, 'Plan Rows': 1, 'Plan Width': 434, 
    #         'Actual Startup Time': 0.015, 'Actual Total Time': 0.016, 'Actual Rows': 0, 'Actual Loops': 1, 'Output': ['n_nationkey', 'n_name', 'n_regionkey', 'n_comment'], 
    #         'Sort Key': ['nation.n_nationkey'], 'Sort Method': 'quicksort', 'Sort Space Used': 25, 'Sort Space Type': 'Memory', 'Shared Hit Blocks': 3, 
    #         'Shared Read Blocks': 0, 'Shared Dirtied Blocks': 0, 'Shared Written Blocks': 0, 'Local Hit Blocks': 0, 'Local Read Blocks': 0, 'Local Dirtied Blocks': 0, 
    #         'Local Written Blocks': 0, 'Temp Read Blocks': 0, 'Temp Written Blocks': 0, 'NodeID': 0, 'ParentNodeID': None
    #     }]
    # }
    qepData = {
                'tree': {
                    1: [{'Node Type': 'Seq Scan', 'Parent Relationship': 'Outer', 'Parallel Aware': False, 'Async Capable': False, 'Relation Name': 'supplier', 'Schema': 'public',
                        'Alias': 'supplier', 'Startup Cost': 0.0, 'Total Cost': 11.5, 'Plan Rows': 150, 'Plan Width': 512, 'Actual Startup Time': 0.005, 'Actual Total Time': 0.005, 
                        'Actual Rows': 0, 'Actual Loops': 1, 'Output': ['supplier.s_suppkey', 'supplier.s_name', 'supplier.s_address', 'supplier.s_nationkey', 'supplier.s_phone', 
                        'supplier.s_acctbal', 'supplier.s_comment'], 'Shared Hit Blocks': 0, 'Shared Read Blocks': 0, 'Shared Dirtied Blocks': 0, 'Shared Written Blocks': 0, 'Local Hit Blocks': 0, 'Local Read Blocks': 0, 
                        'Local Dirtied Blocks': 0, 'Local Written Blocks': 0, 'Temp Read Blocks': 0, 'Temp Written Blocks': 0, 'NodeID': 1, 'ParentNodeID': 0}, 
                        
                        {'Node Type': 'Hash', 'Parent Relationship': 'Inner', 'Parallel Aware': False, 'Async Capable': False, 
                        'Startup Cost': 32.71, 'Total Cost': 32.71, 'Plan Rows': 170, 'Plan Width': 864, 'Actual Startup Time': 0.0, 'Actual Total Time': 0.0, 'Actual Rows': 0, 
                        'Actual Loops': 0, 'Output': ['nation.n_nationkey', 'nation.n_name', 'nation.n_regionkey', 'nation.n_comment', 'region.r_regionkey', 'region.r_name', 
                        'region.r_comment'], 'Shared Hit Blocks': 0, 'Shared Read Blocks': 0, 'Shared Dirtied Blocks': 0, 'Shared Written Blocks': 0, 'Local Hit Blocks': 0, 
                        'Local Read Blocks': 0, 'Local Dirtied Blocks': 0, 'Local Written Blocks': 0, 'Temp Read Blocks': 0, 'Temp Written Blocks': 0, 'NodeID': 2, 
                        'ParentNodeID': 0}], 
                        
                    4: [{'Node Type': 'Seq Scan', 'Parent Relationship': 'Outer', 'Parallel Aware': False, 'Async Capable': False, 'Relation Name': 
                        'nation', 'Schema': 'public', 'Alias': 'nation', 'Startup Cost': 0.0, 'Total Cost': 11.7, 'Plan Rows': 170, 'Plan Width': 434, 'Actual Startup Time': 0.0, 
                        'Actual Total Time': 0.0, 'Actual Rows': 0, 'Actual Loops': 0, 'Output': ['nation.n_nationkey', 'nation.n_name', 'nation.n_regionkey', 'nation.n_comment'], 
                        'Shared Hit Blocks': 0, 'Shared Read Blocks': 0, 'Shared Dirtied Blocks': 0, 'Shared Written Blocks': 0, 'Local Hit Blocks': 0, 'Local Read Blocks': 0, 
                        'Local Dirtied Blocks': 0, 'Local Written Blocks': 0, 'Temp Read Blocks': 0, 'Temp Written Blocks': 0, 'NodeID': 5, 'ParentNodeID': 4}, 
                        
                        {'Node Type': 'Hash', 
                        'Parent Relationship': 'Inner', 'Parallel Aware': False, 'Async Capable': False, 'Startup Cost': 11.7, 'Total Cost': 11.7, 'Plan Rows': 170, 'Plan Width': 430, 
                        'Actual Startup Time': 0.0, 'Actual Total Time': 0.0, 'Actual Rows': 0, 'Actual Loops': 0, 'Output': ['region.r_regionkey', 'region.r_name', 'region.r_comment'], 
                        'Shared Hit Blocks': 0, 'Shared Read Blocks': 0, 'Shared Dirtied Blocks': 0, 'Shared Written Blocks': 0, 'Local Hit Blocks': 0, 'Local Read Blocks': 0, 
                        'Local Dirtied Blocks': 0, 'Local Written Blocks': 0, 'Temp Read Blocks': 0, 'Temp Written Blocks': 0, 'NodeID': 6, 'ParentNodeID': 4}], 
                        
                    5: [{'Node Type': 'Seq Scan', 
                        'Parent Relationship': 'Outer', 'Parallel Aware': False, 'Async Capable': False, 'Relation Name': 'region', 'Schema': 'public', 'Alias': 'region', 'Startup Cost': 0.0, 
                        'Total Cost': 11.7, 'Plan Rows': 170, 'Plan Width': 430, 'Actual Startup Time': 0.0, 'Actual Total Time': 0.0, 'Actual Rows': 0, 'Actual Loops': 0, 'Output': ['region.r_regionkey', 
                        'region.r_name', 'region.r_comment'], 'Shared Hit Blocks': 0, 'Shared Read Blocks': 0, 'Shared Dirtied Blocks': 0, 'Shared Written Blocks': 0, 'Local Hit Blocks': 0, 
                        'Local Read Blocks': 0, 'Local Dirtied Blocks': 0, 'Local Written Blocks': 0, 'Temp Read Blocks': 0, 'Temp Written Blocks': 0, 'NodeID': 7, 'ParentNodeID': 6}], 

                    3: [{'Node Type': 'Hash Join', 'Parent Relationship': 'Outer', 'Parallel Aware': False, 'Async Capable': False, 'Join Type': 'Inner', 'Startup Cost': 13.82, 
                         'Total Cost': 25.98, 'Plan Rows': 170, 'Plan Width': 864, 'Actual Startup Time': 0.0, 'Actual Total Time': 0.0, 'Actual Rows': 0, 'Actual Loops': 0, 'Output': 
                         ['nation.n_nationkey', 'nation.n_name', 'nation.n_regionkey', 'nation.n_comment', 'region.r_regionkey', 'region.r_name', 'region.r_comment'], 'Inner Unique': True, 
                         'Hash Cond': '(nation.n_regionkey = region.r_regionkey)', 'Shared Hit Blocks': 0, 'Shared Read Blocks': 0, 'Shared Dirtied Blocks': 0, 'Shared Written Blocks': 0, 
                         'Local Hit Blocks': 0, 'Local Read Blocks': 0, 'Local Dirtied Blocks': 0, 'Local Written Blocks': 0, 'Temp Read Blocks': 0, 'Temp Written Blocks': 0, 'NodeID': 4, 
                         'ParentNodeID': 3}], 
                         
                    2: [{'Node Type': 'Sort', 'Parent Relationship': 'Outer', 'Parallel Aware': False, 'Async Capable': False, 'Startup Cost': 32.28, 'Total Cost': 32.71, 
                        'Plan Rows': 170, 'Plan Width': 864, 'Actual Startup Time': 0.0, 'Actual Total Time': 0.0, 'Actual Rows': 0, 'Actual Loops': 0, 'Output': ['nation.n_nationkey', 
                        'nation.n_name', 'nation.n_regionkey', 'nation.n_comment', 'region.r_regionkey', 'region.r_name', 'region.r_comment'], 'Sort Key': ['nation.n_nationkey'], 'Shared Hit Blocks': 0, 
                        'Shared Read Blocks': 0, 'Shared Dirtied Blocks': 0, 'Shared Written Blocks': 0, 'Local Hit Blocks': 0, 'Local Read Blocks': 0, 'Local Dirtied Blocks': 0, 
                        'Local Written Blocks': 0, 'Temp Read Blocks': 0, 'Temp Written Blocks': 0, 'NodeID': 3, 'ParentNodeID': 2}], 
                        
                    0: [{'Node Type': 'Hash Join', 'Parallel Aware': False, 
                        'Async Capable': False, 'Join Type': 'Inner', 'Startup Cost': 34.83, 'Total Cost': 48.39, 'Plan Rows': 150, 'Plan Width': 1376, 'Actual Startup Time': 0.005, 
                        'Actual Total Time': 0.006, 'Actual Rows': 0, 'Actual Loops': 1, 'Output': ['nation.n_nationkey', 'nation.n_name', 'nation.n_regionkey', 'nation.n_comment', 
                        'region.r_regionkey', 'region.r_name', 'region.r_comment', 'supplier.s_suppkey', 'supplier.s_name', 'supplier.s_address', 'supplier.s_nationkey', 'supplier.s_phone', 
                        'supplier.s_acctbal', 'supplier.s_comment'], 'Inner Unique': False, 'Hash Cond': '(supplier.s_nationkey = nation.n_nationkey)', 'Shared Hit Blocks': 0, 
                        'Shared Read Blocks': 0, 'Shared Dirtied Blocks': 0, 'Shared Written Blocks': 0, 'Local Hit Blocks': 0, 'Local Read Blocks': 0, 'Local Dirtied Blocks': 0, 
                        'Local Written Blocks': 0, 'Temp Read Blocks': 0, 'Temp Written Blocks': 0, 'NodeID': 0, 'ParentNodeID': None}]}, 'additionalInfo': {'Shared Hit Blocks': 104, 
                        'Shared Read Blocks': 8, 'Shared Dirtied Blocks': 1, 'Shared Written Blocks': 0, 'Local Hit Blocks': 0, 'Local Read Blocks': 0, 'Local Dirtied Blocks': 0, 
                        'Local Written Blocks': 0, 'Temp Read Blocks': 0, 'Temp Written Blocks': 0, 'Ranking': [(('Seq Scan', 1), 11.5), (('Seq Scan', 5), 11.7), (('Seq Scan', 7), 11.7), 
                        (('Hash', 6), 11.7), (('Hash Join', 4), 25.98), (('Sort', 3), 32.71), (('Hash', 2), 32.71)]}
        }

    queryApp = QApplication([])
    queryWindow = QueryWindowGUI()
    # queryWindow = QueryWindowGUI(qepData["tree"])
    queryWindow.show()
    sys.exit(queryApp.exec())


