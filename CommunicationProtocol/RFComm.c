#include "RFStream.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/time.h>
#include <sys/types.h>
#include <unistd.h>

int main(int argc, char **argv) {
   char cmd[3], sPort[50], data[1000];
   fd_set rfds;
   struct timeval tv;
   char *indexOfNL;
   int port = -1;
   int quit = 0;

   do {
      fscanf(stdin, "%s", cmd);
   
      if (!strcmp(cmd, "-s")) { // set up port
         if (fscanf(stdin, " %49s %d", sPort, &port) == 2) {
            switch (port) {
               case 0:
               if ((port = SetUpSerial(sPort)) == -1)
                  fprintf(stdout, "CONNECTION_FAILURE\n");
               else
                  fprintf(stdout, "CONNECTION_SUCCESS\n");
               break;
      
               case 1:
               if ((port = SetUpTCP(sPort)) == -1) 
                  fprintf(stdout, "CONNECTION_FAILURE\n");
               else
                  fprintf(stdout, "CONNECTION_SUCCESS\n");
               break;

               default:
               fprintf(stdout, "ERROR: Communication Type Not Supported\n");
               break;
            }
         }
         else {
            fprintf(stdout, "ERROR: -s Parameters: <Port Name> <Communication Type>\n");
         }
      }

      else if (!strcmp(cmd, "-c")) { //send/receive data from port
         if (fscanf(stdin, " %99s", data) == 1) {
            indexOfNL = strchr(data, '\0');
            data[indexOfNL - data] = '\r';
            data[indexOfNL + 1 - data] = '\0';
            FD_ZERO(&rfds);
            FD_SET(port, &rfds);
            tv.tv_usec = 1;
            tv.tv_sec = 0;

            if (port != -1) { 
               while (select(port + 1, &rfds, NULL, NULL, &tv) > 0) {
                  if (ReceiveData(data, sizeof(data) - 1, port) == -1) // read from port
                     break;
                  FD_SET(port, &rfds);
                  tv.tv_usec = 1;
                  tv.tv_sec = 0;
               }
               FD_SET(port, &rfds);
               tv.tv_sec = 1;
               tv.tv_usec = 0;
               //write to port when select reports ready
               SendData(data, strlen(data), port); // write to port
               //read from port when select is ready and until the buffer is empty
               while (select(port + 1, &rfds, NULL, NULL, &tv) > 0) {
                  if (ReceiveData(data, sizeof(data) - 1, port) == -1) // read from port
                     break;
                  fprintf(stdout, "RECEIVED_DATA: %s", data);   
                  FD_SET(port, &rfds);
                  tv.tv_sec = 1;
                  tv.tv_usec = 0;
               }
            }
            else
               fprintf(stdout, "ERROR: port not opened\n");

         }
         else  
            fprintf(stdout, "ERROR: -c Parameters: <Port Name> <data>\n");
      }

      else if (!strcmp(cmd, "-d")) {// close port communication
         if (port != -1) {
            if (close(port))  //close port
               fprintf(stdout, "CLOSE_FAILURE\n");
            else
               fprintf(stdout, "CLOSE_SUCCESS\n");

            port = -1;
         }
         else
            fprintf(stdout, "ERROR: port not opened\n");
            
      }

      else if (!strcmp(cmd, "-q")) {
         fprintf(stdout, "EXITING\n");
         quit = 1;
      }
      
      else 
         fprintf(stdout, "ERROR: Command Not Recognized. List of availabe commands: -s, -c, -d, -q\n");
       
   } while (!quit);

   return 0;
}
