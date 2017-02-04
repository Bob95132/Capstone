#!/bin/sh

sudo ifdown wlan0
sudo cp ./AccessPointConfiguration /etc/network/interfaces
sudo systemctl daemon-reload
sudo service networking restart 
sudo service hostapd restart
sudo service dnsmasq restart
sudo ifup wlan0
