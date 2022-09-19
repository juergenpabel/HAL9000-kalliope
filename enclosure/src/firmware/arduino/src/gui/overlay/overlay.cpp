#include "gui/screen/screen.h"
#include "gui/overlay/overlay.h"
#include "globals.h"

static gui_overlay_func  g_gui_overlay = gui_overlay_none;


gui_overlay_func gui_overlay_get() {
	return g_gui_overlay;
}


gui_overlay_func gui_overlay_set(gui_overlay_func new_overlay) {
	gui_overlay_func previous_overlay = nullptr;
	if(new_overlay != nullptr) {
		if(new_overlay != g_gui_overlay) {
			previous_overlay = g_gui_overlay;
			g_gui_overlay = new_overlay;
			gui_screen_set_refresh();
		}
	}
	return previous_overlay;
}


void gui_overlay_update(bool refresh) {
	if(refresh) {
		g_device_tft_overlay.fillSprite(TFT_BLACK);
	}
	g_gui_overlay(refresh);
}


void gui_overlay_none(bool refresh) {
}

