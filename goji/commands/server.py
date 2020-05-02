import os
from gevent.pywsgi import WSGIServer
import goji.server

def server(args):
  http_server = WSGIServer(('', 8080), goji.server.app)
  http_server.serve_forever()

def command_server(args):
  server(args)

