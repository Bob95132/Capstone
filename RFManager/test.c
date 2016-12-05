#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char **argv) {
   int i;
   int j;
   char args[1000];
   char *a = args;
   for (i = 0; i < argc; i++) {
      char *p = argv[i];
      while(*p != '\0') {
         *a = *p;
         a++;
         p++;
      }
      *a = ' ';
      a++;
   }
   fprintf(stdout, "Hello: %s\n", args);
   fflush(stdout);
   while(1) {
      char flag[2];
      char data[100];
      fscanf(stdin, "%s %s", flag, data);
      fprintf(stdout, "RECEIVED_DATA: %s %s\n", flag, data);
      fflush(stdout);
      if (strcmp("-q", flag) == 0) {
         break;
      }
   }
   fprintf(stdout, "exiting...\n");
   exit(0);
}
