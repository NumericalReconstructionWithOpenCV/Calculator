import cv2
import unittest
import ObjectDetect as objectDetect
import FindCorner
import Setting.DefineManager

class ProjectSettingTest(unittest.TestCase):

    def TestVersionOfOpenCV(self):
        self.assertEqual(cv2.__version__, Setting.DefineManager.USE_OPENCV_VERSION, "Wrong Version Installed")

testSuite = unittest.TestSuite()
testSuite.addTest(ProjectSettingTest('TestVersionOfOpenCV'))
unittest.TextTestRunner(verbosity=2).run(testSuite)

objectDetect.DetectObjectFromImage(Setting.DefineManager.OBJECT_DETECT_TESTCASE_PATH)
FindCorner.FindCornerFromImage(Setting.DefineManager.FIND_CORNER_TESTCASE_PATH)
