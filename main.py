import markdown
import os

from jinja2 import Environment, FileSystemLoader


def parse():
    # Define input and output directories
    input_dir = 'docs'
    output_dir = 'dist'
    template_dir = 'templates'

    # Create Jinja2 environment
    env = Environment(loader=FileSystemLoader(template_dir))

    # Loop through input files
    for filename in os.listdir(input_dir):
        if filename.endswith('.md'):
            # Read input file
            with open(os.path.join(input_dir, filename), 'r') as f:
                input_text = f.read()

            # Parse metadata
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
            html = markdown.markdown('\n'.join(lines[len(metadata) + 1:]))

            # Render template
            template = env.get_template(metadata.get('template', 'default.html'))
            output_text = template.render(content=html, **metadata)

            # Write output file
            with open(os.path.join(output_dir, filename.replace('.md', '.html')), 'w') as f:
                f.write(output_text)


if __name__ == '__main__':
    parse()
