typedef void (*gui_screen_func)(bool refresh);

gui_screen_func gui_screen_get();
void            gui_screen_set(gui_screen_func new_screen);
void            gui_screen_set_refresh();

void gui_screen_update(bool refresh);
void gui_screen_none(bool refresh);

