# RFManager
Python application for scanning RFID inventory and writing the results of inventory scans to file. RFManger uses the
RFComm C application from /CommunicationProtocol in order to communicate with the RFID reader device.
 
## To Install
use pip to install python dependencies
```
sudo pip install pexpect
sudo pip install xlswriter
```
create a log folder
```
cd RFManager
mkdir log
```
verify that the RFComm.c application has been compiled in ../CommunicationProtocol

## To Configure
All configuration for RFManager is done in /conf/rfid.conf

The default configuration looks for a target directory called ScanData in the Capstone root directory as the location 
in which to put all completed inventory reports.
Either change the RFSCAN_PATH property in /conf/rfid.conf, or create the ScanData/ target inside the Capstone root directory with:
```
cd path/to/Capstone/root/
mkdir ScanData
```
 
## To Run
Run RFManager to start collecting RFID inventory from the reader device by executing the startup script from the Capstone root directory
```
./start_collection.sh
```
*Note: to check the current progress of an inventory scan execute the check_scan script from the Capstone root directory*
```
./check_scan.sh
```
