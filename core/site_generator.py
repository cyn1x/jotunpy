import os
import shutil
import time

import markdown
import sass

from jinja2 import Environment, FileSystemLoader, exceptions

from core import html_editor
from core.config import CONFIG
from core.util import read_file, write_file

# Define the Jinja2 environment and file system loader
env = Environment(loader=FileSystemLoader('templates'))


def build_site():
    build_start = time.perf_counter()
    posts = collect_posts()

    reset_dist()
    if bool(CONFIG['SETTINGS'].getboolean('DEBUG')) is True:
        copy_utils()
    convert_markdown(CONFIG['IO']['INPUT_DIR'], posts)
    convert_markdown(os.path.join(CONFIG['IO']['INPUT_DIR'], 'blog'), posts)
    copy_static_files('js')
    copy_static_files('img')
    compile_sass()

    build_finish = time.perf_counter()
    print(f'Finished site build in {round(build_finish - build_start, 3)} second(s)')


def reset_dist():
    shutil.rmtree(CONFIG['IO']['OUTPUT_DIR'], ignore_errors=True)
    os.makedirs(CONFIG['IO']['OUTPUT_DIR'])
    os.makedirs(os.path.join(CONFIG['IO']['OUTPUT_DIR'], 'html', 'blog'))


def convert_markdown(input_dir, post_list):
    """Loop through input Markdown files and dispatch for conversion"""
    for filename in os.listdir(input_dir):
        if filename.endswith('.md'):
            markdown_input = read_file(os.path.join(input_dir, filename))
            metadata, html = convert_to_html(markdown_input)
            output_text = render(metadata, html)
            output_text = add_posts(output_text, post_list)  # Show a shortcut to the latest blog posts
            output_text = inject_dev_utils(output_text, filename)
            write_dir = determine_html_subdir(metadata)
            write_file(os.path.join(write_dir, filename.replace('.md', '.html')), output_text)


def inject_dev_utils(output_text, filename):
    """Checks for a post list target element to insert a list of posts and injects dev utilities if using the server"""
    if bool(CONFIG['SETTINGS'].getboolean('DEBUG')) is True \
            and (bool(CONFIG['SETTINGS'].getboolean('CLIENT_SIDE_ROUTING')) is False
                 or filename.split('.')[0] == 'index'):
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
    html = markdown.markdown('\n'.join(lines[len(metadata) + 2:]), extensions=['nl2br'])

    return metadata, html


def render(metadata, html):
    """Use Jinja2 to render the HTML template with the Markdown content"""
    template = env.get_template(metadata.get('template', 'default.html'))

    try:
        output_text = template.render(content=html, **metadata)
        return output_text
    except exceptions.TemplateNotFound as e:
        print(f'jinja2.exceptions.TemplateNotFound: {e}')
        exit(1)


def add_posts(input_text, post_list):
    """Collect all blog posts and add hyperlinks"""
    editor = html_editor.HtmlEditor(
        html=input_text,
        anchor=CONFIG['SETTINGS']['POST_LIST_TARGET'],
        element=post_list,
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
        name = filename.split('.')[0]
        contents += f'<a href=\'/html/blog/{name}.{ext}\' class=\'post-link\'>' \
                    f'{name.title().replace("-", " ")}' \
                    f'</a>'
    return contents


def determine_html_subdir(metadata):
    if metadata.get('template') == 'post.html':
        return os.path.join(CONFIG['IO']['OUTPUT_DIR'], 'html', 'blog')
    elif metadata.get('template') != 'index.html':
        return os.path.join(CONFIG['IO']['OUTPUT_DIR'], 'html')
    else:
        return CONFIG['IO']['OUTPUT_DIR']
