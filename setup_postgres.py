import os

from invoke import Responder
from fabric import Connection, Config

"""
This script the lastest supported version of postges on Ubuntu.
Please provide a command line argument for the server you wish to
add docker to.

The below digital ocean link was invaluable.
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04
"""
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--server_address", type=str, action="store",
                    help="The connection string to the server. Usually user@ip.")
args = parser.parse_args()

if not args.server_address:
    print("No server address provided")
    exit(1)

c = Connection(args.server_address)
responder = Responder(
    pattern=r"Do you want to continue\? \[Y/n\]",
    response="y\n",
)
c.run('sudo apt-get update', pty=True, watchers=[responder])
c.run('sudo apt-get install postgresql postgresql-contrib', pty=True, watchers=[responder])
c.run('createuser --interactive', pty=True, watchers=[responder])
