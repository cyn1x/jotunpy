# JotunPy

Static site generator with live development preview written in Python. The live development server makes use of 
[server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events) 
to refresh the client browser on state change.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

### Windows
```commandline
git clone https://github.com/cyn1x/jotunpy.git
cd jotunpy
install.bat
```

### Linux
```bash

```

## Usage

I personally prefer using virtual environments to not pollute the global `pip` namespace when not necessary to do so.

When running for the first time, create a new website directory to copy all stock templates over to the new working 
directory for customization.

```commandline
venv\Scripts\activate
python main.py new -o "..\my-awesome-website"
cd ..\my-awesome-website
python ..\jotunpy\main.py dev
```

When running thereafter, just activate the virtual environment before starting the live development server in the 
current working directory.

```commandline
..\jotunpy\venv\Scripts\activate
python ..\jotunpy\main.py dev
```

### Help

The `-h` or `--help` flag shows information on all of the available options.
```commandline
> python main.py -h
usage: main.py [-h] {dev,build,new} ...

Static site generator and development server

positional arguments:
  {dev,build,new}  sub command help
    dev            run the development server
    build          bundle for production deployment
    new            generate a new project

options:
  -h, --help       show this help message and exit
```
Similarly, each sub command contains useful help information for any optional arguments.
```commandline
> python main.py dev -h
usage: main.py dev [-h] [-p PORT]

options:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  port number for the development server
```

### Configuration

Most of the important settings are stored in the `config.ini` file in the root directory of the directory where the 
new project was created. The `CLIENT_SIDE_ROUTING` key indicates whether a JavaScript based router will be used for 
client-side rendering. The default value is `No` to ensure the development utilities are injected into all HTML files 
unless otherwise specified.
