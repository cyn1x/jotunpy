# JotunPy

Static site generator with live development preview written in Python. The live development server makes use of 
[server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events) 
to refresh the client browser on state change.

## Installation

Clone the repository and run the `install.bat` script to install the required dependencies. The script will create a 
new virtual environment in the `venv` directory, and install all the required dependencies into the virtual
environment. The script will also create a new `config.ini` file in the root directory of the project.

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

The `-h` or `--help` flag shows information on all the available options.
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
JotunPy supports application specific configurations through a `config.ini` file, and environment variable loading 
through a `config.yaml` file.

#### INI

The INI file is used for application specific settings. Most of the important settings are stored in the `config.ini` 
file in the root directory of the directory where the new project was created. The `CLIENT_SIDE_ROUTING` key indicates 
whether a JavaScript based router will be used for client-side rendering. The default value is `No` to ensure the 
development utilities are injected into all HTML files unless otherwise specified.

#### YAML

The YAML configuration file is used for loading environment variables into the application's runtime. An example of 
its usefulness can be demonstrated with non-sensitive information like separate API URIs depending on whether a 
site build is triggered for production, or live development preview is enabled for site development.

```yaml
development: {
  key: 'value'
}
production: {
  key: 'value'
}
```

## Blog

Blog posts are only published in the `site.rss` feed if a build is triggered for production using the `build` option. 
Site rebuilds in development using the `dev` option mode will not update the `site.rss` feed, and instead use the time 
of the last development build as a placeholder for the publication date of the blog post in HTML.

### Database

An SQLite database is used to store blog post metadata for published blog posts. The database is created in the root 
`.data/` directory of the project when a new project is created using the `new` option with the filename `site.db`.
