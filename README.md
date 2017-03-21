# Capstone
Repository for the Active RFID Inventory Capstone project. This software is developed for the Raspberry Pi 3 and Raspbian OS.
 
 ##Components
 1. Communication Protocol
 2. RFManager
 3. RFServer
 
 ##To Install
 See README for each of the above components
 
 ##To Run
 1. Configure Raspberry Pi 3 as a WiFi hotspot using the start_ap.sh script in /NetConfig/
 
```
cd NetConfig/
./start_ap.sh
```
* Ensure that you can pair to the Pi's WiFi access point using the default WiFi password
*Note: reconfigure Raspberry Pi's network interface to access the internet using start_internet.sh from /NetConfig/*


2. Start the PIUI server using the startup script in the root directory
```
./start_server.sh
```

* Ensure that you are able to load the RFConnect page by opening a web browser on the device you connected to the
Pi's WiFi access point and navigating to the address:
```
http://192.168.1.1:9999
```

*If everything is set up, you should get the RFConnect interface with start and stop buttons for the inventory scan.
