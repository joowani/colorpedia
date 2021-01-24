from setuptools import find_packages, setup

with open("README.md") as fp:
    description = fp.read()


setup(
    name="colorpedia",
    license="MIT",
    description="Command-line tool for looking up colors",
    long_description=description,
    long_description_content_type="text/markdown",
    author="Joohwan Oh",
    author_email="joohwan.oh@outlook.com",
    url="https://github.com/joowani/colorpedia",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    python_requires=">=3.6",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    install_requires=[
        "fire>=0.3.1",
        "setuptools>=42",
        "setuptools_scm[toml]>=3.4",
    ],
    extras_require={
        "dev": [
            "black",
            "flake8",
            "isort>=5.0.0",
            "mypy",
            "pytest>=6.0.0",
            "pytest-cov>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "color = colorpedia.cli:entry_point",
            "colorpedia = colorpedia.cli:entry_point",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
