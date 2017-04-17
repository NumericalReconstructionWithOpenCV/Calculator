import Setting.DefineManager
import logging

def PrintLog(targetClassName = "Write Class Name", targetMethodName = "Write Method Name",
             logDescription = "Write Log Message", logLevel = Setting.DefineManager.LOG_LEVEL_DEBUG):
    logMessage = "{" + targetClassName + "} [" + targetMethodName + "] (" + logDescription + ")"
    logger = logging.getLogger()
    if logLevel == Setting.DefineManager.LOG_LEVEL_DEBUG:
        logger.setLevel(logging.DEBUG)
        logging.debug(logMessage)
    elif logLevel == Setting.DefineManager.LOG_LEVEL_INFO:
        logger.setLevel(logging.INFO)
        logging.info(logMessage)
    elif logLevel == Setting.DefineManager.LOG_LEVEL_WARN:
        logger.setLevel(logging.WARN)
        logging.warn(logMessage)
    elif logLevel == Setting.DefineManager.LOG_LEVEL_ERROR:
        logger.setLevel(logging.ERROR)
        logging.error(logMessage)
    else:
        logging.warn("{LogManager} [PrintLog] (Wrong Parameter Accepted)")