import maya.cmds as cmds
import random
from PySide2.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QDoubleSpinBox, QCheckBox

#Design window
class RandomizerUI(QDialog):

    def __init__(self, parent=None):
        super(RandomizerUI, self).__init__(parent)
        self.setWindowTitle("Maya Object Randomizer")

        #Create Widgets
        self.runButton = QPushButton("Press to Randomize!")
        
        #Create min value spinboxes
        self.minX = QDoubleSpinBox()
        self.minX.setRange(-99, 99)
        self.minY = QDoubleSpinBox()
        self.minY.setRange(-99, 99)
        self.minZ = QDoubleSpinBox()
        self.minZ.setRange(-99, 99)

        #Create max value spinboxes
        self.maxX = QDoubleSpinBox()
        self.maxX.setRange(-99, 99)
        self.maxY = QDoubleSpinBox()
        self.maxY.setRange(-99, 99)
        self.maxZ = QDoubleSpinBox()
        self.maxZ.setRange(-99, 99)

        #Create labels for min value spinboxes
        self.textMinX = QLabel("Enter in the minimum X value")
        self.textMinY = QLabel("Enter in the minimum Y value")
        self.textMinZ = QLabel("Enter in the minimum Z value")

        #Create labels for max value spinboxes
        self.textMaxX = QLabel("Enter in the maximum X value")
        self.textMaxY = QLabel("Enter in the maximum Y value")
        self.textMaxZ = QLabel("Enter in the maximum Z value")

        #Create checkboxes to not randomise a positional value
        self.xCheck = QCheckBox("Don't randomize X")
        self.yCheck = QCheckBox("Don't randomize Y")
        self.zCheck = QCheckBox("Don't randomize Z")

        #Create weighted value spinboxes and labels
        self.weightX = QDoubleSpinBox()
        self.weightX.setRange(-99, 99)
        self.textWeightX = QLabel("Enter the weighted value for X")
        self.weightY = QDoubleSpinBox()
        self.weightY.setRange(-99, 99)
        self.textWeightY = QLabel("Enter the weighted value for Y")
        self.weightZ = QDoubleSpinBox()
        self.weightZ.setRange(-99, 99)
        self.textWeightZ = QLabel("Enter the weighted value for Z")
        self.triCheck = QCheckBox("Use randomization weighting?")
        self.triExplain = QLabel("This will result in the random value being closer the the entered number")
        self.triExplain2 = QLabel("Ignore the weighted value boxes if you leave this unticked")

        #Create a label used for displaying errors
        self.errorOutput = QLabel("")

        #Organize Layouts
        layout = QVBoxLayout()
        
        #Explain weighted values to user
        layout.addWidget(self.triCheck)
        layout.addWidget(self.triExplain)
        layout.addWidget(self.triExplain2)

        #Organize X Values
        layout.addWidget(self.textMinX)
        layout.addWidget(self.minX)
        layout.addWidget(self.textMaxX)
        layout.addWidget(self.maxX)
        layout.addWidget(self.textWeightX)
        layout.addWidget(self.weightX)

        #Organize Y Values
        layout.addWidget(self.textMinY)
        layout.addWidget(self.minY)
        layout.addWidget(self.textMaxY)
        layout.addWidget(self.maxY)
        layout.addWidget(self.textWeightY)
        layout.addWidget(self.weightY)

        #Organize Z Values
        layout.addWidget(self.textMinZ)
        layout.addWidget(self.minZ)
        layout.addWidget(self.textMaxZ)
        layout.addWidget(self.maxZ)
        layout.addWidget(self.textWeightZ)
        layout.addWidget(self.weightZ)

        #Adds weighted value checkboxes
        layout.addWidget(self.xCheck)
        layout.addWidget(self.yCheck)
        layout.addWidget(self.zCheck)
        
        #Add button and hidden error label
        layout.addWidget(self.runButton)
        layout.addWidget(self.errorOutput)

        self.setLayout(layout)

        #Connections button click to function
        self.runButton.clicked.connect(self.positionalRandomizer)

    #Function to randomise object positions
    def positionalRandomizer(self):
        #Retrieve all objects selected
        objects = cmds.ls(sl=True)

        #Clear error label
        self.errorOutput.setText("")

        #Store spinbox values in variables
        minXValue = self.minX.value()
        minYValue = self.minY.value()
        minZValue = self.minZ.value()

        maxXValue = self.maxX.value()
        maxYValue = self.maxY.value()
        maxZValue = self.maxZ.value()

        #Calculate weighted values that don't impact the randomisation if user selects to not use them
        if (self.triCheck.isChecked() == False):
            meanX = (minXValue + maxXValue)/2
            meanY = (minXValue + maxXValue)/2
            meanZ = (minXValue + maxXValue)/2
        else:
            meanX = self.weightX.value()
            meanY = self.weightY.value()
            meanZ = self.weightZ.value()

        #Checking which positional values wont be altered
        checkingX = self.xCheck.isChecked()
        checkingY = self.yCheck.isChecked()
        checkingZ = self.zCheck.isChecked()

        #If statements to catch possible errors
        if (minXValue > maxXValue) or (minYValue > maxYValue) or (minZValue > maxZValue):
            self.errorOutput.setText("ERROR! One of your minimum values is higher than the corresponding maximum value")
        elif (meanX < minXValue) or (meanY < minYValue) or (meanZ < minZValue):
            self.errorOutput.setText("ERROR! One of your weighted values is lower than the corresponding minimum value")
        elif (meanX > maxXValue) or (meanY > maxYValue) or (meanZ > maxZValue):
            self.errorOutput.setText("ERROR! One of your weighted values is higher than the corresponding maximum value")
        else:
            for j in objects:
                if (checkingX != True): cmds.setAttr(j + ".translateX", random.triangular(minXValue, maxXValue, meanX))
                if (checkingY != True): cmds.setAttr(j + ".translateY", random.triangular(minYValue, maxYValue, meanY))
                if (checkingZ != True): cmds.setAttr(j + ".translateZ", random.triangular(minZValue, maxZValue, meanZ))


randUI = RandomizerUI()
randUI.show()