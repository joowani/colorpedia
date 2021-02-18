# Contributing

Set up dev environment:
```shell
cd ~/your/repository/fork  # Activate venv if you have one (recommended)
pip install -e .[dev]      # Install dev dependencies (e.g. black, mypy, pre-commit)
pre-commit install         # Install git pre-commit hooks
```

Run unit tests with coverage:

```shell
py.test --cov=colorpedia --cov-report=html  # Open htmlcov/index.html in your browser
```

Build and test documentation (Colorpedia uses [MkDocs](https://www.mkdocs.org)):
```shell
mkdocs serve  # Open http://127.0.0.1:8000 in your browser
```

You can add new colors [here](https://github.com/joowani/colorpedia/blob/main/colorpedia/hexcodes.py) 
and palettes [here](https://github.com/joowani/colorpedia/blob/main/colorpedia/palettes.py).
Thank you for your contribution!
