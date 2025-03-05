#include "Challenge_Perms.hpp"
#include "flags.h"
#include "main.h"
#include <cstdint>
#include <cstring>

extern I2C_HandleTypeDef hi2c2;

constexpr int I2C_TIMEOUT = 100;
constexpr uint8_t EEPROM_ADDRESS = 0xA0;

typedef struct __attribute__((packed)) {
  uint16_t user_id;
  uint8_t permissions;
  uint8_t checksum;
} user_data_t;

bool challenge_perms_run(char *ret) {
  uint8_t data_tx[1] = {0};

  if (HAL_I2C_Master_Transmit(&hi2c2, EEPROM_ADDRESS, data_tx, 1,
                              I2C_TIMEOUT) != HAL_OK) {
    strcat(ret, "BEEP: internal error: write failed\r\n");
    return false;
  }

  user_data_t data = {0};

  if (HAL_I2C_Master_Receive(&hi2c2, EEPROM_ADDRESS | 0x01, (uint8_t *)&data,
                             sizeof(data), I2C_TIMEOUT) != HAL_OK) {
    strcat(ret, "BEEP: internal error: read failed\r\n");
    return false;
  }

  uint8_t *p = (uint8_t *)&data;
  uint8_t expected_checksum = 0xB3;

  for (unsigned int i = 0; i < sizeof(user_data_t) - 1; i++) {
    expected_checksum ^= (*p++);
  }

  if (data.checksum != expected_checksum) {
    strcat(ret, "How puzzling! We appear to have some data corruption...\r\n");
    return false;
  }

  if (data.user_id != 42) {
    strcat(ret, "User is...not the answer to life.\r\n");
    return false;
  }

  if (data.permissions < 200) {
    strcat(ret, "You do not have enough authorization. This incident will be "
                "reported.\r\n");
    return false;
  }

  strcat(ret, "congrats: " FLAG_CHALLENGE_PERMS);
  strcat(ret, "\r\n");
  return true;
}
