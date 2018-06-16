#!/usr/bin/env bash

# Digital Ocean Tutorial
# https://www.digitalocean.com/community/tutorials/how-to-install-jenkins-on-ubuntu-16-04

# Install and run
wget -q -O - https://pkg.jenkins.io/debian/jenkins-ci.org.key | sudo apt-key add -
echo deb https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list
sudo apt-get update
sudo apt-get install jenkins
sudo systemctl start jenkins

# Open Firewall
sudo ufw allow 8080
sudo ufw status

# Setting up the UI
sudo cat /var/lib/jenkins/secrets/initialAdminPassword


# Digital Ocean Tutorial
# https://www.digitalocean.com/community/tutorials/how-to-configure-jenkins-with-ssl-using-an-nginx-reverse-proxy
# Add SSL and NGINX reverse proxy