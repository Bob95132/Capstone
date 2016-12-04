#include <unistd.h>
#include <stdio.h>
#include <termios.h>
#include <stdlib.h>

int SetUpSerial(char *name);
int SetUpTCP(char *name);
int SendData(char *data, int size, int port);
int ReceiveData(char *buf, int size, int port);

