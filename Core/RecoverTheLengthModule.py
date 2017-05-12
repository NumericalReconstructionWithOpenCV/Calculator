from Setting import DefineManager
from Utils import CustomOpenCV
import cv2

def GetFunctionCrossPosition(functionParameter):
    print "GetFunctionCrossPosition"
    beforeFunctionParameter = []
    crossPositionData = []
    for eachFunctionParameter in functionParameter:
        # 1x + 2 = y
        # -2x + 4 = y
        # 1x + 2 = -2x + 4
        # 3x = 2
        # x = 2/3
        # y = 8/3
        if beforeFunctionParameter != []:
            position = DefineManager.ZERO_POSITION
            position = CalculateCrossPosition(beforeFunctionParameter, eachFunctionParameter)
            crossPositionData.append(position)
        beforeFunctionParameter = eachFunctionParameter

    position = CalculateCrossPosition(beforeFunctionParameter, functionParameter[DefineManager.ZERO])
    crossPositionData.append(position)
    return crossPositionData

def CalculateCrossPosition(beforeParameter, afterParameter):
    position = DefineManager.ZERO_POSITION
    position[DefineManager.X_POSITION_SAVE_POINT] = (beforeParameter[DefineManager.CONSTANT_VALUE_SAVE_POINT] - afterParameter[DefineManager.CONSTANT_VALUE_SAVE_POINT]) / (beforeParameter[DefineManager.INCLINATION_SAVE_POINT] - afterParameter[DefineManager.INCLINATION_SAVE_POINT])
    position[DefineManager.Y_POSITION_SAVE_POINT] = beforeParameter[DefineManager.INCLINATION_SAVE_POINT] * position[DefineManager.X_POSITION_SAVE_POINT] + beforeParameter[DefineManager.CONSTANT_VALUE_SAVE_POINT]
    print position
    return position

def DrawPointToImage(positionData, imageData):
    print "DrawPointToImage"
    for eachPosition in positionData:
        cv2.circle(imageData, (int(eachPosition[DefineManager.X_POSITION_SAVE_POINT]), int(eachPosition[DefineManager.Y_POSITION_SAVE_POINT])),
                   2, DefineManager.RGB_COLOR_RED, -1)
    CustomOpenCV.ShowImagesWithName([imageData])