import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from config import HOSTNAME, PORT, OUTPUT_DIR


class Server(SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=OUTPUT_DIR, **kwargs)

    def do_GET(self):
        if self.path == '/events':
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(b'data: Initialising event stream\n\n')
            while True:
                self.wfile.write(b'data: ' + str(time.time()).encode() + b'\n\n')
                time.sleep(10)
        else:
            super().do_GET()


def run():
    server_address = (HOSTNAME, PORT)
    # `ThreadingHTTPServer` is used as `HTTPServer` hangs on keyboard interrupt after the first client is served.
    httpd = ThreadingHTTPServer(server_address, Server)

    try:
        print(f'Server running at http://{HOSTNAME}:{PORT}')
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
