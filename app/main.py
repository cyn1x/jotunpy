import os
import sys

from app import web_server, site_generator, observer
from app.config import CONFIG, update_config


def setup():
    environment = os.environ.get('ENVIRONMENT')
    if environment == 'DEVELOPMENT':
        pass
    elif environment == 'PRODUCTION':
        update_config("SETTINGS.DEBUG", 'No')


def parse_args():
    if sys.argv[1] == 'dev':
        pass
    elif sys.argv[1] == 'build':
        update_config("IO.OUTPUT_DIR", CONFIG['IO']['BUILD_DIR'])

    parse_optional_args()


def parse_optional_args():
    if len(sys.argv) == 3 and sys.argv[1] == 'build':
        if sys.argv[2] == '--optimize':
            # update_config("SETTINGS.HTML_OUTPUT_STYLE", '')
            update_config("SETTINGS.CSS_OUTPUT_STYLE", 'compressed')
            # update_config("SETTINGS.JS_OUTPUT_STYLE", '')
        elif sys.argv[2] == '--no-optimize':
            # update_config("SETTINGS.HTML_OUTPUT_STYLE", '')
            update_config("SETTINGS.CSS_OUTPUT_STYLE", 'nested')
            # update_config("SETTINGS.JS_OUTPUT_STYLE", '')


def run_dev():
    site_generator.build_site()
    observer.run()
    web_server.run()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('No options specified.')
        exit(0)

    setup()
    parse_args()

    if sys.argv[1] == 'dev':
        run_dev()
    elif sys.argv[1] == 'build':
        site_generator.build_site()
    else:
        print('Invalid options specified.')
