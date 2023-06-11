import sys

from app import web_server, site_generator, observer
from app.util import config


def parse_args(args):
    if args[1] == '--dev':
        run_dev()
    elif args[1] == '--build':
        config['IO']['OUTPUT_DIR'] = config['IO']['BUILD_DIR']
        site_generator.build_site()


def run_dev():
    site_generator.build_site()
    observer.run()
    web_server.run()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        parse_args(sys.argv)
    else:
        run_dev()
