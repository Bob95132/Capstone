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

int SetUpSerial(char *name) {
   struct termios settings;
   memset(&settings, 0, sizeof(settings));
   int comPort = open(name, O_RDWR | O_NOCTTY | O_SYNC);

   if (comPort < 0) 
      printf("Error opening %s: %s\n", port, strerror(errno));

   tcgetattr(comPort, &settings);

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

   if (tcsetattr(comPort, TCSANOW, &options) != 0) {
      printf("Set Attribute Error: %d\n", errno);
      comPort = -1;
   }
   
   return comPort;
}

int SetUpTCP(char *name) {
   struct sockaddr_in dest;

   memset(&dest, 0, sizeof(dest));
   int comPort = socket(AF_INET, SOCK_STREAM, 0);

   dest.sin_family = AF_INET;
   dest.sin_addr.s_addr = inet_pton(myPort->name);

   dest.sin_port = htons(PORTNUM);

   if (connect(comPort, (struct sockaddr *)&dest, sizeof(struct sockaddr_in)) != 0) {
      printf("Error in Connection: %d\n", errno);
      comPort = -1;
   }

   return comPort;
}

int SendData(char *data, int size, int port) {
   int len = write(port, data, size);
   if (len != size)
      fprintf(stderr, "Error from write: %d, %d\n", len, errno);
}

char *ReceiveData(char *buf, int size, int port) {
   int len = read(comPort, buf, size - 1);
   
   if (len > 0)
      buf[len] = 0;
   else {
      fprintf(stderr, "Error from read: %d: %s\n", len, strerror(errno));
      buff[0] = 0;
   }
   
   return buff;
}


