import os
from gevent.pywsgi import WSGIServer
import goji.server
from goji.logger import log

def server(args):
  http_server = WSGIServer(('', 8080), goji.server.app)
  http_server.serve_forever()
  logging.setLogger(log)

def command_server(args):
  server(args)

