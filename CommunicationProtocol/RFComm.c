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
   int size;
   char *indexOfNL;
   int pval = 0;
   int com = -1;
   int quit = 0;

   do {
      fscanf(stdin, "%2s ", cmd);
   
      if (!strcmp(cmd, "-s")) { // set up port
         if (fscanf(stdin, "%49s %d", sPort, &port) == 2) {
            switch (port) {
               case 0:
               if ((port = SetUpSerial(sPort)) == -1)
                  pval = 1;
               break;
      
               case 1:
               if ((port = SetUpTCP(sPort)) == -1) 
                  pval = 1;  
               break;

               default:
               fprintf(stderr, "Communication Type Not Supported: %d\n", com);
               pval = 1;
               break;
            }
         }
         else {
            fprintf(stderr, "RFCom -s Parameters: <Port Name> <Communication Type>\n");
            pval = 1;
         }
      }

      else if (!strcmp(cmd, "-c")) { //send/receive data from port
         if (fgets(data, 99, stdin) != NULL) {
            indexOfNL = strchr(data, '\n');
            *indexOfNL = '\r';
            //write to port when select reports ready
           // if (select(port, NULL, &wfds, NULL, NULL) > 0 && pval == 0)
            pval = ((size = SendData(data, strlen(data), port)) == -1) ? 1 : 0; // write to port
            printf("Write Size: %d\n", size);
            //read from port when select is ready and until the buffer is empty
            if (!pval) {
               pval = ((size = ReceiveData(data, sizeof(data) - 1, port)) == -1) ? 1 : 0;// read from port
               fprintf(stdout, "Size: %d %s", size, data);   
            }
         }
         else  {
            fprintf(stderr, "RFCom -c Parameters: <Port Name> <data>\n");
            pval = 1;
         }
      }

      else if (!strcmp(cmd, "-d")) // close port communication
         pval = (close(port) == -1) ? 1 : 0; //close port

      else if (!strcmp(cmd, "-q"))
         quit = 1;
      
      else {
         pval = 1;
         fprintf(stderr, "Command Not Recognized. List of availabe commands: -s, -c, -d, -q\n");
      } 
   } while (!quit && !pval);

   return pval;
}
