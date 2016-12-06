#!/bin/bash

python ./RFManager/RFManager.py &

PID = $!
echo PID
echo PID > RF_PID

