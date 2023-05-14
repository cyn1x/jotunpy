from app import server, site_generator, observer

if __name__ == '__main__':
    observer.run()
    site_generator.build_site()
    server.run()
