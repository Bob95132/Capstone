#!/bin/bash

ps | grep -f SERV_PID
RUNNING=$?

if [ $RUNNING -eq 0 ];
then
    echo "PIUI Server already running."
    exit 1
else
    rm -rf RFManager/bin/RF_STATUS
    echo "Starting RFServer..."
    python ./RFServer/lib/Server.py &>./RFServer/log/out &
    PID=$!
    echo $PID
    echo $PID > SERV_PID
    exit 0
fi


