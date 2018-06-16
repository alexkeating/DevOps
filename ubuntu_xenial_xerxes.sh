#!/usr/bin/env bash

# Initial server set up digital
# https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-16-04


# sudo su -c "useradd alex -s /bin/bash -m"
# sudo chpasswd << 'test'
# Not sure the change password command works

# Create user group sudo - needs to be done inn root
usermod -aG sudo alex

# Done on local
# Local user depends on the user name
ssh-keygen -t rsa -N "" -f /Users/localuser/.ssh/id_rsa

# Copy local ssh key to machine
# Mac brew install ssh-copy-id

su - alex
mkdir ~/.ssh
chmod 700 ~/.ssh

# Copy public key

# Turn off password authetication
sudo nano /etc/ssh/sshd_config
sudo systemctl reload sshd

# Set Up Firewall
sudo ufw app list
sudo ufw allow OpenSSH
sudo ufw enable
echo "y" | sudo ufw enable