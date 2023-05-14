import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import paho.mqtt.client as mqtt
import re
import sys


class LocalData(object):
  records = {}

class HTTPRequestHandler(BaseHTTPRequestHandler):
  def do_POST(self):
    if re.search('/api/post/*', self.path):
      length = int(self.headers.get('content-length'))
      data = self.rfile.read(length).decode('utf8')

      record_id = self.path.split('/')[-1]
      LocalData.records[record_id] = data

      logger.debug('Set \"{0}\": value: {1}'.format(record_id, data))
      t_dictionary = json.loads(data)
      logger.debug(t_dictionary)
      for key in t_dictionary:
        logger.debug('/burk38k7/{0}/{1}={2}'.format(record_id, key,t_dictionary[key]))
        mqtt_client.publish('/burk38k7/{0}/{1}'.format(record_id, key),str(t_dictionary[key]))
      self.send_response(200)
    else:
      self.send_response(403)
    self.end_headers()

  def do_GET(self):
    if re.search('/api/get/*', self.path):
      record_id = self.path.split('/')[-1]
      if record_id in LocalData.records:
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        # Return json, even though it came in as POST URL params
        data = json.dumps(LocalData.records[record_id]).encode('utf-8')
        logger.debug('Get \"{0}\" value: {1}'.format(record_id, data))
        self.wfile.write(data)
      else:
        self.send_response(404, 'Not Found: record does not exist')
    else:
      self.send_response(403)
    self.end_headers()

parser = argparse.ArgumentParser(prog=os.path.basename(__file__), description='Simple HTTP server for receiving data and then sending to MQTT.')
parser.add_argument('--port', metavar='port', type=int, default=8000,
          help='HTTP server port')
pargs = parser.parse_args()

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

global logger
global mqtt_client
logger = get_logger()
mqtt_client = mqtt.Client("P1")

if __name__ == '__main__':
  server = HTTPServer(('', pargs.port), HTTPRequestHandler)
  logger.debug('Starting httpd...')
  try:
    broker_address="127.0.0.1" 
    mqtt_client.connect(broker_address)
    server.serve_forever()
  except KeyboardInterrupt:
    logger.debug('Interrupted from keyboard')
    pass
  finally:
    logger.debug('Stopping httpd...')
    server.server_close()
    