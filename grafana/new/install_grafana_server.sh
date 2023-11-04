#!/bin/sh

# install grafana-server
# ref: https://grafana.com/docs/grafana/latest/installation/debian/

sudo apt-get install -y adduser libfontconfig1 musl
wget https://dl.grafana.com/oss/release/grafana_10.2.0_amd64.deb
sudo dpkg -i grafana_10.2.0_amd64.deb
 
# Start Grafana server
sudo service grafana-server start

#service grafana-server status

