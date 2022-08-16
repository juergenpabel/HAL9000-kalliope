#include <SimpleWebSerial.h>
#include "util/jpeg.h"
#include "globals.h"


static int render2buffer(JPEGDRAW *pDraw) {
	uint16_t*  image565_data;

	image565_data = (uint16_t*)pDraw->pUser;
	memcpy(image565_data, pDraw->pPixels, sizeof(uint16_t)*pDraw->iWidth*pDraw->iHeight);
	return true;
}


void util_jpeg_decode565_ram(uint8_t* jpeg_data, uint32_t jpeg_size, uint16_t* image565_data, uint32_t image565_size, JPEG_DRAW_CALLBACK* image565_func) {

	if(g_util_jpeg.openRAM(jpeg_data, jpeg_size, image565_func) != JPEG_SUCCESS) {
		g_util_webserial.send("syslog", "util_jpeg_decode565_ram() -> g_util_jpeg.open() failed");
		return;
	}
	if(image565_data != NULL && image565_size > 0) {
		if(g_util_jpeg.getWidth()*g_util_jpeg.getHeight() != image565_size) {
			g_util_webserial.send("syslog", "util_jpeg_decode565_ram() -> provided buffer is not the correct size (jpeg:width*height)");
			g_util_jpeg.close();
		}
		if(image565_func == NULL) {
			image565_func = render2buffer;
		}
	}
	if(image565_data == NULL || image565_size == 0) {
		if(image565_func == NULL) {
			g_util_webserial.send("syslog", "util_jpeg_decode565_ram() -> no buffer provided, JPEG_DRAW_CALLBACK must not be NULL");
			g_util_jpeg.close();
			return;
		}
	}
	g_util_jpeg.setUserPointer(image565_data);
	g_util_jpeg.decode(0, 0, 0); //TODO:check
	g_util_jpeg.close();
}


void util_jpeg_decode565_littlefs(const char* filename, uint16_t* image565_data, uint32_t image565_size, JPEG_DRAW_CALLBACK* image565_func) {
	File  file;

	file = LittleFS.open(filename, "r");
	if(file == false) {
		g_util_webserial.send("syslog", "util_jpeg_decode565_littlefs(): file not found");
		g_util_webserial.send("syslog", filename);
		return;
	}
	if(g_util_jpeg.open(file, image565_func) != JPEG_SUCCESS) {
		g_util_webserial.send("syslog", "util_jpeg_decode565_littlefs() -> g_util_jpeg.open() failed");
		g_util_webserial.send("syslog", filename);
		return;
	}
	if(image565_data != NULL && image565_size > 0) {
		if(g_util_jpeg.getWidth()*g_util_jpeg.getHeight() != image565_size) {
			g_util_webserial.send("syslog", "util_jpeg_decode565_littlefs() -> provided buffer is not the correct size (jpeg:width*height)");
			g_util_webserial.send("syslog", filename);
			g_util_jpeg.close();
		}
		if(image565_func == NULL) {
			image565_func = render2buffer;
		}
	}
	if(image565_data == NULL || image565_size == 0) {
		if(image565_func == NULL) {
			g_util_webserial.send("syslog", "util_jpeg_decode565_littlefs() -> no buffer provided, JPEG_DRAW_CALLBACK must not be NULL");
			g_util_webserial.send("syslog", filename);
			g_util_jpeg.close();
			return;
		}
	}
	g_util_jpeg.setUserPointer(image565_data);
	g_util_jpeg.decode(0, 0, 0); //TODO:check
	g_util_jpeg.close();
}
