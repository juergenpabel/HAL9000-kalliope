#include "globals.h"

#include <TimeLib.h>
#include "screen.h"

uint32_t        g_splash_timeout = 0;
screen_update_func g_previous_screen = NULL;


void screen_update_splash(bool refresh) {
	if(g_splash_timeout > 0 && now() > g_splash_timeout) {
		g_webserial.send("RoundyPI", "splash timed out, reactivating previous screen");
		screen_update(g_previous_screen, true);
		g_previous_screen = NULL;
	}
}

