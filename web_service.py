import json
import os
import sys
import logging
import uuid

from socketserver import TCPServer
from http.server import BaseHTTPRequestHandler, HTTPServer
from multiprocessing import Queue


logger = logging.getLogger(__name__)

def create_handler_class(q):
    class QueueHandler(BaseHTTPRequestHandler):

        def __init__(self, request, client_address, server):
            super().__init__(request, client_address, server)
            self.q = q

        def _set_headers(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        def do_POST(self):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            json_data = self._get_response_dict(post_data)
            json_data['id'] = self._get_id()
            self._add_to_queue(json_data)
            self._set_headers()
            self.wfile.write(bytes('Queued', 'UTF-8'))

        def _get_response_dict(self, post_data):
            post_data_str = post_data.decode('UTF-8')
            return json.loads(post_data_str)

        def _add_to_queue(self, json_data):
            q.put(json_data)

        def _get_id(self):
            return uuid.uuid4().hex

    return QueueHandler

def run(q, port, logs_directory):

    if not logs_directory:
        logger.addHandler(logging.StreamHandler(sys.stdout))
    else:
        log_path = os.path.join(args.logs_directory, "mailer.log")
        logger.addHandler(logging.FileHandler(log_path))

    server_address = ('', port)
    handler_class = create_handler_class(q)
    httpd = TCPServer(server_address, handler_class)
    httpd.serve_forever()
