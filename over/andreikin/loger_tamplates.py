
import logging
#logger.manager.loggerDict = {}
#logger.handlers = []
logging.basicConfig( format="[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)# WARNING  DEBUG

#logger.warning("Enter in if condition")

