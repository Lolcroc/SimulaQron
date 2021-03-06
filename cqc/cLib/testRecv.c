#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>

// #include <stdlib.h>

#include <netinet/in.h>
#include <netdb.h>

#include <string.h>
#include<arpa/inet.h>

#include "cqc.h"

int main(int argc, char *argv[]) {

	uint16_t portno;
	char *hostname;
	cqc_lib *cqc;
	int app_id;
	uint16_t qubit;

	/* Retrieve arguments from command line */
	if (argc != 3) {
		fprintf(stderr,"usage %s hostname port\n", argv[0]);
		exit(0);
   	}
	hostname = argv[1];
   	portno = atoi(argv[2]);

	/* In this example, we are simply application 10 */
	app_id = 10;

	/* In this example, we will not check for errors. All functions return -1 on failure */
	cqc = cqc_init(app_id);
	cqc_connect(cqc, hostname, portno);

	qubit = cqc_recv(cqc);

	(void) qubit;

   	return 0;
}
