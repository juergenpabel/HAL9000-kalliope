#include <stddef.h>
#include <stdint.h>
#include "defines.h"


typedef struct sequence sequence_t;
typedef struct sequence {
	char        name[32];
	uint32_t    timeout;
	sequence_t* next;
} sequence_t;


typedef struct {
	uint16_t size;
	uint8_t  data[5120-2];
} png_t;

