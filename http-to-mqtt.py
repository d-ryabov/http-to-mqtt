
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--httpd', metavar='httpd', type=int, default=8000,
                    help='HTTP server port')
pargs = parser.parse_args()

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
  server_address = ('', pargs.httpd)
  httpd = server_class(server_address, handler_class)
  try:
      httpd.serve_forever()
  except KeyboardInterrupt:
      httpd.server_close()