#include <TFT_eSPI.h>
#include <LittleFS.h>
#include <pngle.h>
#include <SPI.h>
#include <SdFat.h>
#include <SimpleWebSerial.h>

#define SPI_SPEED SD_SCK_MHZ(32)

#define SCK 18
#define SS 17
#define SDCARD_SS_PIN 17
#define SD_CS_PIN 17
#define MISO 16
#define MOSI 19

#define FRAMES_PNG_MAX 64
#define SEQUENCES_MAX 8

static TFT_eSPI        g_tft = TFT_eSPI();
static SimpleWebSerial g_websocket;


typedef struct sequence sequence_t;
typedef struct sequence {
	char        type;
	char        name[256];
	uint32_t    timeout;
	sequence_t* next;
} sequence_t;


typedef struct {
	char     type;
	uint16_t size;
	uint8_t* data;
} png_t;


static sequence_t* g_sequence = NULL;
static sequence_t  g_sequences_queue[SEQUENCES_MAX] = {0};
static png_t       g_frames_png[FRAMES_PNG_MAX] = {0};
static uint16_t    g_image_565[240][240] = {0};


void pngle_on_draw(pngle_t *pngle, uint32_t x, uint32_t y, uint32_t w, uint32_t h, uint8_t rgba[4]) {
	uint16_t pixel565 = 0;
	uint8_t* frame_png = NULL;

	pixel565 = g_tft.color565(rgba[0], rgba[1], rgba[2]);

	g_image_565[  0 + y][  0 + x] = pixel565;
	g_image_565[239 - x][  0 + y] = pixel565;
	g_image_565[239 - y][239 - x] = pixel565;
	g_image_565[  0 + x][239 - y] = pixel565;
}


void pngle_draw(uint8_t* png, uint16_t png_size) {
	pngle_t* pngle = NULL;

	pngle = pngle_new();
	if(pngle == NULL) {
		Serial.printf("pngle_new() failed\n");
		return;
	}
	pngle_set_draw_callback(pngle, pngle_on_draw);
	if(pngle_feed(pngle, png, png_size) != png_size) {
		Serial.printf("pngle_feed() failed\n");
		pngle_destroy(pngle);
		return;
	}
	pngle_destroy(pngle);
	g_tft.pushImage(0, 0, 240, 240, (uint16_t*)g_image_565);
}


void draw_quarter_frame(uint8_t frame) {
	uint8_t* png_data = NULL;
	uint16_t png_size = 0;
	//uint32_t time_start = 0;

	//time_start = millis();
	memset(g_image_565, '\0', sizeof(g_image_565));
	if(frame >= FRAMES_PNG_MAX) {
		Serial.printf("invalid frame number %d", frame);
		return;
	}
	png_data = g_frames_png[frame].data;
	png_size = g_frames_png[frame].size;
	if(png_data==NULL || png_size==0) {
		return;
	}
	pngle_draw(png_data, png_size);
	//Serial.printf("Frame generated and drawn in %d ms\n", millis() - time_start);
}


void draw_frames() {
	for(int i=0; i<FRAMES_PNG_MAX; i++) {
		if(g_frames_png[i].type != '\0') {
			switch(g_frames_png[i].type) {
				case 'F':
					//TODO:draw_full_frame(i);
					break;
				case 'Q':
					draw_quarter_frame(i);
					break;
				default:
					Serial.printf("invalid frame type '%c'\n", g_frames_png[i].type);
			};
		}
	}
}


void load_quarter_frames(const char* path) {
	char     filename[256] = {0};
	File     file = {0};
	uint32_t time_start = 0;

	time_start = millis();
	for(int i=0; i<FRAMES_PNG_MAX; i++) {
		if(g_frames_png[i].data != NULL) {
			free(g_frames_png[i].data);
			g_frames_png[i].data = NULL;
			g_frames_png[i].size = 0;
			g_frames_png[i].type = '\0';
		}
	}
	for(int i=0; i<FRAMES_PNG_MAX; i++) {
		snprintf(filename, sizeof(filename)-1, "%s/%.2d.png", path, i);
		file = LittleFS.open(filename, "r");
		if(file) {
			g_frames_png[i].data = (uint8_t*)malloc(file.size());
			if(g_frames_png[i].data == NULL) {
				Serial.printf("malloc() failed for png '%s' with size=%d", filename, file.size());
				file.close();
				return;
			}
			g_frames_png[i].size = file.size();
			g_frames_png[i].type = 'Q';
			file.read(g_frames_png[i].data, g_frames_png[i].size);
			file.close();
		}
	}
	Serial.printf("Quarter frames loaded from littlefs:'%s' in %d ms\n", path, millis() - time_start);
}


void load_hal_frames(const char* name) {
	char  path[256] = {0};

	snprintf(path, sizeof(path)-1, "/images/eye/%s", name);
	load_quarter_frames(path);
}


void on_hal_sequence_timeout(JSONVar parameter) {
	if(strncmp("set", (const char*)parameter["action"], 4) == 0) {
		g_sequence->timeout = millis() + (long)parameter["timeout"] * 1000;
	}
	if(strncmp("add", (const char*)parameter["action"], 4) == 0) {
		g_sequence->timeout += (long)parameter["timeout"] * 1000;
	}
}


void on_hal_sequences(JSONVar parameter) {
	uint8_t     target_offset = 0;
	sequence_t* target_sequence = NULL;

	//if(strncmp("set", (const char*)parameter["action"], 4) == 0) {
	//}
	if(1) { //if(strncmp("add", (const char*)parameter["action"], 4) == 0) {
		if(parameter.hasOwnProperty("sequence")) {
			parameter = parameter["sequence"];
		}
		while(target_offset<SEQUENCES_MAX && g_sequences_queue[target_offset].type!='\0') {
			target_offset++;
		}
		if(target_offset==SEQUENCES_MAX) {
			Serial.printf("Sequences queue already full\n");
			return;
		}
		Serial.printf("Adding sequence '%s' to queue at pos=%d with timeout=%d and next=%d\n",(const char*)parameter["name"], target_offset, (long)parameter["timeout"], parameter.hasOwnProperty("next"));

		target_sequence = g_sequence;
		while(target_sequence->next != NULL) {
			target_sequence = target_sequence->next;
		}
		target_sequence->next = &g_sequences_queue[target_offset];
		target_sequence = target_sequence->next;
		target_sequence->type = 'Q';
		strncpy(target_sequence->name, parameter["name"], sizeof(target_sequence->name)-1);
		target_sequence->timeout = 1000 * (long)parameter["timeout"];
		target_sequence->next = NULL;
	}

	if(parameter.hasOwnProperty("next")) {
		on_hal_sequences(parameter["next"]);
	}
}


void on_hal_display_backlight(JSONVar parameter) {
	bool status;

	if(parameter.hasOwnProperty("display")) {
		status = parameter["display"]["status"];
	}
	if(strncmp("set", (const char*)parameter["action"], 4) == 0) {
		//g_tft.setBacklight(status);
		//TODO:log
	}
}


void setup() {
	Serial.begin(115200);
	delay(3000);
	Serial.printf("\nRoundyPI\n");

	g_tft.begin();
	g_tft.setRotation(0);
	g_tft.fillScreen(TFT_BLACK);
	g_tft.setSwapBytes(true);
	Serial.printf("TFT ready\n");

	if(!LittleFS.begin()) {
		Serial.printf("LittleFS error, halting\n");
		while(1) delay(1);
	}
	Serial.printf("LittleFS ready\n");

	g_sequences_queue[0].type = 'Q';
	strncpy(g_sequences_queue[0].name, "init", sizeof(g_sequences_queue[0].name)-1);
	g_sequences_queue[0].timeout = 0;
	g_sequences_queue[0].next = NULL;
	g_sequence = &g_sequences_queue[0];
	Serial.printf("Sequences ready\n");

	g_websocket.on("sequences", on_hal_sequences);
	g_websocket.on("sequence:timeout", on_hal_sequence_timeout);
	g_websocket.on("display:backlight", on_hal_display_backlight);
	Serial.printf("Webserial ready\n");
}


void loop() {
	draw_frames();
	g_websocket.check();
	delay(1);

	sequence_t* last_sequence = g_sequence;
	sequence_t* next_sequence = g_sequence->next;
	if(last_sequence->timeout > 0) {
		if(millis() > last_sequence->timeout) {
			last_sequence->timeout = 0;
		}
	}
	if(last_sequence->timeout == 0) {
		if(next_sequence != NULL) {
			last_sequence->type = '\0';
			last_sequence->name[0] = '\0';
			last_sequence->timeout = 0;
			last_sequence->next = NULL;
			if(next_sequence->type == 'Q') {
				load_hal_frames(next_sequence->name);
			}
			g_sequence = next_sequence;
//			if(g_sequence->timeout > 0) {
				g_sequence->timeout += millis();
//			}
		}
	}
}
