#pragma once

#define INPUT_COUNT 29

#ifdef __cplusplus
extern "C" {
#endif

extern char remote_inputs[INPUT_COUNT];
extern char remote_should_reset;

int RemoteInit();
int RemoteCommunicate(unsigned char* buffer);

#ifdef __cplusplus
}
#endif
