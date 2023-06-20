import os


def clear_terminal():
    """Clear the terminal screen based on the operating system"""
    if os.name == "posix":  # UNIX/Linux/MacOS
        os.system("clear")
    elif os.name == "nt":  # Windows
        os.system("cls")


def read_file(file):
    f = open(file, 'r')
    contents = f.read()
    f.close()

    return contents


def write_file(file, contents):
    f = open(file, 'w')
    f.write(contents)
    f.close()
