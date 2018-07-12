import os

from invoke import Responder
from fabric import Connection, Config

"""
This script the lastest supported version of mysql on Ubuntu.
Please provide a command line argument for the server you wish to
add docker to.

The below digital ocean link was invaluable.
select * from mysql.user;
https://stackoverflow.com/questions/10299148/mysql-error-1045-28000-access-denied-for-user-billlocalhost-using-passw
https://stackoverflow.com/questions/14779104/how-to-allow-remote-connection-to-mysql#
https://www.digitalocean.com/community/tutorials/how-to-create-a-new-user-and-grant-permissions-in-mysql
https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-16-04
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
c.run('sudo apt-get install mysql-server', pty=True, watchers=[responder])
c.run('mysql_secure_installation', pty=True, watchers=[responder])
c.run('systemctl status mysql.service', pty=True, watchers=[responder])
