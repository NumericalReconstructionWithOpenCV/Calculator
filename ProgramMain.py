import cv2
import unittest2 as unittest
import FileIO as fileIO
from matplotlib import pyplot as plt

print "Hello World, We will check your project Setting"

class ProjectSettingTest(unittest.TestCase):

    def TestVersionOfOpenCV(self):
        self.assertEqual(cv2.__version__, "3.2.0", "Wrong Version Installed")

class ProjectCalculateLength(unittest.TestCase):

    def ImageLoadTest(self):
        self.assertNotEqual(fileIO.LoadImage("Resources/beforeImage.png"), None)

testSuite = unittest.TestSuite()
testSuite.addTest(ProjectSettingTest('TestVersionOfOpenCV'))
testSuite.addTest(ProjectCalculateLength('ImageLoadTest'))
unittest.TextTestRunner(verbosity=2).run(testSuite)