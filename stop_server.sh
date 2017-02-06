#!/bin/bash

ps | grep -f SERV_PID
RUNNING=$?
read -r PID <SERV_PID

if [ $RUNNING -eq 0 ]; then
   kill -s SIGTERM $PID
fi