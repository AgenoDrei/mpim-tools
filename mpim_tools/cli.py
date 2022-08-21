import os.path
import click
import sys
import pandas as pd
import json
from mpim_tools.create_matches import create_matches
from mpim_tools.notify_matches import send_mails
from mpim_tools.startup import CACHE_DIR, MAILGUN_BASE, names


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
@click.option("-n", "--maximum_matches", help="Maximum number of possible matches per person", default=10)
@click.option("-m", "--mode", help="Select FWB / Relationship / Friendship mode", default="Relationship")
def match(people_path, output_path, maximum_matches, mode):
    """
    Propose matches in the folder OUTPUT_PATH for every participant defined in PEOPLE_PATH
    """
    print(f"Process people and create max. {maximum_matches} possible matches...")
    people_df = pd.read_excel(people_path)
    if os.path.exists(output_path) and len(os.listdir(output_path)) != 0:
        click.echo("Output path already exists")
        return -1
    if not os.path.exists(output_path): os.mkdir(output_path)
    create_matches(people_df, output_path, maximum_matches, mode=mode)


@cli.command(name="confirm")
@click.argument("matches_path")
def confirm(matches_path):
    """
    Create matches.xlsx from curated match folder in MATCHES_PATH for each participant
    """
    print(f"Confirm matches in path {matches_path}...")
    if not os.path.exists(matches_path):
        click.echo("Path does not exist")
        return -1
    matches_df = pd.DataFrame(columns=[names['notification']['PERSON_ID'], names['notification']['MATCH_IDS']])
    files = os.listdir(matches_path)
    for f in files:
        person_id = os.path.splitext(f)[0]
        df = pd.read_csv(os.path.join(matches_path, f), sep=';')
        matches_df = matches_df.append({
            names['notification']['PERSON_ID']: person_id,
            names['notification']['MATCH_IDS']: df[names['notification']['FORM_ID']].tolist()
        }, ignore_index=True)
    matches_df.to_excel(os.path.join(matches_path, "matches.xlsx"), index=False)


@cli.command(name="notify")
@click.argument("matches_path")
@click.argument("people_path")
@click.option("-d", "--debug/--no-debug", help="Activate debug mode", default=False)
@click.option("-m", "--mode", help="Select FWB / Relationship / Friends mode", default="Relationship")
def notify(matches_path, people_path, debug, mode):
    """
    The matches in MATCHES PATH (previously calculated and curated matches by cli match command) is used to send
    mails to the participants defined in PEOPLE_PATH.
    """
    print(f"Processing matches from {matches_path} for mode {mode}, debug status {debug}")
    matches_df = pd.read_excel(matches_path)
    people_df = pd.read_excel(people_path)

    send_mails(matches_df, people_df, mode, debug=debug)


if __name__ == '__main__':
    cli(sys.argv[1:])

