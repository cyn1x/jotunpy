from src import server, websocket, generator, observer

if __name__ == '__main__':
    observer.run()
    generator.build_site()
    websocket.run()
    server.run()
