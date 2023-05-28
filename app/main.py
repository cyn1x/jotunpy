import threading

from app import web_server, site_generator, observer


# Create an event to signal buffer completion
buffer_event = threading.Event()

if __name__ == '__main__':
    site_generator.build_site()
    observer.run()
    web_server.run()
