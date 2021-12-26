# mpim-tools

[![PyPI](https://img.shields.io/pypi/v/mpim-tools.svg)](https://pypi.org/project/mpim-tools/)
[![Changelog](https://img.shields.io/github/v/release/AgenoDrei/mpim-tools?include_prereleases&label=changelog)](https://github.com/AgenoDrei/mpim-tools/releases)
[![Tests](https://github.com/AgenoDrei/mpim-tools/workflows/Test/badge.svg)](https://github.com/AgenoDrei/mpim-tools/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/AgenoDrei/mpim-tools/blob/master/LICENSE)

Meet people in Maastricht - tools to automate matching workflow

## Installation

Install this tool using `pip`:

    $ pip install mpim-tools

## Usage

Setup the tool with the necessary config using this command:
    
    mpim-tools setup <mailgun_domain> <api_key>

Notify all participants provided you have a file with all the personal information and the previously generated matches:

    mpim-tools notify ~\MPIM-tools\data\examples_matches.xlsx ~\MPIM-tools\data\example_data_relationships.xlsx 


## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd mpim-tools
    python -m venv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest

## ToDo 
* [ ] Add all infos from the google form to the generated mail 
* [ ] Get an actual domain for the emails
* [ ] HTML email templates
* [ ] Create matching algorithm
  * [ ] Based on categorical information
  * [ ] Based on unstructured free-text fields