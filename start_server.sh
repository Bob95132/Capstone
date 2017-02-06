#!/bin/bash

ps | grep -f SERV_PID
RUNNING=$?

if [ $RUNNING -eq 0 ];
then
    echo "PIUI Server already running."
    exit 1
else
    python ./RFServer/Server.py &>out &
    PID=$!
    echo $PID
    echo $PID > SERV_PID
    exit 0
fi


