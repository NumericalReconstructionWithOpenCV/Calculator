import unittest

import cv2

from Setting import DefineManager
from Core import FindCorner, ObjectDetect
from Utils import FileIO


class ProjectSettingTest(unittest.TestCase):

    def TestVersionOfOpenCV(self):
        self.assertEqual(cv2.__version__, DefineManager.USE_OPENCV_VERSION, "Wrong Version Installed")

testSuite = unittest.TestSuite()
testSuite.addTest(ProjectSettingTest('TestVersionOfOpenCV'))
unittest.TextTestRunner(verbosity=2).run(testSuite)

beforeTargetImage = FileIO.LoadImage(DefineManager.TESTCASE_BEFORE_IMAGE_PATH)
afterTargetImage = FileIO.LoadImage(DefineManager.TESTCASE_AFTER_IMAGE_PATH)

ObjectDetect.DetectObjectFromImage(beforeTargetImage, afterTargetImage)

#FindCorner.FindCornerFromImage(Setting.DefineManager.FIND_CORNER_TESTCASE_PATH)
