import cv2
import unittest
import FileIO as fileIO
import ObjectDetect as objectDetect
import FindCorner
from matplotlib import pyplot as plt
import numpy as np

class ProjectSettingTest(unittest.TestCase):

    def TestVersionOfOpenCV(self):
        self.assertEqual(cv2.__version__, "3.2.0", "Wrong Version Installed")

class ProjectCalculateLength(unittest.TestCase):
    def TestingDetecting(self):
        objectDetect.Detecting()

    def MakeBlankImage(self):
        global blankImage
        blankImage = np.zeros((1280, 720, 3), np.uint8)

    def BeforeImageLoadTest(self):
        global beforeImage, blankImage
        beforeImage = "Resources/testcase4/before.png"
        self.assertNotEqual(beforeImage, blankImage)

    def AfterImageLoadTest(self):
        global afterImage, blankImage
        afterImage = "Resources/testcase4/after.png"
        self.assertNotEqual(afterImage, blankImage)

    def ObjectDetectFromImage(self):
        global beforeImage, afterImage, blankImage
        objectDetect.DetectObjectFromImage("Resources/testcase5/")

    def FindCornerFromImage(self):
        FindCorner.FindCornerFromImage("Resources/testcase7/")

testSuite = unittest.TestSuite()
testSuite.addTest(ProjectSettingTest('TestVersionOfOpenCV'))
testSuite.addTest(ProjectCalculateLength('MakeBlankImage'))
testSuite.addTest(ProjectCalculateLength('BeforeImageLoadTest'))
testSuite.addTest(ProjectCalculateLength('AfterImageLoadTest'))
testSuite.addTest(ProjectCalculateLength('ObjectDetectFromImage'))
testSuite.addTest(ProjectCalculateLength('FindCornerFromImage'))
#testSuite.addTest(ProjectCalculateLength('TestingDetecting'))
unittest.TextTestRunner(verbosity=2).run(testSuite)