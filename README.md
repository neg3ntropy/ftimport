# ftimport

Automatically control a web browser to add transactions to a [Financial Times](https://www.ft.com/) portfolio.

## Usage

- Download the project and create a new Firefox profile in a `profile` subfolder
- Authenticate to ft.com, create a portfolio and get its id from the URL
- Export the transactions that you want to add to a CSV file
- Run and watch things happens
- Verify and clean your transaction records in ft.com

## Disclaimer

This is a quick and dirty solution presently, tailored to a single person requirements.

It is not supported by the Financial Times. It could break at any time for any change in the website.

Only CSV export from Degiro are supported, but things could not work depending on the region of the account or locale settings.

## Development

The project is implemented on top of these core technologies:

* [python](https://www.python.org/)
* [selenium](https://selenium-python.readthedocs.io/)
* [PyPOM](https://pypom.readthedocs.io/en/latest/) for browser automation and page objects.

The following tools are integrated for development:

* [pipenv](https://github.com/pypa/pipenv) for dependency management
* [black](https://github.com/psf/black) for code formatting
* [isort](https://github.com/timothycrosley/isort) for import sorting
* [pylint](https://www.pylint.org/) for code linting
* [pudb](https://documen.tician.de/pudb/index.html), a console debugger
* [ipython](https://ipython.org/), a interactive shell or REPL for live coding
* [mypy](http://mypy-lang.org/) for static type checking

### Getting started

Make sure you have:

* pipenv (recommended version 2018.11.26)
* python 3.9 or [pyenv](https://github.com/pyenv/pyenv).
* Firefox

Anything else is installed via pipenv:

```
$ pipenv install --dev
```

Activate the development environment:

```
$ pipenv shell
```

[geckodriver](https://github.com/mozilla/geckodriver/releases) will be downloaded automatically and installed
in `drivers/cache`.

For Visual Studio Code:

* `./vscode/settings.json` enables all tools with the default Python extension
* add EditorConfig extension: `Ctrl^P` then `ext install EditorConfig.EditorConfig`
