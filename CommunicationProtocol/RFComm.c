#include "RFStream.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/time.h>
#include <sys/types.h>
#include <unistd.h>

int main(int argc, char **argv) {
   int port;
   char cmd[3], sPort[50], data[1000];
   fd_set rfds;
   struct timeval tv;
   char *indexOfNL;
   int quit = 0;

   do {
      fscanf(stdin, "%2s ", cmd);
   
      if (!strcmp(cmd, "-s")) { // set up port
         if (fscanf(stdin, "%49s %d", sPort, &port) == 2) {
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
               fprintf(stderr, "ERROR: Communication Type Not Supported\n");
               break;
            }
         }
         else {
            fprintf(stderr, "ERROR: -s Parameters: <Port Name> <Communication Type>\n");
         }
      }

      else if (!strcmp(cmd, "-c")) { //send/receive data from port
         if (fgets(data, 99, stdin) != NULL) {
            indexOfNL = strchr(data, '\n');
            *indexOfNL = '\r';
            FD_ZERO(&rfds);
            FD_SET(port, &rfds);
            tv.tv_sec = 2;
         
            //write to port when select reports ready
           // if (select(port, NULL, &wfds, NULL, NULL) > 0 && pval == 0)
            if (SendData(data, strlen(data), port) == -1) // write to port
               fprintf(stderr, "ERROR: %s\n", strerror(errno));
            //read from port when select is ready and until the buffer is empty
            while (select(port + 1, &rfds, NULL, NULL, &tv) > 0) {
               if (ReceiveData(data, sizeof(data) - 1, port) == -1) {// read from port
                  fprintf(stderr, "ERROR: %s\n", strerror(errno));
                  break;
               }
              
               fprintf(stdout, "RECEIVED_DATA: %s", data);   
               FD_SET(port, &rfds);
               tv.tv_sec = 2;
            }

         }
         else  
            fprintf(stderr, "ERROR: -c Parameters: <Port Name> <data>\n");
      }

      else if (!strcmp(cmd, "-d")) {// close port communication
         if (close(port))  //close port
            fprintf(stdout, "CLOSE_FAILURE\n");
         else
            fprintf(stdout, "CLOSE_SUCCESS\n");
         break;
      }

      else if (!strcmp(cmd, "-q"))
         break;
      
      else 
         fprintf(stderr, "ERROR: Command Not Recognized. List of availabe commands: -s, -c, -d, -q\n");
       
   } while (1);

   return 0;
}
