#include "Challenge_Tea.hpp"
#include "flags.h"
#include "main.h"
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

/*
  Pin Map:
  - PB6: SPI2_MISO
  - PB7: SPI2_MOSI
  - PB8: SPI2_SCK
  - PB9: CS
*/

static constexpr int BLOCK_SIZE = 8;

static void encipher(uint32_t v[2], uint32_t const key[4]) {
  unsigned int i;
  uint32_t v0 = v[0], v1 = v[1], sum = 0, delta = 0x9E3779B9;
  for (i = 0; i < 32; i++) {
    v0 += (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]);
    sum += delta;
    v1 += (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum >> 11) & 3]);
  }
  v[0] = v0;
  v[1] = v1;
}

extern SPI_HandleTypeDef hspi2;

bool challenge_tea_run(char *ret) {
  HAL_StatusTypeDef status;
  HAL_GPIO_WritePin(FLASH_SS_GPIO_Port, FLASH_SS_Pin, GPIO_PIN_RESET);

  uint8_t tx_buffer[] = {0x48, 0, 16, 0, 0};

  status =
      HAL_SPI_Transmit(&hspi2, tx_buffer, sizeof(tx_buffer), HAL_MAX_DELAY);
  if (status != HAL_OK) {
    strcat(ret, "internal comms error (1)\r\n");
    return false;
  }

  uint8_t d[16] = {0};

  status = HAL_SPI_Receive(&hspi2, d, sizeof(d), HAL_MAX_DELAY);
  if (status != HAL_OK) {
    strcat(ret, "internal comms error (2)\r\n");
    return false;
  }

  HAL_GPIO_WritePin(FLASH_SS_GPIO_Port, FLASH_SS_Pin, GPIO_PIN_SET);

  uint32_t tea_leaves[4] = {
      (uint32_t)(d[0] << 24) | (d[1] << 16) | (d[2] << 8) | d[3],
      (uint32_t)(d[4] << 24) | (d[5] << 16) | (d[6] << 8) | d[7],
      (uint32_t)(d[8] << 24) | (d[9] << 16) | (d[10] << 8) | d[11],
      (uint32_t)(d[12] << 24) | (d[13] << 16) | (d[14] << 8) | d[15]};

  char flag[] = FLAG_CHALLENGE_TEA;

  static_assert(sizeof(flag) % BLOCK_SIZE == 1,
                "flag must be multiple of BLOCK_SIZE");

  size_t len_flag = strlen(flag);
  for (size_t i = 0; i < len_flag; i += BLOCK_SIZE) {
    encipher((uint32_t *)&flag[i], tea_leaves);
  }

  strcat(ret, "You swirl the teapot before pouring out...\r\n\r\n");

  char tmp[8];
  for (unsigned int i = 0; i < sizeof(flag) - 1; i++) {
    snprintf(tmp, sizeof(tmp), "%02x", flag[i]);
    strcat(ret, tmp);
  }

  strcat(ret, "\r\n");

  return true;
}
