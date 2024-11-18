#ifndef CAM_DEV_H
#define CAM_DEV_H

// include files
#include <Arduino.h>
#include <esp_camera.h>

// public defines
// public constants

// public variables

// public functions
bool cam_dev_init(void);
int cam_dev_snapshot(uint8_t *out_buf);

#endif // CAM_DEV_H