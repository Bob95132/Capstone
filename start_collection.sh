#!/bin/bash

ps | grep -f RF_PID
RUNNING=$?

if [ $RUNNING -eq 0 ];
then
    echo "RFManager already running."
else
    python ./RFManager/RFManager.py &
    PID=$!
    echo $PID
    echo $PID > RF_PID
fi


