from setuptools import find_packages, setup

with open("docs/README.md") as fp:
    long_description = fp.read()

setup(
    name="colorpedia",
    description="CLI for Color Lookups",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Joohwan Oh",
    author_email="joohwan.oh@outlook.com",
    url="https://github.com/joowani/colorpedia",
    keywords=["cli", "color", "terminal"],
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    python_requires=">=3.6",
    license="MIT",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    install_requires=[
        "dataclasses>=0.6; python_version < '3.7'",
        "fire>=0.3.1",
        "setuptools>=42",
        "setuptools_scm[toml]>=3.4",
    ],
    extras_require={
        "dev": [
            "black",
            "flake8>=3.8.4",
            "isort>=5.0.0",
            "mkdocs-material",
            "mypy>=0.790",
            "pre-commit>=2.9.3",
            "pytest>=6.0.0",
            "pytest-cov>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "color = colorpedia.cli:entry_point_color",
            "colorpedia = colorpedia.cli:entry_point_colorpedia",
        ],
    },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Topic :: Documentation :: Sphinx",
        "Topic :: Utilities",
    ],
)
