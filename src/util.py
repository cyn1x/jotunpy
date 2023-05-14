def read_file(file):
    f = open(file, 'r')
    contents = f.read()
    f.close()

    return contents


def write_file(file, contents):
    f = open(file, 'w')
    f.write(contents)
    f.close()
