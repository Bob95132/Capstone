#!/bin/bash

ps | grep -f RF_PID
RUNNING=$?
read -r PID<RF_PID

if [ $RUNNING -eq 0 ]; then
   kill -2 $PID
fi
