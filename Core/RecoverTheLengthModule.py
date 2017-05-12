from Setting import DefineManager
from Utils import CustomOpenCV
import cv2
import numpy as np

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
        if len(beforeFunctionParameter) > 0:
            position = CalculateCrossPosition(beforeFunctionParameter, eachFunctionParameter)
            crossPositionData.append(np.copy(position))
        beforeFunctionParameter = np.copy(eachFunctionParameter)

    position = CalculateCrossPosition(beforeFunctionParameter, functionParameter[DefineManager.ZERO])
    crossPositionData.append(position)
    return crossPositionData

def CalculateCrossPosition(beforeParameter, afterParameter):
    position = DefineManager.ZERO_POSITION
    position[DefineManager.X_POSITION_SAVE_POINT] = -(beforeParameter[DefineManager.CONSTANT_VALUE_SAVE_POINT] - afterParameter[DefineManager.CONSTANT_VALUE_SAVE_POINT]) / ( beforeParameter[DefineManager.INCLINATION_SAVE_POINT] - afterParameter[DefineManager.INCLINATION_SAVE_POINT])
    position[DefineManager.Y_POSITION_SAVE_POINT] = beforeParameter[DefineManager.INCLINATION_SAVE_POINT] * position[DefineManager.X_POSITION_SAVE_POINT] + beforeParameter[DefineManager.CONSTANT_VALUE_SAVE_POINT]
    #print position
    return position

def DrawPointToImage(positionData, imageData):
    print "DrawPointToImage"
    drawImage = np.copy(imageData)
    height, width = drawImage.shape[:2]
    index = 0
    for eachPosition in positionData:
        if eachPosition[DefineManager.X_POSITION_SAVE_POINT] < 0 or eachPosition[DefineManager.Y_POSITION_SAVE_POINT] < 0 :
            continue
        if eachPosition[DefineManager.X_POSITION_SAVE_POINT] >= width or eachPosition[DefineManager.Y_POSITION_SAVE_POINT] >= height:
            continue
        cv2.circle(imageData, (int(eachPosition[DefineManager.X_POSITION_SAVE_POINT]), int(eachPosition[DefineManager.Y_POSITION_SAVE_POINT])),
                   2, DefineManager.RGB_COLOR_RED, -1)
        cv2.putText(imageData, str(index), (int(eachPosition[DefineManager.X_POSITION_SAVE_POINT]), int(eachPosition[DefineManager.Y_POSITION_SAVE_POINT])),
                    cv2.FONT_HERSHEY_COMPLEX,0.3,DefineManager.RGB_COLOR_WHITE)
        index = index + 1
    CustomOpenCV.ShowImagesWithName([imageData])