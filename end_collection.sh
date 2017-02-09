#!/bin/bash

ps | grep -f RF_PID
RUNNING=$?
read -r PID <RF_PID

if [ $RUNNING -eq 0 ]; then
   echo "Terminating RFManager..."
   kill -s SIGTERM $PID
fi
