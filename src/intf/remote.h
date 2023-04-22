#pragma once

#define INPUT_COUNT 29

#ifdef __cplusplus
extern "C" {
#endif

extern char remote_inputs[INPUT_COUNT];

int RemoteInit();
int RemoteSendBuffer(unsigned char* buffer);

#ifdef __cplusplus
}
#endif
