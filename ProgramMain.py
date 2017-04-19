import unittest

import cv2

import Setting.DefineManager
from Core import FindCorner, ObjectDetect


class ProjectSettingTest(unittest.TestCase):

    def TestVersionOfOpenCV(self):
        self.assertEqual(cv2.__version__, Setting.DefineManager.USE_OPENCV_VERSION, "Wrong Version Installed")

testSuite = unittest.TestSuite()
testSuite.addTest(ProjectSettingTest('TestVersionOfOpenCV'))
unittest.TextTestRunner(verbosity=2).run(testSuite)

ObjectDetect.DetectObjectFromImage(Setting.DefineManager.OBJECT_DETECT_TESTCASE_PATH)
FindCorner.FindCornerFromImage(Setting.DefineManager.FIND_CORNER_TESTCASE_PATH)
