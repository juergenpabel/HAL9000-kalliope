include <hal9000.scad>

conf_rfid = true;
conf_rotary = true;
conf_button = false;
conf_motion = false;

translate([+00.0,+00.0,+00.0]) rotate([+00,+00,+00]) hal9000_enclosure();
translate([+47.5,+18.5,235.0]) rotate([180,+00,+00]) hal9000_enclosure_panel();
translate([+47.5,+30.0,+97.5]) rotate([+90,+00,+00]) hal9000_component_display_frame_bottom();
translate([+47.5,+05.5,+97.5]) rotate([-90,+00,+00]) hal9000_component_display_frame_top();
translate([+47.5,+13.5,+97.5]) rotate([-90,+00,+00]) hal9000_component_display_cover();
translate([+47.5,+00.5,+97.5]) rotate([-90,+00,+00]) hal9000_component_display_ring();
