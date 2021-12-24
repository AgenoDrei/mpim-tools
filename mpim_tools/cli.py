import click


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
