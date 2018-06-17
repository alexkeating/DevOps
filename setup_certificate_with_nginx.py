import os

from invoke import Responder
from fabric import Connection, Config

# Directions provided by a Digital Ocean tutorial
# https://www.digitalocean.com/community/tutorials/how-to-set-up-let-s-encrypt-with-nginx-server-blocks-on-ubuntu-16-04

# Helpful Articles for setting up DNS in Digital ocean
# https://www.digitalocean.com/community/tutorials/an-introduction-to-dns-terminology-components-and-concepts
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
c.run(f'touch /etc/nginx/sites-available/{args.domain}', pty=True, watchers=[responder])
c.run(f'echo "server_name example.com www.{args.domain};" >> touch /etc/nginx/sites-available/{args.domain};')
c.run("sudo ufw allow 'Nginx Full'", pty=True)
c.run("sudo ufw delete allow 'Nginx HTTP'", pty=True)
c.run("sudo ufw delete allow 'Nginx HTTPS'", pty=True)  # This line may be okay to omit. Depending on server config
c.run('sudo ufw status', pty=True)
c.run(f'sudo certbot --nginx -d {args.domain} -d www.{args.domain}', pty=True)
c.run('sudo certbot renew')
c.run('sudo apt-get remove python-certbot-nginx', pty=True, watchers=[responder])
