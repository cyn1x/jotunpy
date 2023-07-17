import os
import shutil
import time
from datetime import datetime

import markdown
import sass

from jinja2 import Environment, FileSystemLoader, exceptions

from core import html_editor
from core.config import CONFIG, import_env
from core.util import read_file, write_file

# Define the Jinja2 environment and file system loader
env = Environment(loader=FileSystemLoader('templates'))


def build_site():
    build_start = time.perf_counter()

    # Clear output directory before build
    shutil.rmtree(CONFIG['IO']['OUTPUT_DIR'], ignore_errors=True)

    # Copy development mode utility files if in debug mode
    if bool(CONFIG['SETTINGS'].getboolean('DEBUG')) is True:
        copy_utils()

    compile_markdown(CONFIG['IO']['INPUT_DIR'])

    # Exclude any static directories that have their own defined handlers
    exclusions = CONFIG['SETTINGS']['EXCLUDED_STATIC_DIRS'].split(',')
    static_dir = CONFIG['IO']['STATIC_DIR']
    for filename in os.listdir(static_dir):
        if os.path.isdir('/'.join([static_dir, filename])) and not exclusions.__contains__(filename):
            copy_static_files(filename)

    # Copy any relevant files for search engine crawlers if they exist
    inclusions = CONFIG['SETTINGS']['CRAWLER_FILES'].split(',')
    for filename in os.listdir('./'):
        file = os.path.join('./', filename)
        if os.path.exists(file) and os.path.isfile(file) and inclusions.__contains__(filename):
            shutil.copy(file, CONFIG['IO']['OUTPUT_DIR'])

    compile_sass()

    build_finish = time.perf_counter()
    print(f'Finished site build in {round(build_finish - build_start, 3)} second(s)')


def compile_markdown(input_dir):
    """Recursively loop through input Markdown files and dispatch for conversion"""
    convert_markdown(input_dir)
    for filename in os.listdir(input_dir):
        file = '/'.join([input_dir, filename])
        if os.path.isdir('/'.join([input_dir, filename])):
            compile_markdown(file)


def convert_markdown(input_dir):
    """Loop through input Markdown files and dispatch for conversion"""
    for filename in os.listdir(input_dir):
        if filename.endswith('.md'):
            markdown_input = read_file(os.path.join(input_dir, filename))
            metadata, html = convert_to_html(markdown_input)  # Convert Markdown to HTML
            html_document = render(metadata, html)  # Render HTML document

            output_text = ''
            if bool(CONFIG['SETTINGS'].getboolean('DEBUG')) is True:
                output_text = inject_dev_utils(html_document, filename)  # Inject dev utilities if using the server
            if filename.split('.')[0] == CONFIG['SETTINGS']['BLOG_HOMEPAGE'].split('.')[0]:
                output_text = add_posts(html_document)  # Show a shortcut to the latest blog posts

            dst_dir = os.path.join(CONFIG['IO']['OUTPUT_DIR'], input_dir.replace('docs', 'html'))
            if filename == 'index.md':
                dst_dir = CONFIG['IO']['OUTPUT_DIR']
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            write_file(os.path.join(dst_dir, filename.replace('.md', '.html')),
                       output_text if output_text else html_document)


def inject_dev_utils(output_text, filename):
    """Checks for a post list target element to insert a list of posts and injects dev utilities if using the server"""
    if bool(CONFIG['SETTINGS'].getboolean('CLIENT_SIDE_ROUTING')) is False or filename.split('.')[0] == 'index':
        output_text = add_utils(output_text)  # Add development mode utility files

    return output_text


def copy_utils():
    shutil.copytree(
        '.data',
        os.path.join(CONFIG['IO']['OUTPUT_DIR'], '.data')
    )


def copy_static_files(ext):
    """Copy all static files to their appropriate directories"""
    src = os.path.join(CONFIG['IO']['STATIC_DIR'], ext)
    dst = os.path.join(CONFIG['IO']['OUTPUT_DIR'], ext)

    shutil.copytree(src, dst)


def compile_sass():
    input_dir = os.path.join(CONFIG['IO']['STATIC_DIR'], 'scss')
    output_dir = os.path.join(CONFIG['IO']['OUTPUT_DIR'], 'css')

    if bool(CONFIG['SETTINGS'].getboolean('DEBUG')) is True:
        style = 'expanded'
    else:
        style = CONFIG['SETTINGS']['CSS_OUTPUT_STYLE']

    try:
        sass.compile(
            dirname=(input_dir, output_dir),
            output_style=style,
        )
    except sass.CompileError as e:
        print(e)


def convert_to_html(input_text):
    """Compile Markdown files to HTML using Python-Markdown"""
    lines = input_text.split('\n')
    metadata = parse_metadata(lines)

    # Parse input text to HTML
    html = markdown.markdown('\n'.join(lines[len(metadata) + 2:]), extensions=['nl2br'])

    return metadata, html


def parse_metadata(lines):
    count = 0
    metadata = {}

    for line in lines:
        if line.startswith('---'):
            count += 1
            if count == 2:
                break
            continue
        parts = line.split(':', 1)
        if len(parts) == 2:
            metadata[parts[0].strip()] = parts[1].strip()

    return metadata


def render(metadata, html):
    """Use Jinja2 to render the HTML template with the Markdown content"""
    template = env.get_template(metadata.get('template', 'default.html'))
    env_vars = import_env()[os.environ['ENVIRONMENT'].lower()]

    try:
        output_text = template.render(content=html, **metadata, **env_vars)
        return output_text
    except exceptions.TemplateNotFound as e:
        print(f'jinja2.exceptions.TemplateNotFound: {e}')
        exit(1)


def add_posts(input_text):
    """Collect all blog posts and add hyperlinks"""
    posts = collect_posts()
    editor = html_editor.HtmlEditor(
        html=input_text,
        anchor=CONFIG['SETTINGS']['POST_LIST_TARGET'],
        element=posts,
        prepend=False
    )
    return editor.add_html()


def add_utils(input_text):
    """Inject client-side development tools if in development mode"""
    editor = html_editor.HtmlEditor(
        html=input_text,
        anchor='</body>',
        element=f'<script type=\'module\' src="/.data/scripts/dev.js"></script>\n',
        prepend=True
    )
    return editor.add_html()


def collect_posts():
    """Collects all Markdown blog files and creates a string of hyperlinks to each of their HTML generated variants"""
    contents = ''
    ext = 'html'
    for filename in os.listdir(os.path.join(CONFIG['IO']['INPUT_DIR'], 'blog')):
        markdown_input = read_file(os.path.join(CONFIG['IO']['INPUT_DIR'], 'blog', filename))
        lines = markdown_input.split('\n')
        metadata = parse_metadata(lines)
        creation_date = metadata.get('published')
        human_readable_datetime = datetime.strptime(creation_date, '%Y-%m-%dT%H:%M:%S%z').strftime('%B %d, %Y')

        name = filename.split('.')[0]
        contents += f'<a href=\'/html/blog/{name}.{ext}\' class=\'post-link\'>' \
                    f'<p>{name.title().replace("-", " ")}</p>' \
                    f'</a>' \
                    f'<p>{human_readable_datetime}</p>'

    if contents == '':
        contents = "<p>There doesn't seem to be anything here yet. Check back later or subscribe to the RSS feed " \
                      'to be notified when new blog posts are published.</p>'

    return contents
