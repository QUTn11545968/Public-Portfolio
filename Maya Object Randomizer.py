#Creating a version of the face randomizer for just a single selected object for testing

import maya.cmds as cmds
import random

#when not using [0] maybe just use a for objectName loop
objectName = cmds.ls(sl=True) 
#Count the number of faces of selected object
faceNum = 0
faceList = []


def scaleRandomiser (theObject, lowScale, highScale):
    cmds.select(clear = True)
    cmds.select(theObject)
    cmds.scale(random.uniform(lowScale, highScale),random.uniform(lowScale, highScale),random.uniform(lowScale, highScale), relative = True)


def rotateRandomiser (theObject, lowRotate, highRotate):
    cmds.select(clear = True)
    cmds.select(theObject)
    cmds.rotate(random.uniform(lowRotate, highRotate),random.uniform(lowRotate, highRotate),random.uniform(lowRotate, highRotate), relative = True)


def faceRandomiser (theObject, PercentOfFace, highThick):
    cmds.select(clear = True)
    cmds.select(theObject)
    faceNum = int(cmds.polyEvaluate(fc=True))

    #Iterate through the object's faces and add them to the list
    while faceNum > 0: 
        faceList.append('{}.f[{}]'.format(theObject, faceNum))
        faceNum = faceNum - 1

    #Count how many items are in the list of faces, return as a float
    facePercentage = float(len(faceList))
    #Using the percent value, calculate how many faces are going to be selecetd
    facePercentage = facePercentage * PercentOfFace
    #Round number and convert to int
    facePercentage = int(round(facePercentage))

    #gets a random selection of faces equal to facePercentage
    percentList = random.sample(faceList, facePercentage)


    while percentList != []:
        try:
            cmds.polyExtrudeFacet(percentList[-1], thickness = (random.uniform(0, highThick)))
            percentList.pop(-1)
        except:
            percentList.pop(-1)


def finishingTouches(theObject):
    cmds.polySmooth(theObject, divisions=2)
    cmds.polyRemesh(theObject, maxEdgeLength=0.5, collapseThreshold=30, smoothStrength = 0.3)

#Counts the number of faces, but is 1 higher than iterator's final number because lists start from [0]
numObjects = int(len(objectName))
#Created because I couldn't use i as a int
iterator = 0

def objectLoop():
    while numObjects > iterator:
        scaleRandomiser(objectName[iterator], 0.7, 1.3)
        rotateRandomiser(objectName[iterator], 0, 90)
        faceRandomiser(objectName[iterator], 0.6, 0.05)
        finishingTouches(objectName[iterator])
        iterator = iterator + 1

objectLoop()
