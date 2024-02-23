from translations.edit import app as application

import os

import click

@click.group()
def cli():
    pass

@cli.command()
@click.option('-p', '--port', default='30000', help='The port number')
def run(port):
    #Overwrite the default DB connection for HWI
    application.run(host="0.0.0.0", port=port)

def start_cli():
    """
    Set up an empty client
    """
    cli()

if __name__ == "__main__":
    start_cli()

