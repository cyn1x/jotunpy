import re


class HtmlEditor:
    def __init__(self, **kwargs):
        self.html = kwargs.get('html')
        self.anchor = kwargs.get('anchor')
        self.element = kwargs.get('element')
        self.prepend = kwargs.get('prepend')

    def add_html(self):
        """Appends or prepends a given HTML element at the position of a specific anchor tag"""
        contents = ''
        lines = self.html.split('\n')
        for line in lines:
            if line.__contains__(self.anchor):
                whitespace = line.split('<')[0]
                # Remove unnecessary whitespace between opening and closing tags if no content exists
                element = re.sub(r'(?<=>)\s+(?=<)', '', line)
                divided_element = element.split('><')
                if len(element.split('><')) > 1:
                    # Append content between HTML opening and closing tag with formatted whitespace
                    contents += divided_element[0] + '>\n' + (whitespace + '    ') + self.element + '\n' + whitespace\
                                + '<' + divided_element[1] + '\n'
                else:
                    append_html = whitespace + self.element + line + '\n'
                    prepend_html = line + '\n' + whitespace + self.element
                    contents += append_html if self.prepend is True else prepend_html
            else:
                contents += line + ('\n' if line != '</html>' else '')

        return contents

    def remove_html(self):
        """Removes a given HTML element at the position of a specific anchor tag"""
        pass
