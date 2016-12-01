#include "RFStream.h"
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <sys/types.h>
#include <unistd.h>

int main(int argc, char **argv) {
   fd_set rfds, wfds;
   struct timeval tv;
   int retval;
   char buf[100];

   if (argc > 1) {
      if (!strcmp(argv[1], "-s")) {
         if (argc == 4) {
            switch (atol(argv[3])) {
               case 0:
               fprint(stdout, "Port Number: %d", SetUpSerial(argv[2]);
               break;
      
               case 1:
               fprint(stdout, "Port Number: %d", SetUpTCP(argv[2]);
               break;
            }
         }
         else
            fprintf(stderr, "RFCom -s Parameters: <Port Name> <Communication Type>");
      }

      if (!strcmp(argv[1], "-c")) {
         if (argc == 4) {
            memset(&tv, 0, sizeof(tv));
            FD_ZERO(&rfds);
            FD_ZERO(&rfds);
            FD_SET(atol(argv[2]), &rfds);
            FD_SET(atol(argv[2]), &wfds);
            tv.tv_usec = 1000;
         
            if (select(atol(argv[2]), NULL, &wfds, NULL, &tv) > 0)
               SendData(argv[3], strlen(argv[3]), atol(argv[2]));
            while (select(atol(argv[2]), &rfds, NULL, NULL, &tv) > 0) {
               ReceiveData(buf, sizeof(buf) - 1, atol(argv[2]));
               fprintf(stdout, "%s\n", buf);
               FD_SET(atol(argv[2]), &rfds);
            }
         }
      }

      if (!strcmp(argv[1], "-d")) {
         if (argc == 3)
            close(atol(argv[2]));
         else 
            fprintf(stderr, "RFCom -d Parameters: <Port Number>");
      }
   }

   return 0;
}
