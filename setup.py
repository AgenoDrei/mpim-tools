from setuptools import setup
import os


VERSION = "1.2"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="mpim-tools",
    description="Meet people in Maastricht - tools to automate matching workflow",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon",
    url="https://github.com/AgenoDrei/mpim-tools",
    project_urls={
        "Issues": "https://github.com/AgenoDrei/mpim-tools/issues",
        "CI": "https://github.com/AgenoDrei/mpim-tools/actions",
        "Changelog": "https://github.com/AgenoDrei/mpim-tools/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["mpim_tools"],
    include_package_data=True,
    entry_points="""
        [console_scripts]
        mpim-tools=mpim_tools.cli:cli
    """,
    install_requires=["click", "pandas", "openpyxl", "requests", "jinja2", "importlib_resources", "tqdm", "numpy", "toml"],
    extras_require={
        "test": ["pytest"]
    },
    python_requires=">=3.6",
)
