import sys

from app import web_server, site_generator, observer


def parse_args(args):
    if args[1] == '--dev':
        run_dev()
    elif args[1] == '--build':
        run_build()


def run_dev():
    site_generator.build_site()
    observer.run()
    web_server.run()


def run_build():
    site_generator.bundle_site()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        parse_args(sys.argv)
    else:
        run_dev()
