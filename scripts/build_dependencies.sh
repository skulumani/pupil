#!/bin/bash
set +e
options=("Yes" "No" "Quit")
prompt () {
    echo "Are you sure you want to $1"
    select yn in "${options[@]}"; do
        case $yn in 
            Yes ) eval "$2";
                break;;
            No ) break;;
            exit ) exit;;
        esac
    done
}

DOCKER_REPO=https://download.docker.com/linux/ubuntu

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
if ! grep -q "^deb .*${DOCKER_REPO}" /etc/apt/sources.list /etc/apt/sources.list.d/*; then
    sudo add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"
fi

sudo apt-get update
prompt "Install docker" "sudo apt-get install docker-ce"

prompt "Setup docker for non-root user" "sudo groupadd docker || sudo usermod -aG docker $USER"

prompt "Setup Rockwell Collins proxy for Docker" "sudo mkdir /etc/systemd/system/docker.service.d && sudo cp ./scripts/http-proxy.conf /etc/systemd/system/docker.service.d"

echo "You may need to restart to get group access"
echo "Try running docker run hello-world"
