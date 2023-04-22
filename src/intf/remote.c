#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>

#include "remote.h"

#define PORT 8080
#define RESOLUTION 384 * 224
#define FB_BUFFER_SIZE RESOLUTION * 2
#define RGB_BUFFER_SIZE RESOLUTION * 3

char remote_inputs[INPUT_COUNT];

static int remote_socket;

int RemoteInit() {
    remote_socket = socket(AF_INET, SOCK_STREAM, 0);

    struct sockaddr_in server_address;
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(PORT);
    server_address.sin_addr.s_addr = INADDR_ANY;

    int connection_status = connect(remote_socket, (struct sockaddr *) &server_address, sizeof(server_address));

    if (connection_status < 0) {
        close(remote_socket);
        remote_socket = 0;
        return 1;
    }

    return 0;
}

int RemoteSendBuffer(unsigned char* buffer) {
    if (!remote_socket) {
        return 1;
    }

    // for OpenGL pixel formats refer to https://afrantzis.com/pixel-format-guide/opengl.html

    unsigned char rgb_buffer[RGB_BUFFER_SIZE];
    unsigned short* bp = (unsigned short *)buffer;

    for (int i = 0; i < RESOLUTION; i++) {
        unsigned short pix = *(bp + i);

        float red = (pix >> 11) / (float)0b11111;
        float green = ((pix >> 5) & 0b111111) / (float)0b111111;
        float blue = (pix & 0b11111) / (float)0b11111;

        rgb_buffer[i * 3] = (unsigned char)(red * 255);
        rgb_buffer[i * 3 + 1] = (unsigned char)(green * 255);
        rgb_buffer[i * 3 + 2] = (unsigned char)(blue * 255);
    }

    send(remote_socket, rgb_buffer, RGB_BUFFER_SIZE, 0);

    // get inputs

    recv(remote_socket, remote_inputs, INPUT_COUNT, 0);

    return 0;
}
