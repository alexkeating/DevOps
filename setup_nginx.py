import os

from invoke import Responder
from fabric import Connection, Config

# Directions provided by a Digital Ocean tutorial
# https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-16-04
SERVER_ADDRESS = os.getenv('SERVER_ADDRESS', '')
c = Connection(SERVER_ADDRESS)
responder = Responder(
    pattern=r"Do you want to continue\? \[Y/n\]",
    response="y\n",
)
c.run('sudo apt-get update', pty=True)
c.run('sudo apt-get install nginx', pty=True, watchers=[responder])
app_list = c.run('sudo ufw app list', pty=True)
c.run("sudo ufw allow 'Nginx HTTP'", pty=True)
c.run('systemctl status nginx', pty=True)

