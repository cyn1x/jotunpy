import argparse
import os
import shutil

from core import web_server, site_generator, observer
from core.config import CONFIG, update_config

parser = argparse.ArgumentParser(
    prog='main.py',
    description='Static site generator and development server')

subparsers = parser.add_subparsers(help='sub command help')
subparsers.required = True


def start_dev(opts):
    """Starts the development server"""
    if opts.port is not None:
        update_config("SERVER.PORT", opts.port)

    site_generator.build_site()
    observer.run()
    web_server.run()


def start_build(opts):
    """Packages static content so that is ready for deployment"""
    os.environ['ENVIRONMENT'] = 'PRODUCTION'
    update_config("SETTINGS.DEBUG", 'No')
    update_config("IO.OUTPUT_DIR", CONFIG['IO']['BUILD_DIR'])

    if opts.optimize is True:
        # update_config("SETTINGS.HTML_OUTPUT_STYLE", '')
        update_config("SETTINGS.CSS_OUTPUT_STYLE", 'compressed')
        # update_config("SETTINGS.JS_OUTPUT_STYLE", '')
    elif opts.no_optimize is True:
        # update_config("SETTINGS.HTML_OUTPUT_STYLE", '')
        update_config("SETTINGS.CSS_OUTPUT_STYLE", 'nested')
        # update_config("SETTINGS.JS_OUTPUT_STYLE", '')
    else:
        # Accept config defaults
        pass

    site_generator.build_site()


def start_new(opts):
    """Generates project files in an empty directory"""
    os.mkdir(opts.output_dir)
    shutil.copytree(CONFIG['IO']['INPUT_DIR'], os.path.join(opts.output_dir, 'docs'))
    shutil.copytree(CONFIG['IO']['TEMPLATE_DIR'], os.path.join(opts.output_dir, 'templates'))
    shutil.copytree(CONFIG['IO']['STATIC_DIR'], os.path.join(opts.output_dir, 'static'))
    shutil.copyfile('config.ini', os.path.join(opts.output_dir, 'config.ini'))
    print(f'New project created successfully in {opts.output_dir}')


def configure_parser():
    # Parser for starting the development server with the option of specifying a port
    parser_a = subparsers.add_parser('dev', help='run the development server')
    parser_a.add_argument('-p', '--port', help='port number for the development server')
    parser_a.set_defaults(func=start_dev)

    # Parser for generating files ready for deployment with the option of optimizing
    parser_b = subparsers.add_parser('build', help='bundle for production deployment')
    parser_b.add_argument('--optimize', help='build output files are to be optimized', action='store_true')
    parser_b.add_argument('--no-optimize', help='build output files are to not be optimized', action='store_true')
    parser_b.set_defaults(func=start_build)

    # Parser for generating a new project structure in a specified directory
    parser_c = subparsers.add_parser('new', help='generate a new project')
    parser_c.add_argument('-o', '--output-dir', help='directory to create the project', default='.')
    parser_c.set_defaults(func=start_new)


if __name__ == '__main__':
    configure_parser()
    args = parser.parse_args()
    args.func(args)
