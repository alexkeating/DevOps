import os

from invoke import Responder
from fabric import Connection, Config

"""
This script will install certbot and create a certificate for 
the provided domain.

The below digital ocean link was invaluable.
https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-16-04
"""
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--server_address", type=str, action="store",
                    help="The connection string to the server. Usually user@ip.")
parser.add_argument("-d", "--domain", action="store", type=str,
                    help="Domain for the nginx server block. Example would be example.com."
                         "Please omit the www.")
args = parser.parse_args()

if not args.server_address:
    print("No server address provided")
    exit(1)

if not args.domain:
    print("No domain provided")
    exit(1)

c = Connection(args.server_address)
responder = Responder(
    pattern=r"Do you want to continue\? \[Y/n\]",
    response="y\n",
)
c.run('sudo add-apt-repository ppa:certbot/certbot', pty=True, watchers=[responder])
c.run('sudo apt-get update', pty=True, watchers=[responder])
c.run('sudo apt-get install python-certbot-nginx', pty=True, watchers=[responder])
c.run('sudo ufw status', pty=True)
c.run(f'sudo certbot --nginx -d {args.domain} -d www.{args.domain}', pty=True)
c.run('sudo certbot renew')
