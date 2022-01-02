import os.path

import click
import sys
import pandas as pd
import json
from _socket import herror

from mpim_tools.create_matches import create_matches
from mpim_tools.notify_matches import send_mails
from mpim_tools.startup import CACHE_DIR, MAILGUN_BASE


@click.group()
@click.version_option()
def cli():
    "Meet people in Maastricht - tools to automate matching workflow"


@cli.command(name="setup")
@click.argument("domain")
@click.argument("apikey")
def notify(domain, apikey):
    """
    :param domain: mailgun domain that is used
    :param apikey: private api-key
    """
    print(f"Save configuration to {CACHE_DIR}")
    config = {"base_url": MAILGUN_BASE, "domain": domain, "apikey": apikey}
    f = open(CACHE_DIR / "config.json", 'w')
    json.dump(config, f)


@cli.command(name="match")
@click.argument("people_path")
@click.argument("output_path")
@click.option("-m", "--maximum_matches", help="Maximum number of possible matches per person", default=10)
def match(people_path, output_path, maximum_matches):
    print(f"Process people and create max. {maximum_matches} possible matches...")
    people_df = pd.read_excel(people_path)
    if os.path.exists(output_path):
        click.echo("Output path already exists")
        return -1
    os.mkdir(output_path)
    create_matches(people_df, output_path, maximum_matches)


@cli.command(name="notify")
@click.argument("matches_path")
@click.argument("people_path")
@click.option("-d", "--debug/--no-debug", help="Activate debug mode", default=False)
@click.option("-m", "--mode", help="Select FWB / Relationship / Friends mode", default="Relationship")
def notify(matches_path, people_path, debug, mode):
    print(f"Processing matches from {matches_path} for mode {mode}, debug status {debug}")
    matches_df = pd.read_excel(matches_path)
    people_df = pd.read_excel(people_path)

    send_mails(matches_df, people_df, mode, debug=debug)


if __name__ == '__main__':
    cli(sys.argv[1:])

