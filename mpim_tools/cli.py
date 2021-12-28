import click
import os
import pandas as pd
import json

from _socket import herror

from mpim_tools.notify_matches import send_mails
from mpim_tools.startup import CACHE_DIR


@click.group()
@click.version_option()
def cli():
    "Meet people in Maastricht - tools to automate matching workflow"


@cli.command(name="command")
@click.argument("example")
@click.option("-o", "--option", help="An example option")
def first_command(example, option):
    "Command description goes here"
    click.echo(f"Here is some output: {example}/{option}")


@cli.command(name="setup")
@click.argument("domain")
@click.argument("apikey")
def notify(domain, apikey):
    """
    :param domain: mailgun domain that is used
    :param apikey: private api-key
    """
    print(f"Save configuration to {CACHE_DIR}")
    config = {"base_url": "https://api.eu.mailgun.net/v3/", "domain": domain, "apikey": apikey}
    f = open(CACHE_DIR / "config.json", 'w')
    json.dump(config, f)


@cli.command(name="notify")
@click.argument("matches_path")
@click.argument("people_path")
@click.option("-d", "--debug/--no-debug", help="Activate debug mode", default=False)
def notify(matches_path, people_path, debug):
    print(f"Processing matches from {matches_path}, debug mode {debug}")
    matches_df = pd.read_excel(matches_path)
    people_df = pd.read_excel(people_path)

    send_mails(matches_df, people_df, debug=debug)


import sys
if __name__ == '__main__':
    cli(sys.argv[1:])

