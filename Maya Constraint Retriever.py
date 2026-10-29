import maya.cmds as cmds
from PySide2.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QLabel, QTableWidget, QTableWidgetItem


layout = QVBoxLayout()
conList = []
objectKids = []
tempCon = QTableWidgetItem()
tempPar = QTableWidgetItem()
tempChi = QTableWidgetItem()

class ConstraintUI(QDialog):

    def __init__(self, parent=None):
        super(ConstraintUI, self).__init__(parent)
        self.setWindowTitle("Maya Object Constraint Finder")

        self.objectLabel = QLabel("")
        self.errorLabel = QLabel("")

        self.runFinder = QPushButton("Find Constrained Objects")

        layout.addWidget(self.objectLabel)
        self.infoCompile()
        self.tableSetUp()
        self.dataSetUp()
        layout.addWidget(self.runFinder)
        layout.addWidget(self.errorLabel)
        

        self.runFinder.clicked.connect(self.infoCompile)
        self.parentName = 'if u see this i messed up'
        self.neededRows = 0
        
        
        self.setLayout(layout)
        self.rowNum = 0

    

    def tableSetUp(self):
        self.neededRows = len(conList)
        self.conTable = QTableWidget(self.neededRows, 3)
        self.conTable.setHorizontalHeaderLabels(['Constraint', 'Parent', 'Child'])
        layout.addWidget(self.conTable)

        for row in range(len(conList)):
            for col in range(3):
                self.conTable.setItem(row, col, QTableWidgetItem("({row+1},{col+1})"))

    def parentRetriever(self, constraint):
        tempVar = cmds.connectionInfo(constraint + '.target[0].targetParentMatrix',sfd=1)
        self.parentName = tempVar.rstrip('.parentMatrix[0]')

    def infoCompile(self):
        """
        Creates a list of dicts of the Parent, Child, and Constraint Name for each constraint relationship
        """
        objList = (cmds.ls(sl=True))
        for k in objList:
            objectKids = cmds.listConnections(k, d=0, s=1, type='constraint') or []
            objectKids = list(set(objectKids))
            for j in objectKids:
                self.parentRetriever(j)
                conList.append({"Parent": self.parentName, "Child": k, "Constraint": j})




    def dataSetUp(self):
        self.rowNum = 0
        for i in conList:
            self.conTable.setItem(self.rowNum, 0, QTableWidgetItem(i['Constraint']))
            self.conTable.setItem(self.rowNum, 1, QTableWidgetItem(i['Parent']))
            self.conTable.setItem(self.rowNum, 2, QTableWidgetItem(i['Child']))
            self.rowNum = self.rowNum +1
        print(self.rowNum)
        print("????????")

if __name__ == "__main__":
    conUI = ConstraintUI()
    conUI.show()
    

