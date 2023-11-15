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
)

"""
Global Parameters
"""
SQL_WINDOW_WIDTH = 300
SQL_WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1980
WINDOW_HEIGHT = 1600

"""
Main Application Window
"""
class QueryWindowGUI(QMainWindow):
    def __init__(self, parsedQepData):
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

        # Set the Various Windows required
        centralAppLayout.addWidget(SQLQueryWindow(), 0, 0)
        # scene = QGraphicsScene()
        centralAppLayout.addWidget(QEPTreeWindow(self.parsedQepData), 0, 1)
        centralAppLayout.addWidget(SQLQueryWindow(), 0, 2)
        centralAppLayout.addWidget(SQLQueryWindow(), 0, 3)

        scrollArea = QScrollArea()
        scrollArea.setAlignment(Qt.AlignmentFlag.AlignTop)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(centralWidget)

        self.setCentralWidget(scrollArea)

"""
Window 1 - Provide SQL Query from User
"""
class SQLQueryWindow(QWidget):
    def __init__(self):
        super().__init__(parent=None)

        # Initialisation of Components
        self.setWindowTitle("SQL Query")
        self.label = QLabel("Provide your SQL Query:")
        self.textEdit = QTextEdit()
        self.submitButton = QPushButton("Submit")

        # Attach an Event Listener to the Button
        self.submitButton.clicked.connect(self.submitHandler)

        # Set Dimensions & Alignment of Cursor
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.textEdit.setFixedWidth(SQL_WINDOW_WIDTH)
        self.textEdit.setFixedHeight(SQL_WINDOW_HEIGHT)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.textEdit, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.submitButton, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

    def submitHandler(self):
        # Retrieve User Text
        userInputQuery = self.textEdit.toPlainText()
        print("Extracted User Input: ", userInputQuery)

        # TODO Provide some backend logic to send the text to the backend

        # Clear the Text after Submission
        self.textEdit.clear()


"""
Helper Function to help Parse the JSON Object from PostgreSQL to build the QEP Tree
"""
def parse_qep_data(qepData):
    # Create an empty dictionary to store parsed information
    parsedData = {}

    # Iterate over the keys and values in the qep_data
    for key, value in qepData.items():
        # Check if the value is a nested dictionary
        if isinstance(value, dict):
            # Recursively parse the nested dictionary
            parsedData[key] = parse_qep_data(value)
        else:
            # Store the key-value pair in the parsed data
            parsedData[key] = value

    return parsedData


"""
Window 2 - Display the QEP Tree received from the Backend
"""
NODE_WIDTH = 380
NODE_HEIGHT = 120
NODE_HORIZONTAL_SPACING = 20
NODE_VERTICAL_SPACING = 100

class QEPTreeWindow(QGraphicsView):
    def __init__(self, parsedQepData, parent=None):
        super(QEPTreeWindow, self).__init__(parent)
        self.parsedQepData = parsedQepData

        # Create a Dictionary to Track Nodes with their Top and Bottom Coordinates
        self.topDict = {}
        self.bottomDict = {}

        # Set up the QGraphicsScene
        scene = QGraphicsScene(self)
        scene.setSceneRect(0, 0, WINDOW_HEIGHT, WINDOW_WIDTH)

        # Draw the QEP Tree
        self.drawQepTree(scene, self.parsedQepData, x=200, y=1000)

        # Set the scene for the view
        self.setScene(scene)
        scene.setBackgroundBrush(Qt.GlobalColor.white)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    """
    Plot a QEP Tree starting from the lowest level before moving to the root, where x and y are the initial starting coordinates
    """
    def drawQepTree(self, scene, parsedQepData, x, y):
        # x, y represents the coordinates of the top left corner of the rectangle
        currX = x
        currY = y
        firstIter = True

        # Iterate starting from the Root of the Tree
        for levelStr, nodesList in (parsedQepData.items()):
            # Get the Current Level as an int
            level = levelStr.count('0')

            # level represents the level of the tree, e.g. 0.0.0.0 is level 4, while nodes contains information about all nodes in the tree
            if not firstIter:
                # Went down a level
                currY += (NODE_HEIGHT + NODE_VERTICAL_SPACING)
            else:
                firstIter = False

            print(nodesList[0]["Node Type"])
            # TODO Iterate over all the nodes in this level (if there are more than 1
            # TODO Assume that there will be a list of nodes even when 1
            numNodesOnCurrLevel = len(nodesList)

            for index, node in enumerate(nodesList):
                if index != 0:
                    # As long as not first iter
                    # Determine the Location of the next Node on the same level, currY is constant on the same level
                    currX  = currX + NODE_WIDTH + NODE_HORIZONTAL_SPACING

                # Create a QGraphicsRectItem for the current node
                currNode = QGraphicsRectItem(currX, currY, NODE_WIDTH, NODE_HEIGHT)
        
                scene.addItem(currNode)

                # Create a QGraphicsTextItem to display node information at same place 
                nodeDesc = QGraphicsTextItem(self.retrieveNodeInfo(node))
                # Set the text color to black
                nodeDesc.setDefaultTextColor(Qt.GlobalColor.black)
                nodeDesc.setPos(currX, currY)
                scene.addItem(nodeDesc)

                # Draw line connecting parent and child nodes
                if level > 1:
                    # Parent Coordinates refer to the Bottom Middle of the Rectangle
                    parentX = currX + (NODE_WIDTH / 2) 
                    parentY = currY + NODE_HEIGHT

                    # TODO Determine the Coordinates of the Child Node
                    lineItem = QGraphicsLineItem(parentX, parentY, parentX, parentY + NODE_VERTICAL_SPACING)
                    scene.addItem(lineItem)

            if numNodesOnCurrLevel > 1:
                # Determine the Next Node Position on the Next Level
                # Adjust the position for the next node on the same level
                currX += (numNodesOnCurrLevel - 1) * (NODE_WIDTH + NODE_HORIZONTAL_SPACING)

            else:
                # Reset X back to the original spot since only 1 node
                currX = x

    def retrieveNodeInfo(self, nodeData):
        info = f"Node Type: {nodeData.get('Node Type', 'N/A')}\n"
        info += f"Cost: {nodeData.get('Total Cost', 'N/A')}\n"
        info += f"Output: {nodeData.get('Output', 'N/A')}\n"
        info += f"Group Key: {nodeData.get('Group Key', 'N/A')}\n"
        info += f"Rows: {nodeData.get('Actual Rows', 'N/A')}\n"
        info += f"Loops: {nodeData.get('Actual Loops', 'N/A')}"
        
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
    # TODO Changes made, convert all values to a list of nodes and all keys are strings
    qepData = {
        '0.0.0.0': [{'Node Type': 'Seq Scan', 'Parent Relationship': 'Outer', 'Parallel Aware': False, 'Async Capable': False, 'Relation Name': 'nation', 'Schema': 'public', 'Alias': 'nation', 'Startup Cost': 0.0, 'Total Cost': 12.12, 'Plan Rows': 1, 'Plan Width': 434, 'Actual Startup Time': 0.014, 'Actual Total Time': 0.018, 'Actual Rows': 1, 'Actual Loops': 1, 'Output': ['n_nationkey', 'n_name', 'n_regionkey', 'n_comment'
            ], 'Filter': "(nation.n_name = 'ALGERIA'::bpchar)", 'Rows Removed by Filter': 24, 'Shared Hit Blocks': 1, 'Shared Read Blocks': 0, 'Shared Dirtied Blocks': 0, 'Shared Written Blocks': 0, 'Local Hit Blocks': 0, 'Local Read Blocks': 0, 'Local Dirtied Blocks': 0, 'Local Written Blocks': 0, 'Temp Read Blocks': 0, 'Temp Written Blocks': 0
        }], 
        '0.0.0': [{'Node Type': 'Sort', 'Parent Relationship': 'Outer', 'Parallel Aware': False, 'Async Capable': False, 'Startup Cost': 12.13, 'Total Cost': 12.14, 'Plan Rows': 1, 'Plan Width': 434, 'Actual Startup Time': 0.022, 'Actual Total Time': 0.023, 'Actual Rows': 1, 'Actual Loops': 1, 'Output': ['n_nationkey', 'n_name', 'n_regionkey', 'n_comment'
            ], 'Sort Key': ['nation.n_nationkey'
            ], 'Sort Method': 'quicksort', 'Sort Space Used': 25, 'Sort Space Type': 'Memory', 'Shared Hit Blocks': 1, 'Shared Read Blocks': 0, 'Shared Dirtied Blocks': 0, 'Shared Written Blocks': 0, 'Local Hit Blocks': 0, 'Local Read Blocks': 0, 'Local Dirtied Blocks': 0, 'Local Written Blocks': 0, 'Temp Read Blocks': 0, 'Temp Written Blocks': 0
        }], 
        '0.0': [{'Node Type': 'Group', 'Parent Relationship': 'Outer', 'Parallel Aware': False, 'Async Capable': False, 'Startup Cost': 12.13, 'Total Cost': 12.14, 'Plan Rows': 1, 'Plan Width': 434, 'Actual Startup Time': 0.024, 'Actual Total Time': 0.025, 'Actual Rows': 1, 'Actual Loops': 1, 'Output': ['n_nationkey', 'n_name', 'n_regionkey', 'n_comment'
            ], 'Group Key': ['nation.n_nationkey'
            ], 'Shared Hit Blocks': 1, 'Shared Read Blocks': 0, 'Shared Dirtied Blocks': 0, 'Shared Written Blocks': 0, 'Local Hit Blocks': 0, 'Local Read Blocks': 0, 'Local Dirtied Blocks': 0, 'Local Written Blocks': 0, 'Temp Read Blocks': 0, 'Temp Written Blocks': 0
        }],
        '0': [{'Node Type': 'Sort', 'Parallel Aware': False, 'Async Capable': False, 'Startup Cost': 12.15, 'Total Cost': 12.16, 'Plan Rows': 1, 'Plan Width': 434, 'Actual Startup Time': 0.051, 'Actual Total Time': 0.052, 'Actual Rows': 1, 'Actual Loops': 1, 'Output': ['n_nationkey', 'n_name', 'n_regionkey', 'n_comment'
            ], 'Sort Key': ['nation.n_regionkey'
            ], 'Sort Method': 'quicksort', 'Sort Space Used': 25, 'Sort Space Type': 'Memory', 'Shared Hit Blocks': 4, 'Shared Read Blocks': 0, 'Shared Dirtied Blocks': 0, 'Shared Written Blocks': 0, 'Local Hit Blocks': 0, 'Local Read Blocks': 0, 'Local Dirtied Blocks': 0, 'Local Written Blocks': 0, 'Temp Read Blocks': 0, 'Temp Written Blocks': 0
        }]
    }

    queryApp = QApplication([])
    queryWindow = QueryWindowGUI(qepData)
    queryWindow.show()
    sys.exit(queryApp.exec())


