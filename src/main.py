import server
import observer
import generator

if __name__ == '__main__':
    observer.run()
    generator.build_site()
    server.run()
