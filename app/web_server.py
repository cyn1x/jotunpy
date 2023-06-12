from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from app.config import CONFIG
from app.event import BUFFER_EVENT


class Server(SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=CONFIG['IO']['OUTPUT_DIR'], **kwargs)

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
