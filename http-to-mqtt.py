import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import log
import re
import os


class LocalData(object):
  records = {}

class HTTPRequestHandler(BaseHTTPRequestHandler):
  def __init__(self):
    self.logger = log.get_logger('main')

  def do_POST(self):
    if re.search('/api/post/*', self.path):
      length = int(self.headers.get('content-length'))
      data = self.rfile.read(length).decode('utf8')

      record_id = self.path.split('/')[-1]
      LocalData.records[record_id] = data

      self.logger.info('Set \"{0}\": \"{1}\"'.format(record_id, data))
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
        self.logger.info('Get \"{0}\": \"{1}\"'.format(record_id, data))
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

    
if __name__ == '__main__':
  #logger = log.get_logger('main')
  server = HTTPServer(('', pargs.port), HTTPRequestHandler)
  #logger.info('Starting httpd...')
  try:
    server.serve_forever()
  except KeyboardInterrupt:
    #logger.info('Interrupted from keyboard')
    pass
  finally:
    #logger.info('Stopping httpd...')
    server.server_close()
    