#include <Arduino.h>
#include <esp_camera.h>

// static variables
camera_config_t camera_config = {
    .pin_pwdn = -1,
    .pin_reset = 18,
    .pin_xclk = 14,
    .pin_sscb_sda = 4,
    .pin_sscb_scl = 5,
    .pin_d7 = 15,
    .pin_d6 = 16,
    .pin_d5 = 17,
    .pin_d4 = 12,
    .pin_d3 = 10,
    .pin_d2 = 8,
    .pin_d1 = 9,
    .pin_d0 = 11,
    .pin_vsync = 6,
    .pin_href = 7,
    .pin_pclk = 13,
    .xclk_freq_hz = 20000000,
    .ledc_timer = LEDC_TIMER_0,
    .ledc_channel = LEDC_CHANNEL_0,
    .pixel_format = PIXFORMAT_RGB565,
    .frame_size = FRAMESIZE_QQVGA,
    .jpeg_quality = 12,
    .fb_count = 1
};

bool cam_dev_init(void) {
    esp_err_t err = esp_camera_init(&camera_config);
    if (err != ESP_OK) {
        Serial.print("Camera Init Failed");
        return false;
    }
    Serial.print("Camera Init Success");

    // Disable automatic white balance
    sensor_t *s = esp_camera_sensor_get();
    if (s != NULL) {
        s->set_whitebal(s, 0); // 0 to disable, 1 to enable
        // You can also adjust other parameters like AWB gain or white balance mode if needed
        // s->set_awb_gain(s, 0); // Disable AWB gain
        // s->set_wb_mode(s, 0); // 0: Auto, 1: Sunny, 2: Cloudy, 3: Office, 4: Home
    }
    Serial.print("Disable white balance");
    return true;
}

int cam_dev_snapshot(uint8_t *out_buf) {
    int buf_sz = 0;
    camera_fb_t * pic = esp_camera_fb_get();
    buf_sz = pic->len;
    memcpy(out_buf, pic->buf, buf_sz);
    // for(int i = 0; i < buf_sz; i++) {
    //     out_buf[i] = pic->buf[i];
    // }
    esp_camera_fb_return(pic);

    return buf_sz;
}