#include <unistd.h>
#include <stdio.h>
#include <termios.h>
#include <stdlib.h>

typedef struct CommPort CommPort;

int OpenPort(CommPort *myPort, char *name, int type);
char *GetName(CommPort *myPort);
int GetType(Commport *myPort);
int GetPort(Commport *myPort);
int ClosePort(CommPort *myPort);
int SetUpSerial(CommPort *myPort);
int SendData(char *data, CommPort *myPort);
char *ReceiveData(char *buf, int size, CommPort *myPort);

int SetUpTCP(CommPort *myPort);
