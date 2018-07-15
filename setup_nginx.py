import os

from invoke import Responder
from fabric import Connection, Config

# Directions provided by a Digital Ocean tutorial
# https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-16-04
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
c.run('sudo apt-get update', pty=True)
c.run('sudo apt-get install nginx', pty=True, watchers=[responder])
app_list = c.run('sudo ufw app list', pty=True)
c.run("sudo ufw allow 'Nginx HTTP'", pty=True)
c.run('systemctl status nginx', pty=True)

