#!/bin/bash

ps | grep -f SERV_PID
RUNNING=$?
read -r PID <SERV_PID

if [ $RUNNING -eq 0 ]; then
   echo "Terminating RFServer..."
   kill -s SIGKILL $PID
   ./end_collection.sh
fi
