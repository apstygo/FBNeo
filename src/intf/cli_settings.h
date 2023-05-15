#ifndef cli_settings_h
#define cli_settings_h

#include <stdio.h>

struct CLISettings {
    uint8_t headless;
    uint8_t sound;
    uint8_t skipped_frames;
};

extern struct CLISettings cli_settings;

#endif /* cli_settings_h */
