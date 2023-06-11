import os
import shutil
import time

import markdown
import sass

from jinja2 import Environment, FileSystemLoader

from app import html_editor
from util import config, read_file, write_file

# Define the Jinja2 environment and file system loader
env = Environment(loader=FileSystemLoader('templates'))


def build_site():
    build_start = time.perf_counter()

    reset_dist()
    convert_markdown(config['IO']['INPUT_DIR'])
    convert_markdown(os.path.join(config['IO']['INPUT_DIR'], 'blog'))
    copy_scripts()
    compile_sass()

    build_finish = time.perf_counter()
    print(f'Finished site build in {round(build_finish - build_start, 3)} second(s)')


def reset_dist():
    shutil.rmtree(config['IO']['OUTPUT_DIR'], ignore_errors=True)
    os.makedirs(config['IO']['OUTPUT_DIR'])
    os.makedirs(os.path.join(config['IO']['OUTPUT_DIR'], 'html', 'blog'))


def convert_markdown(input_dir):
    """Loop through input Markdown files and dispatch for conversion"""
    for filename in os.listdir(input_dir):
        if filename.endswith('.md'):
            markdown_input = read_file(os.path.join(input_dir, filename))
            metadata, html = convert_to_html(markdown_input)
            output_text = render(metadata, html)

            if filename.split('.')[0] == 'index':
                output_text = add_utils(output_text)  # Add development mode utility files
                output_text = add_posts(output_text)  # Show a shortcut to the latest blog posts on the main page
            write_dir = determine_html_subdir(metadata)
            write_file(os.path.join(write_dir, filename.replace('.md', '.html')), output_text)


def collect_posts():
    """Collects all Markdown blog files and creates a string of hyperlinks to each of their HTML generated variants"""
    contents = ''
    ext = 'html'
    for filename in os.listdir(os.path.join(config['IO']['INPUT_DIR'], 'blog')):
        name = filename.split('.')[0]
        contents += f'<a href=\'/html/blog/{name}.{ext}\' class=\'post-link\'>' \
                    f'{name.title().replace("-", " ")}' \
                    f'</a>'
    return contents


def copy_scripts():
    """Copy all static files to their appropriate directories"""
    scripts_src = os.path.join(config['IO']['STATIC_DIR'], 'js')
    scripts_dst = os.path.join(config['IO']['OUTPUT_DIR'], 'js')
    os.mkdir(scripts_dst)

    for filename in os.listdir(scripts_src):
        shutil.copyfile(
            os.path.join(scripts_src, filename),
            os.path.join(scripts_dst, filename),
            follow_symlinks=True
        )


def compile_sass():
    input_dir = os.path.join(config['IO']['STATIC_DIR'], 'scss')
    output_dir = os.path.join(config['IO']['OUTPUT_DIR'], 'css')

    try:
        sass.compile(
            dirname=(input_dir, output_dir),
            output_style='expanded',
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
    output_text = template.render(content=html, **metadata)

    return output_text


def add_posts(input_text):
    """Collect all blog posts and add hyperlinks"""
    editor = html_editor.HtmlEditor(
        html=input_text,
        anchor='<ul class=\'post-list\'>',
        element=collect_posts(),
        prepend=False
    )
    return editor.add_html()


def add_utils(input_text):
    """Inject client-side development tools if in development mode"""
    editor = html_editor.HtmlEditor(
        html=input_text,
        anchor='</body>',
        element='<script type=\'module\' src="js/dev.js"></script>\n',
        prepend=True
    )
    return editor.add_html()


def determine_html_subdir(metadata):
    if metadata.get('template') == 'post.html':
        return os.path.join(config['IO']['OUTPUT_DIR'], 'html', 'blog')
    elif metadata.get('template') != 'default.html':
        return os.path.join(config['IO']['OUTPUT_DIR'], 'html')
    else:
        return config['IO']['OUTPUT_DIR']
