import os
import xml

import markdown
import shutil
import time

from jinja2 import Environment, FileSystemLoader

from config import OUTPUT_DIR, INPUT_DIR, STATIC_DIR
from util import read_file, write_file

# Define the Jinja2 environment and file system loader
env = Environment(loader=FileSystemLoader('templates'))


def build_site():
    build_start = time.perf_counter()

    # Clear the output directory
    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
    os.makedirs(OUTPUT_DIR)

    handle_conversions()
    handle_copy()

    build_finish = time.perf_counter()
    print(f'Finished site build in {round(build_finish-build_start, 3)} second(s)')


def handle_conversions():
    """Loop through input Markdown files and dispatch for conversion"""
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith('.md'):
            markdown_input = read_file(os.path.join(INPUT_DIR, filename))
            metadata, html = convert_to_html(markdown_input)
            output_text = render(metadata, html)
            inject_utils(filename, output_text)
            write_file(os.path.join(OUTPUT_DIR, filename.replace('.md', '.html')), output_text)


def handle_copy():
    """Copy all static files to their appropriate directories"""
    for filename in os.listdir(STATIC_DIR):
        shutil.copytree(
            os.path.join(STATIC_DIR, filename),
            os.path.join(OUTPUT_DIR, filename)
        )


def convert_to_html(input_text):
    """Compile Markdown files to HTML using Python-Markdown"""
    count = 0
    metadata = {}
    lines = input_text.split('\n')
    for line in lines:
        if line.startswith('---'):
            count += 1
            if count == 2:
                break
            continue
        parts = line.split(':', 1)
        if len(parts) == 2:
            metadata[parts[0].strip()] = parts[1].strip()

    # Parse input text to HTML
    html = markdown.markdown('\n'.join(lines[len(metadata) + 2:]))

    return metadata, html


def render(metadata, html):
    """Use Jinja2 to render the HTML template with the Markdown content"""
    template = env.get_template(metadata.get('template', 'default.html'))
    output_text = template.render(content=html, **metadata)

    return output_text


def inject_utils(filename, input_text):
    """Inject client-side development tools if in development mode"""
    if filename.split('.')[0] != 'index':
        return

    contents = ''
    lines = input_text.split('\n')
    for line in lines:
        if line.__contains__('</body>'):
            contents += line.split('<')[0] + '<script type=\'module\' src="/static/js/dev.js"></script>\n' + line + '\n'
        else:
            contents += line + '\n'
