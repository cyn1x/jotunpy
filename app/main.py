from app import web_server, site_generator, observer

if __name__ == '__main__':
    observer.run()
    site_generator.build_site()
    web_server.run()
