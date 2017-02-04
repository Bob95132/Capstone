#!/bin/sh

sudo ifdown wlan0
sudo cp ./InternetConfiguration /etc/network/interfaces
sudo systemctl daemon-reload
sudo service dnsmasq stop
sudo service hostapd stop
sudo service dhcpcd restart
sudo service networking restart 
sudo ifup wlan0


