#include "RFStream.h"

int main(int argc, char **argv) {
   char line[BUFFSIZE];
   char rline[BUFFSIZE];
   CommPort *myPort;

   if (argc > 3) {
      NewCommPort(myPort, argv[1], argv[2]);      

      if (myPort->type == 0)
         SetUpSerial(myPort);
      else
         SetUpTCP(myPort); 

      while(strcmp(line, "-q") != 0) {
         if (fgets(line, BUFFSIZE - 1, stdin) != NULL && strcmp(line, "-q") != 0) {
            SendData(line, BUFFSIZE - 1, myPort->comPort);
            select(GetPort(   
            ReceiveData(rline, BUFFSIZE, myPort->comPort);
            printf("%s", rline);
         }
      }
   }

   free(myPort);       
}

}
