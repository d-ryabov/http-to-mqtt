import logging
import os
import sys

def get_logger(name):
  logname = '{0}.log'.format(os.path.basename(__file__).split('.')[0])
  logger = logging.getLogger(name)
  logger.handlers.clear()

  rootFormatter = logging.Formatter('%(filename)-17.17s:%(lineno)-4s %(asctime)-15s [%(levelname)-5.5s]: %(message)-s')

  handlerStdout = logging.StreamHandler(sys.stdout)
  handlerStdout.setFormatter(rootFormatter)

  handlerFile = logging.handlers.TimedRotatingFileHandler(logname, when='midnight', backupCount=int(10))

  handlerFile.setFormatter(rootFormatter)

  logger.handlers.append(handlerStdout)
  logger.handlers.append(handlerFile)
  logger.setLevel("INFO")

  return logging.getLogger()