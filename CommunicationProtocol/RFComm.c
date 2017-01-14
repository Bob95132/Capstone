#include "RFStream.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/time.h>
#include <sys/types.h>
#include <unistd.h>

int SetUpConn(char *name, int comm) {
   int port;
   switch (comm) {
      case 0:   
      port = SetUpSerial(name);
      break;
      
      case 1:
      port = SetUpTCP(name);
      break;

      default:
      port = -2;
      fprintf(stdout, "ERROR: Communication Type Not Supported\n");
      break;
   }

   if (port == -1)
      fprintf(stdout, "CONNECTION_FAILURE\n");
   else
      fprintf(stdout, "CONNECTION_SUCCESS\n");

   return port;
}

int WriteProtocol(char *data, int port) {
   char *end = strchr(data, '\0');
   data[end - data] = '\r';
   data[end + 1 - data] = '\0';
   return SendData(data, strlen(data), port); // write to port
}

void ReadProtocol(int port, int sec, int usec, int flush) {
   fd_set rfds;
   struct timeval tv;

   FD_ZERO(&rfds);
   FD_SET(port, &rfds);
   tv.tv_usec = usec;
   tv.tv_sec = sec;
   char data[1000];
   int read = 0;

   while (select(port + 1, &rfds, NULL, NULL, &tv) > 0 && 
          ReceiveData(data, sizeof(data) - 1, port) > 0) {

      if (!flush) {
         if (data[0] == 'E')
            fprintf(stdout, "ERROR: Invalid Reader Command\n");
         else
            fprintf(stdout, "RECEIVED_DATA: %s", data);
      }
      FD_SET(port, &rfds);
      tv.tv_usec = usec;
      tv.tv_sec = sec;
      read = 1;
   }

   if (!flush && !read)
      fprintf(stdout, "CMD_SUCCESS\n");

}

void ClosePort(int *port) {
   char *str = (close(*port)) ? "CLOSE_FAILURE" : "CLOSE_SUCCESS";
   fprintf(stdout, "%s\n", str);
   *port = -1;
}


int main(int argc, char **argv) {
   char cmd[3], sPort[50], data[1000];
   int port = -1;
   int quit = 0;

   do {
      fscanf(stdin, "%s", cmd);
   
      if (!strcmp(cmd, "-s")) { // set up port
         if (fscanf(stdin, " %49s %d", sPort, &port) == 2) {
            port = SetUpConn(sPort, port);
         }
         else {
            fprintf(stdout, "ERROR: -s Parameters: <Port Name> <Communication Type>\n");
         }
      }

      else if (!strcmp(cmd, "-c")) { //send/receive data from port
         if (fscanf(stdin, " %99s", data) == 1) {
            if (port != -1) { 
               WriteProtocol(data, port);
               ReadProtocol(port, 0, 1000, 1);
               ReadProtocol(port, 1, 0, 0); 
            }
            else
               fprintf(stdout, "ERROR: port not opened\n");

         }
         else  
            fprintf(stdout, "ERROR: -c Parameters: <Port Name> <data>\n");
      }
      
      else if (!strcmp(cmd, "-d")) {// close port communication
         if (port != -1) 
            ClosePort(&port); 
         else
            fprintf(stdout, "ERROR: port not opened\n");
            
      }

      else if (!strcmp(cmd, "-q")) {
         if (port != -1)
            ClosePort(&port);
         fprintf(stdout, "EXITING\n");
         quit = 1;
      }
      
      else 
         fprintf(stdout, "ERROR: Command Not Recognized. List of availabe commands: -s, -c, -d, -q\n");
       
   } while (!quit);

   return 0;
}
