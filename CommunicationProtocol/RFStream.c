#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <termios.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include "RFStream.h"

#define MAXRCV 500
#define PORTNUM 6500
#define BUFFSIZE 500

struct CommPort {
   char *name;
   int type; //tcp - 1, serial - 0;
   int comPort;
   
}

int OpenPort(CommPort *myPort, char *name, int type) {
   int success = 0;
   myPort = calloc(1, sizeof(myPort))   
   strcpy(myPort->name, name);
   myPort->type = type;

   if (myPort == NULL || myPort->name == 0)
      success = -1;
   
   return success;
}

char *GetName(CommPort *myPort) {
   return myPort->name; //Beware Hard Copy
}

int GetType(CommPort *myPort) {
   return myPort->type;
}

int GetPort(CommPort *myPort) {
   return myPort->comPort;
}

int ClosePort(CommPort *myPort) {
   close(myPort->comPort);
   free(myPort);
}

int SetUpSerial(Comport *myPort) {
   struct termios settings;
   memset(&settings, 0, sizeof(settings));
   myPort->comPort = open(myPort->name, O_RDWR | O_NOCTTY | O_SYNC);

   if (myPort->comPort < 0) 
      printf("Error opening %s: %s\n", port, strerror(errno));

   tcgetattr(myPort->comPort, &settings);

   cfsetispeed(&settings, B115200);
   cfsetospeed(&settings, B115200);

   options.c_cflag |= (CLOCAL | CREAD);

   options.c_cflag &= ~PARENB;
   options.c_cflag &= ~CSTOPB;
   options.c_cflag &= ~CSIZE;
   options.c_cflag |= CS8;
   
   options.c_cflag &= ~CNEW_RTSCTS;

   options.c_iflag = 0;
   options.c_iflag = ICRNL;
   options.c_oflag = 0;
   options.c_oflag = ONLCR;

   options.c_cc[VMIN] = 0;
   options.c_cc[VTIME] = 5;

   if (tcsetattr(myPort->comPort, TCSANOW, &options) != 0) {
      printf("Set Attribute Error: %d\n", errno);
      myPort->comPort = -1;
   }
   
   return myPort->comPort > -1;
}

int SendData(char *data, int size, Comport *myPort) {
   int len = write(myPort->comPort, data, size);
   if (len != size)
      printf("Error from write: %d, %d\n", len, errno);
}


char *ReceiveData(char *buf, int size, CommPort *myPort) {
   int len = read(myPort->comPort, buf, sizeof(buf) - 1);
   
   if (len > 0)
      buf[len] = 0;
   else {
      printf("Error from read: %d: %s\n", len, strerror(errno));
      buff[0] = 0;
   }
   
   return buff;
}

int SetUpTCPOut(Commport *myPort) {
   struct sockaddr_in dest;

   memset(&dest, 0, sizeof(dest));
   myPort->comPort = socket(AF_INET, SOCK_STREAM, 0);

   dest.sin_family = AF_INET;
   dest.sin_addr.s_addr = inet_pton(myPort->name);

   dest.sin_port = htons(PORTNUM);

   if (connect(myPort->comPort, (struct sockaddr *)&dest, sizeof(struct sockaddr_in)) != 0) {
      printf("Error in Connection: %d\n", errno);
      myPort->comPort = -1;
   }

   return myPort->comPort > -1;
}

void TComm(char *name) {
   
}
