#include <sys/socket.h>
#include <netinet/in.h>

#define SERVER_IP_ADDR "127.0.0.1"
#define SERVER_PORT 2000

char server_message[100];

int main(void) {
    int clientSocket = socket(PF_INET, SOCK_DGRAM, 0);

    if (clientSocket == -1) {
        printf("ERROR to create socket");
        return 0;
    }

    struct sockaddr_in sa;
    memset(&sa, 0, sizeof(sa));
    sa.sin_family = AF_INET;
    sa.sin_addr.s_addr = inet_addr(SERVER_IP_ADDR);
    sa.sin_port = htons(SERVER_PORT);

    int l = 1;
    int r = 42;
    char buffer[200];

    char LESS[] = "LESS";
    char MORE[] = "MORE";
    char WIN[] = "WIN";
    char LOSE[] = "LOSE";
    int sa_size = sizeof(sa);

    while (l <= r) {
        int num = (l + r) / 2;
        char snum[10];

        sprintf(snum, "%d", num);
        strcpy(buffer, snum);

        int bytes_sent = sendto(clientSocket, buffer, strlen(buffer), 0, (struct sockaddr *) &sa, sizeof(sa));

        if (bytes_sent < 0) {
            return -1;
        }

        memset(server_message, '\0', sizeof(server_message));

        if (recvfrom(clientSocket, server_message, sizeof(server_message), 0, (struct sockaddr *) &sa, &sa_size) < 0) {
            printf("%s", "FINE \n");
            return -1;
        }

        printf("%s \n", server_message);

        if (strcmp(server_message, WIN) == 0 || strcmp(server_message, LOSE) == 0) {
            return 0;
        }

        if (strcmp(server_message, LESS) == 0) {
            l = num + 1;
        } else {
            r = num - 1;
        }

    }

    return 0;
}