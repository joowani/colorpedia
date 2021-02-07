# Contributing

Set up development environment:
```shell
cd ~/your/colorpedia/clone  # Activate venv if you have one (recommended)
pip install -e .[dev]       # Install dev dependencies (e.g. black, mypy, pre-commit)
pre-commit install          # Install git pre-commit hooks
```

Run unit tests with coverage:

```shell
py.test --cov=colorpedia --cov-report=html
```

Build and test documentation (Colorpedia uses [MkDocs](https://www.mkdocs.org/)):
```shell
mkdocs serve  # Go to http://127.0.0.1:8000 on your browser after
```

Add new colors [here](https://github.com/joowani/colorpedia/blob/main/colorpedia/hexcodes.py) 
and palettes [here](https://github.com/joowani/colorpedia/blob/main/colorpedia/palettes.py).

Thank you for your contribution!
