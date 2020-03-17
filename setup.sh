#!/bin/bash
sudo apt-get update
sleep 1
sudo apt install software-properties-common -y
sleep 1
sudo apt-add-repository --yes --update ppa:ansible/ansible
sleep 1
sudo apt-get install ansible -y
sleep 1
sudo pip install junos-eznc jxmlease pynetbox
sleep 1
ansible-galaxy install Juniper.junos
sleep 1
pip install --upgrade jinja2
sleep 1
sudo apt-get install docker.io -y
sleep 1
sudo usermod -aG docker jcluser
sleep 1
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sleep 1
sudo chmod +x /usr/local/bin/docker-compose
sleep 1
sudo systemctl start docker
sleep 1
sudo systemctl enable docker
sleep 1
git clone https://github.com/netbox-community/netbox-docker.git
sleep 1
cd netbox-docker
sleep 1
sed -i 's/8080/80:8080/gi' docker-compose.yml
sleep 1
sudo docker-compose pull
sleep 1
sudo docker-compose up -d
sleep 1
