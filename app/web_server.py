from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from app import message
from util import config


class Server(SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=config['IO']['OUTPUT_DIR'], **kwargs)

    def do_GET(self):
        if self.path == '/events':
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(b'data: Initialising event stream\n\n')
            try:
                self.handle_buffer()
            except ConnectionAbortedError:
                pass
        else:
            super().do_GET()

    def handle_buffer(self):
        message.buffer_event.wait(timeout=None)
        self.wfile.write(b'data: refresh\n\n')
        message.buffer_event.clear()
        self.handle_buffer()


def run():
    server_address = (config['SERVER']['HOSTNAME'], int(config['SERVER']['PORT']))
    # `ThreadingHTTPServer` is used as `HTTPServer` hangs on keyboard interrupt after the first client is served.
    httpd = ThreadingHTTPServer(server_address, Server)

    try:
        print(f'Server running at http://{config["SERVER"]["HOSTNAME"]}:{config["SERVER"]["PORT"]}')
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
