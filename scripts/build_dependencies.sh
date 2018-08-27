#!/bin/bash

echo "Install Docker CE for Ubuntu"
echo "Docker is now called docker-ce (community edition)"

read -p "Press enter to remove old docker installs"
sudo apt-get remove docker docker-engine docker.io

read -p "Press enter to update packages"
sudo apt-get -y update

read -p "Press enter to Update and add Docker repo"
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo apt-key fingerprint 0EBFCD88

# TODO Create a check to make sure that the repo is already added
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update
sudo apt-get install docker-ce

read -p "Press enter to manage docker as a non-root user"
sudo groupadd docker
sudo usermod -aG docker $USER
