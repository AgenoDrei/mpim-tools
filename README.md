# mpim-tools
Meet people in Maastricht - tools to automate matching workflow

## Installation

Install this tool using `pip`:

    $ pip install mpim-tools

## Usage

Setup the tool with the necessary config using this command:
    
    mpim-tools setup <mailgun_domain> <api_key>

Create match suggestions for manual review for each participant, output folder will be created

    mpim-tools match <examples_relationships.xlsx> <output_path>

After manual curation, this command creates a matching table automatically

    mpim-tools confirm <prv_output_path>

Notify all participants provided you have a file with all the personal information and the previously generated matches:

    mpim-tools notify <matches.xlsx> <examples_relationships.xlsx> 

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
* [x] Mail automation
  * [x] Add all infos from the google form to the generated mail 
  * [x] Get an actual domain for the emails
  * [x] HTML email templates
* [ ] Create matching algorithm
  * [x] Based on categorical information
  * [ ] Based on unstructured free-text fields
  * [x] Command that generates a match table based on the remaining curated matches
* [x] Create user-friendly configuration for mail/id column names
* [ ] Automatically add IDs to inital documents