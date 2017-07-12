
import sys, os, copy, csv, re, pdb, time, subprocess
import numpy as np 

from openravepy import *
curdir = os.path.dirname(os.path.realpath(__file__))
classdir = curdir +'/../InterpolateGrasps/'
sys.path.insert(0, classdir) # path to helper classes
from Visualizers import Vis, GenVis, HandVis, ObjectGenericVis

TWOFER_ANGLES = np.array([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
CLAW_ANGLES = np.array([0,0,np.pi/4,0,0,np.pi/4,0,0,0,0])
PINCH_ANGLES = np.array([0,0,np.pi/2,0,0,np.pi/2,0,0,0,0])
CUP_ANGLES = np.array([0,0,np.pi,0,0,np.pi,0,0,0,0])


class HandView(object):
	def __init__(self):
		self.vis = Vis()
		self.vis.setCamera(60,7*np.pi/8,0)
		self.Hand = HandVis(self.vis)
		self.Hand.loadHand()
		self.Hand.changeColor('blueI')
		self.setGrasp("The Claw")

		self.Obj = ObjectGenericVis(self.vis)
		self.Obj.loadObject('cube',3,3,3,None)  # TODO: Object with larger extent!
		self.Obj.changeColor('greenI')
		self.setObjectOffset(-.075 - (float(self.Obj.e)/100) - .02)
		self.setWristRotation(0)
		
	def setObjectOffset(self, newOffset):
		self.offset = float(newOffset) # offset to have clearance between palm and object
		self.Hand.localTranslation(np.array([0, 0,self.offset]))

	def setWristRotation(self, rotation):
		angle = float(rotation)/16
		rot = matrixFromAxisAngle([0,0, angle])
		self.Hand.localRotation(rot)

	def setObject(self, newObj):
		if newObj == "Cone":
			self.Obj.loadObject('cone',3,3,3,10)
			self.Obj.changeColor('greenI')
		elif newObj == "Cube":
			self.Obj.loadObject('cube',3,3,3,None)
			self.Obj.changeColor('greenI')
		elif newObj == "Cylinder":
			self.Obj.loadObject('cylinder',3,3,3,None)
			self.Obj.changeColor('greenI')
		elif newObj == "Ellipse":
			self.Obj.loadObject('ellipse',3,3,3,None)
			self.Obj.changeColor('greenI')

	def setGrasp(self, newGrasp):
		if newGrasp == "The Two-fer":
			self.grasp = TWOFER_ANGLES
		elif newGrasp == "The Claw":
			self.grasp = CLAW_ANGLES
		elif newGrasp == "The Pinch":
			self.grasp = PINCH_ANGLES
		elif newGrasp == "The Cup":
			self.grasp = CUP_ANGLES
		self.showGrasp()
		return self.grasp

	def showGrasp (self):
		self.Hand.setJointAngles(self.grasp)

	def changeFingerPosition(self, finger, newValue):
		if finger == 1:
			self.grasp[3] = 2.44*newValue/100
			self.grasp[4] = .837*newValue/100
		elif finger == 2:
			self.grasp[6] = 2.44*newValue/100
			self.grasp[7] = .837*newValue/100
		elif finger ==3:
			self.grasp[8] = 2.44*newValue/100
			self.grasp[9] = .837*newValue/100
		self.showGrasp()
		return self.grasp