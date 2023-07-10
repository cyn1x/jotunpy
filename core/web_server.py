import os
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from core.config import CONFIG
from core.event import BUFFER_EVENT


class Server(SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=CONFIG['IO']['OUTPUT_DIR'], **kwargs)

    def do_GET(self):
        # Handle search requests
        if self.path.startswith('/search/'):
            uri = self.path.split('/search')[1]
            file_path = self.translate_path(uri)
            if os.path.isfile(file_path):
                self.send_response(HTTPStatus.OK)
                self.send_header('Content-Length', '0')
                self.end_headers()
            else:
                self.send_error(HTTPStatus.NOT_FOUND, "File not found")
        # Handle event stream requests
        elif self.path == '/events':
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(b'data: Initialising event stream\n\n')
            try:
                self.handle_buffer()
            except ConnectionAbortedError:
                pass
        # Handle all other requests
        else:
            if CONFIG['SETTINGS']['CLIENT_SIDE_ROUTING']:
                # Check if the requested path points to a file
                file_path = self.translate_path(self.path)
                if os.path.isfile(file_path):
                    return super().do_GET()
                # Serve index.html for all other paths
                self.path = '/index.html'
            super().do_GET()

    def handle_buffer(self):
        BUFFER_EVENT.wait(timeout=None)
        self.wfile.write(b'data: refresh\n\n')
        BUFFER_EVENT.clear()
        self.handle_buffer()


def run():
    server_address = (CONFIG['SERVER']['HOSTNAME'], int(CONFIG['SERVER']['PORT']))
    # `ThreadingHTTPServer` is used as `HTTPServer` hangs on keyboard interrupt after the first client is served.
    httpd = ThreadingHTTPServer(server_address, Server)

    try:
        print(f'Server running at http://{CONFIG["SERVER"]["HOSTNAME"]}:{CONFIG["SERVER"]["PORT"]}')
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
