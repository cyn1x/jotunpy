from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from config import HOSTNAME, PORT, OUTPUT_DIR


class Server(SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=OUTPUT_DIR, **kwargs)


def run():
    server_address = (HOSTNAME, PORT)
    # `ThreadingHTTPServer` is used as `HTTPServer` hangs on keyboard interrupt after the first client is served.
    httpd = ThreadingHTTPServer(server_address, Server)

    try:
        print(f'Server running at http://{HOSTNAME}:{PORT}')
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
