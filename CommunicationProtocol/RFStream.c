#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <termios.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/time.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include "RFStream.h"

#define MAXRCV 500
#define PORTNUM 6500
#define BUFFSIZE 500

/* 
SetUpSerial: opens a file descriptor to communicate 
             using UART to external devices
inputs: name(string): the string address of the port 
                      the device is connected to
outputs: comPort(int): the opened file descriptor to the port or -1 for failed open
*/

int SetUpSerial(char *name) {
   struct termios settings; //struct holding all settings to USB connection
   memset(&settings, 0, sizeof(settings)); //zero out struct
   int comPort = open(name, O_RDWR | O_NOCTTY | O_SYNC);

   if (comPort == -1)
      fprintf(stderr, "Error opening %s: %s\n", name, strerror(errno));

   else { 
      tcgetattr(comPort, &settings); // get current attributes

      cfsetispeed(&settings, B115200); // set input baud rate
      cfsetospeed(&settings, B115200); // set output baud rate

      settings.c_cflag |= (CLOCAL | CREAD); // local port and receiver

      settings.c_cflag &= ~PARENB; // no parity
      settings.c_cflag &= ~CSTOPB; // 1 stop bit, o.w. 2
      settings.c_cflag &= ~CSIZE; // clear size
      settings.c_cflag |= CS8; // set to 8 data bits
   
      settings.c_cflag &= ~CRTSCTS; // turn off hardware control
      
      settings.c_lflag = 0;

      settings.c_iflag = 0; //turns off editable input
                                         // bit stripping, and software control
      settings.c_iflag = ICRNL; // set carriage returns to new lines on ipnut
      settings.c_oflag = 0; // clear output config

      settings.c_cc[VMIN] = 0; // set minimum character 
      settings.c_cc[VTIME] = 150;  // set time between characters

      if (tcsetattr(comPort, TCSANOW, &settings) != 0) { //set attributes now
         fprintf(stderr, "Set Attribute Error: %s\n", strerror(errno));
         comPort = -1;
      }
   }
   
   return comPort;
}
/*
SetUpTCP: takes an IP Address and opens file descriptor 
          to a socket for read/write purposes
inputs: name(string): string format of IP address
output: comport(int): file descriptor to socket, or -1 for failed open
*/

int SetUpTCP(char *name) {
   struct sockaddr_in dest;

   memset(&dest, 0, sizeof(dest)); // zero sockaddr_in struct
   int comPort = socket(AF_INET, SOCK_STREAM, 0); // create socket for IPV4 TCP

   dest.sin_family = AF_INET; //destination IPV4
   inet_pton(AF_INET, name, &dest.sin_addr.s_addr); //set destination address

   dest.sin_port = htons(PORTNUM); // set destination port

   if (connect(comPort, (struct sockaddr *)&dest, sizeof(struct sockaddr_in)) != 0) { // open socket
      fprintf(stderr, "Error connecting to ip address: %s\n", strerror(errno));
      comPort = -1;
   }

   return comPort;
}

/*
SendData: sends data over the port 
inputs: data(string): text to be written
        size(int): size of data to be written
        port(int): port to be written to
output: len(int): number of bytes sent, or -1 for failed write
*/

int SendData(char *data, int size, int port) {
   int len = write(port, data, size);
   if (len == -1)
      fprintf(stderr, "Error from write: %s\n", strerror(errno));

   return len;
}

/*
ReceivesData: receives data over the port 
inputs: buf(string): text received
        size(int): max load of data to be received
        port(int): port to be read from
output: len(int): number of bytes read, of -1 for failed read
*/

int ReceiveData(char *buf, int size, int port) {
   int len = read(port, buf, size - 1);
   
   if (len > -1)
      buf[len] = 0;
   else {
      fprintf(stderr, "Error from read: %s\n", strerror(errno));
      buf[0] = 0;
   }
   
   return len;
}


