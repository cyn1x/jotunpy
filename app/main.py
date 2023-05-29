from app import web_server, site_generator, observer


if __name__ == '__main__':
    site_generator.build_site()
    observer.run()
    web_server.run()
