import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import paho.mqtt.client as mqtt
import re
import sys
from _version import __version__


class LocalData(object):
  records = {}

class HTTPRequestHandler(BaseHTTPRequestHandler):
  def do_POST(self):
    if re.search('/api/post/*', self.path):
      length = int(self.headers.get('content-length'))
      data = self.rfile.read(length).decode('utf8')
      logger.debug('HTTP: Recieved POST at {0}. Payload: {1}'.format(self.path, data))

      topic_id = self.path.split('api/post')[1]
      LocalData.records[topic_id] = json.loads(data)
      logger.debug('LocalData: Put {0} to {1}'.format(data,topic_id))

      for value in LocalData.records[topic_id]:
        logger.debug('MQTT: Sending {0} to {1}/{2}'.format(LocalData.records[topic_id][value], topic_id, value))
        mqtt_client.publish('{0}/{1}'.format(topic_id, value),LocalData.records[topic_id][value])
      self.send_response(200)
    else:
      logger.debug('HTTP: Incorrect path')
      self.send_response(403)
    self.end_headers()

  def do_GET(self):
    if re.search('/api/get/*', self.path):
      topic_id = self.path.split('api/get')[1]
      logger.debug('HTTP: Recieved GET at {0}. Payload: {1}'.format(self.path, data))
      if topic_id in LocalData.records:
        logger.debug('LocalData: Data found')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        # Return json, even though it came in as POST URL params
        data = json.dumps(LocalData.records[topic_id]).encode('utf-8')
        logger.debug('LocalData: Get {0} from {1}'.format(data,topic_id))
        self.wfile.write(data)
      else:
        logger.debug('LocalData: Data not found')
        self.send_response(404, 'Not Found: record does not exist')
    else:
      logger.debug('HTTP: Incorrect path')
      self.send_response(403)
    self.end_headers()

def get_logger():
  logname = '{0}.log'.format(os.path.basename(__file__).split('.')[0])
  logger = logging.getLogger()
  logger.handlers.clear()

  rootFormatter = logging.Formatter('%(filename)-17.17s:%(lineno)-4s %(asctime)-15s [%(levelname)-5.5s]: %(message)-s')

  handlerStdout = logging.StreamHandler(sys.stdout)
  handlerStdout.setFormatter(rootFormatter)

  handlerFile = logging.handlers.TimedRotatingFileHandler(logname, when='midnight', backupCount=int(10))

  handlerFile.setFormatter(rootFormatter)

  logger.handlers.append(handlerStdout)
  logger.handlers.append(handlerFile)
  logger.setLevel("DEBUG")

  return logging.getLogger()

def get_mqtt_client():
  logger.debug('MQTT: Creating client')
  mqtt_client = mqtt.Client('mqtt_server')
  broker_address="172.21.0.2"
  logger.debug('MQTT: Connecting to {0}...'.format(broker_address))
  try:
    mqtt_client.connect(broker_address)
    logger.debug('MQTT: Connected')
  except BaseException as e:
    logger.exception('MQTT: An error occured during the connection. Application will shut down')
    sys.exit(1)

  return mqtt_client

parser = argparse.ArgumentParser(prog=os.path.basename(__file__), description='Simple HTTP server for receiving data and then sending to MQTT.')
parser.add_argument('-v', '--version', action='version',
                    version='%(prog)s {version}'.format(version=__version__))
pargs = parser.parse_args()


if __name__ == '__main__':
  logger = get_logger()
  logger.debug('APP: Started')
  mqtt_client = get_mqtt_client()
  server = HTTPServer(('', 8000), HTTPRequestHandler)

  try:
    logger.debug('HTTP: Starting httpd...')
    server.serve_forever()
  except KeyboardInterrupt:
    logger.debug('APP: Interrupted from keyboard')
  finally:
    logger.debug('HTTP: Stopping httpd...')
    server.server_close()
    logger.debug('APP: Finished')
