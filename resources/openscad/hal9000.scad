/* this file is used by other files in this directory, by itself it does not render anything */


$fn=120;
conf_rfid = false;
conf_rotary = false;
conf_button = false;


module hal9000_enclosure() {
	color([0.625,0.625,0.625]) render()
    difference() {
		translate([+00.0,+00.0,+00.0]) cube([+95.0,+35.0,235.0]);
		translate([+05.0,+05.0,+05.0]) cube([+85.0,+25.0,225.0]);
		union(/*acryl-faceplate*/) {
			translate([+05.0,+00.0,+50.0]) cube([+85.0,+01.5,180.0]);
			translate([+02.0,+01.5,+47.0]) cube([+91.0,+03.5,186.0]);
			translate([+05.0,+05.0,+45.0]) cube([+85.0,+01.5,185.0]);
		}
		union(/*control panel*/) {
            translate([+47.5,+18.5,233.5]) cube([+83.0,+25.5,+03.0], center=true);
            translate([+47.5,+18.5,232.5]) cube([+80.5,+23.0,+05.0], center=true);

            union(/*enclosure panel screw holes*/) {
                translate([+82.0,+35.0,225.0]) rotate([+90,+90,+00]) cylinder(d=+06.0,h=+02.0);
                translate([+82.0,+35.0,225.0]) rotate([+90,+90,+00]) cylinder(d=+03.0,h=+05.0);
                translate([+13.0,+35.0,225.0]) rotate([+90,+90,+00]) cylinder(d=+06.0,h=+02.0);
                translate([+13.0,+35.0,225.0]) rotate([+90,+90,+00]) cylinder(d=+03.0,h=+05.0);
            }
        
        }            
        union(/*fixation & screw holes for display frame*/) {
            translate([+47.5,+27.5,+117.5]) cube([+90.0,+05.0,+05.0], center=true);
            translate([+01.0,+17.5,+112.5]) rotate([+00,+90,+00]) cylinder(d=+06.0,h=+02.0, center=true);
            translate([+02.5,+17.5,+112.5]) rotate([+00,+90,+00]) cylinder(d=+03.0,h=+05.0, center=true);

            translate([+94.0,+17.5,+112.5]) rotate([+00,+90,+00]) cylinder(d=+06.0,h=+02.0, center=true);
            translate([+92.5,+17.5,+112.5]) rotate([+00,+90,+00]) cylinder(d=+03.0,h=+05.0, center=true);
            
            translate([+01.0,+17.5,+122.5]) rotate([+00,+90,+00]) cylinder(d=+06.0,h=+02.0, center=true);
            translate([+02.5,+17.5,+122.5]) rotate([+00,+90,+00]) cylinder(d=+03.0,h=+05.0, center=true);

            translate([+94.0,+17.5,+122.5]) rotate([+00,+90,+00]) cylinder(d=+06.0,h=+02.0, center=true);
            translate([+92.5,+17.5,+122.5]) rotate([+00,+90,+00]) cylinder(d=+03.0,h=+05.0, center=true);
        }

        union(/*raspberry pi zero*/) {
            union(/*inlet:power cable*/) {
                translate([+47.5,+32.5,150.0]) rotate([+90,+90,+00]) scale([+00.8,+00.5,+01.0]) cylinder(r=+10.0,h=+05.0, center=true);
                translate([+47.5,+34.0,117.5]) cube([+10.0,+02.0,235.0], center=true);
            }

			//translate([93/2,30,195-58/2]) cube([30.0,5.0,65.0], center=true);
            union(/*screws:pi zero*/) {
                translate([+59.0,+35.0,137.0]) rotate([+90,+90,+00]) cylinder(d=+06.0,h=+02.0);
                translate([+59.0,+35.0,137.0]) rotate([+90,+90,+00]) cylinder(d=+03.0,h=+05.0);
                translate([+36.0,+35.0,137.0]) rotate([+90,+90,+00]) cylinder(d=+06.0,h=+02.0);
                translate([+36.0,+35.0,137.0]) rotate([+90,+90,+00]) cylinder(d=+03.0,h=+05.0);
                
                translate([+59.0,+35.0,195.0]) rotate([+90,+90,+00]) cylinder(d=+06.0,h=+02.0);
                translate([+59.0,+35.0,195.0]) rotate([+90,+90,+00]) cylinder(d=+03.0,h=+05.0);
                translate([+36.0,+35.0,195.0]) rotate([+90,+90,+00]) cylinder(d=+06.0,h=+02.0);
                translate([+36.0,+35.0,195.0]) rotate([+90,+90,+00]) cylinder(d=+03.0,h=+05.0);

            }
			//translate([154/2,30,170-33/2]) cube([23.0,5.0,38.0], center=true);
            union(/*screws:ft232h*/) {
                translate([+86.0,+35.0,137.0]) rotate([+90,+90,+00]) cylinder(d=+06.0,h=+02.0);
                translate([+86.0,+35.0,137.0]) rotate([+90,+90,+00]) cylinder(d=+03.0,h=+05.0);
                translate([+68.0,+35.0,137.0]) rotate([+90,+90,+00]) cylinder(d=+06.0,h=+02.0);
                translate([+68.0,+35.0,137.0]) rotate([+90,+90,+00]) cylinder(d=+03.0,h=+05.0);
                
                translate([+86.0,+35.0,170.0]) rotate([+90,+90,+00]) cylinder(d=+06.0,h=+02.0);
                translate([+86.0,+35.0,170.0]) rotate([+90,+90,+00]) cylinder(d=+03.0,h=+05.0);
                translate([+68.0,+35.0,170.0]) rotate([+90,+90,+00]) cylinder(d=+06.0,h=+02.0);
                translate([+68.0,+35.0,170.0]) rotate([+90,+90,+00]) cylinder(d=+03.0,h=+05.0);
            }
            union(/*screws:mcp23817*/) {
                translate([+21.7,+34.0,137.0]) rotate([+90,+90,+00]) cylinder(d=+06.0,h=+02.0, center=true);
                translate([+21.7,+32.5,137.0]) rotate([+90,+90,+00]) cylinder(d=+03.0,h=+05.0, center=true);
                translate([+09.0,+34.0,137.0]) rotate([+90,+90,+00]) cylinder(d=+06.0,h=+02.0, center=true);
                translate([+09.0,+32.5,137.0]) rotate([+90,+90,+00]) cylinder(d=+03.0,h=+05.0, center=true);
             
                translate([+21.7,+34.0,175.0]) rotate([+90,+90,+00]) cylinder(d=+06.0,h=+02.0, center=true);
                translate([+21.7,+32.5,175.0]) rotate([+90,+90,+00]) cylinder(d=+03.0,h=+05.0, center=true);
                translate([+09.0,+34.0,175.0]) rotate([+90,+90,+00]) cylinder(d=+06.0,h=+02.0, center=true);
                translate([+09.0,+32.5,175.0]) rotate([+90,+90,+00]) cylinder(d=+03.0,h=+05.0, center=true);
            }

        }
		union(/*screws:respeaker 2-mic*/) {
			translate([+47.5-58/2,+35.0,+40.0]) rotate([+90,+90,+00]) cylinder(d=+06.0,h=+02.0);
			translate([+47.5-58/2,+35.0,+40.0]) rotate([+90,+90,+00]) cylinder(d=+03.0,h=+05.0);
			translate([+47.5+58/2,+35.0,+40.0]) rotate([+90,+90,+00]) cylinder(d=+06.0,h=+02.0);
			translate([+47.5+58/2,+35.0,+40.0]) rotate([+90,+90,+00]) cylinder(d=+03.0,h=+05.0);

		}
		union(/*grill:front(microphone)*/) {
            translate([+05.0,+00.0,+05.0]) cube([+85.0,+02.5,+40.0]);
            translate([+02.0,+02.5,+02.5]) cube([+91.0,+01.5,+50.0]);
            translate([+05.0,+04.0,+05.0]) cube([+85.0,+01.0,+40.0]);
		}
		union(/*grill:bottom(speaker)*/) {
			for( x=[1:8] ) {
				for( y=[1:4] ) {
					if( !(x==1&&y==1) && !(x==1&&y==4) && !(x==8&&y==1) && !(x==8&&y==4) ) {
						translate([+25.0+(x*5),+03.5+(y*5),+02.5]) cube([+04.0,+04.0,+05.0], center=true);
					}
				}
			}
            //inlet:visaton K20.40 speaker
			translate([+47.5,+16.0,+04.0]) cube([+41.0,+21.0,+02.0], center=true);
            //screws:visaton K20.40 speaker
			translate([+29.5,+08.0,+00.5]) cylinder(d=+04.5,h=+01.0, center=true);
			translate([+29.5,+08.0,+02.5]) cylinder(d=+02.5,h=+05.0, center=true);
			translate([+29.5,+24.0,+00.5]) cylinder(d=+04.5,h=+01.0, center=true);
			translate([+29.5,+24.0,+02.5]) cylinder(d=+02.5,h=+05.0, center=true);
			translate([+65.5,+08.0,+00.5]) cylinder(d=+04.5,h=+01.0, center=true);
			translate([+65.5,+08.0,+02.5]) cylinder(d=+02.5,h=+05.0, center=true);
			translate([+65.5,+24.0,+00.5]) cylinder(d=+04.5,h=+01.0, center=true);
			translate([+65.5,+24.0,+02.5]) cylinder(d=+02.5,h=+05.0, center=true);
		}
	}
}


module hal9000_enclosure_bottom() {
	color([0.625,0.625,0.625]) render()
	rotate([+0.00,+0.00,+0.00]) translate([+0.00,+0.00,+0.00]) {
        intersection() {
            translate([+0.00,+0.00,+0.00]) hal9000_enclosure();
            translate([+0.00,+0.00,+0.00]) cube([+95.0,+35.0,117.5]);
        }
	}
}


module hal9000_enclosure_top() {
	color([0.625,0.625,0.625]) render()
	rotate([180.0,+00.0,+00.0]) translate([+0.00,+0.00,-235.0]) {
        intersection() {
            translate([+0.00,+0.00,+0.00]) hal9000_enclosure();
            translate([+0.00,+0.00,117.5]) cube([+95.0,+35.0,117.5]);
        }
	}
}


module hal9000_enclosure_panel() {
    color([0.625,0.625,0.625]) render()
    difference() {
        union() {
            translate([+00.0,+00.0,+01.5]) cube([+82.5,+25.0,+03.0], center=true);
            translate([+00.0,+00.0,+02.5]) cube([+80.0,+22.5,+05.0], center=true);
            translate([+00.0,-09.0,+07.5]) cube([+80.0,+04.5,+15.0], center=true);
            if (conf_rfid == true) union() {
                translate([+00.0,-09.0,+17.5]) cube([+59.0,+04.5,+35.0], center=true);
            }
            if (conf_rotary == true) union() {
                translate([-31.0,+03.5,+07.5]) cube([+18.0,+15.5,+15.0], center=true);
                translate([+31.0,+03.5,+07.5]) cube([+18.0,+15.5,+15.0], center=true);
            }
        }
        translate([+34.5,-09.0,+10.0]) rotate([-90,+90,+00]) cylinder(d1=+03.0,d2=+02.5,h=+04.5, center=true);
        translate([-34.5,-09.0,+10.0]) rotate([-90,+90,+00]) cylinder(d1=+03.0,d2=+02.5,h=+04.5, center=true);

        if (conf_rfid == true) union() {
            translate([+00.0,-09.0,+17.0]) cube([+56.0,+01.5,+34.0], center=true);
        }
		if (conf_button == true) union() {
			translate([+00.0,+03.0,+00.8]) cube([+40.5,+15.5,+01.6], center=true);
			translate([-02.5,+03.0,+02.3]) cube([+31.0,+13.0,+01.4], center=true);
			translate([-02.5,+03.0,+04.0]) cube([+31.0,+09.0,+02.0], center=true);
		}
        if (conf_rotary == true) union() {
                translate([-31.0,+03.5,+14.0]) cube([+16.0,+13.5,+2.0], center=true);
                translate([-30.5,+03.5,+05.0]) cylinder(d=+13.5, h=+10.0, center=true);
                translate([-30.5,+03.5,+06.5]) cylinder(d=+07.5, h=+13.0, center=true);
                translate([-24.0,+03.5,+12.0]) cube([+02.0,+02.5,+02.0], center=true);

                translate([+31.0,+03.5,+14.0]) cube([+16.0,+13.5,+2.0], center=true);
                translate([+30.5,+03.5,+05.0]) cylinder(d=+13.5, h=+10.0, center=true);
                translate([+30.5,+03.5,+06.5]) cylinder(d=+07.5, h=+13.0, center=true);
                translate([+24.0,+03.5,+12.0]) cube([+02.0,+02.5,+02.0], center=true);
        }
    }
}


module hal9000_component_display_frame_top() {
    color([0,0,0]) render()
    difference() {
        union() {
            translate([+00.0,+00.0,+05.0]) cube([+74.5,+69.5,+10.0], center=true);
            translate([+00.0,+00.0,+05.0]) cube([+84.5,+59.5,+10.0], center=true);
        }
        difference(/*fisheye inlet*/) {
            translate([+00.0,+00.0,+01.0]) cylinder(d=+55.5,h=+02.0, center=true);
            translate([+00.0,+00.0,+01.0]) cylinder(d=+41.3,h=+02.0, center=true);
        }

        union(/*waveshare 1.8" tft inlet*/) { //TODO: 6.0mm oder 5.5mm??
            translate([+00.0,+00.0,+01.5]) cylinder(d=+33.0,h=+03.0, center=true);
            hull() {
                translate([+00.0,+00.0,+05.5]) cylinder(d=+40.0,h=+06.0, center=true);
                translate([+00.0,+17.5,+05.5]) cube([+20.0,+10.0,+06.0], center=true);
            }
            translate([+00.0,-25.0,+08.0]) cube([+22.5,+20.0,+04.0], center=true);
        }
        union(/*frame cover inlet*/) {
            hull() {
                translate([+00.0,+00.0,+09.0]) cylinder(d=+52.0,h=+02.0, center=true);
                translate([+00.0,+20.0,+09.0]) cube([+26.0,+17.0,+02.0], center=true);
            }
        }
        union(/*screw holes*/) {
            translate([-13.5,-18.0,+06.0]) cylinder(d=+02.0,h=+05.0, center=true);
            translate([+13.5,-18.0,+06.0]) cylinder(d=+02.0,h=+05.0, center=true);
            translate([-09.0,+25.0,+06.0]) cylinder(d=+02.0,h=+05.0, center=true);
            translate([+09.0,+25.0,+06.0]) cylinder(d=+02.0,h=+05.0, center=true);
        }
    }
}


module hal9000_component_display_frame_bottom() {
    color([0,0,0]) render()
    difference() {
        union() {
            translate([+00.0,+00.0,+12.25]) cube([+84.5,+70.0,+24.5], center=true);
            translate([+00.0,+20.0,+02.25]) cube([+89.5,+04.5,+04.5], center=true);
        }
        translate([+00.0,+00.0,+13.0]) cube([+75.0,+70.0,+24.0], center=true);
        translate([+00.0,+00.0,+19.5]) cube([+84.5,+60.0,+10.0], center=true);
        union(/*screw holes*/) {
            translate([+42.5,+15.0,+12.5]) rotate([+00,-90,+00]) cylinder(d1=+03.0,d2=+02.5,h=+05.5);
            translate([+42.5,+25.0,+12.5]) rotate([+00,-90,+00]) cylinder(d1=+03.0,d2=+02.5,h=+05.5);
            translate([-42.5,+15.0,+12.5]) rotate([+00,+90,+00]) cylinder(d1=+03.0,d2=+02.5,h=+05.5);
            translate([-42.5,+25.0,+12.5]) rotate([+00,+90,+00]) cylinder(d1=+03.0,d2=+02.5,h=+05.5);
        }        
    }
}


module hal9000_component_display_cover(){
    color([0,0,0]) render()
    union() {
        difference() {
            hull() {
                translate([+00.0,+00.0,+01.0]) cylinder(d=+50.0,h=+02.0, center=true);
                translate([+00.0,+20.0,+01.0]) cube([+25.0,+15.0,+02.0], center=true);
            }
            translate([+00.0,-15.0,+01.0]) cube([+22.5,+25.0,+02.0], center=true);
            union(/*frame screw holes*/) {
                translate([-13.5,-18.0,+01.0]) cylinder(d=+02.0,h=+02.0, center=true);
                translate([+13.5,-18.0,+01.0]) cylinder(d=+02.0,h=+02.0, center=true);
                translate([-09.0,+25.0,+01.0]) cylinder(d=+02.0,h=+02.0, center=true);
                translate([+09.0,+25.0,+01.0]) cylinder(d=+02.0,h=+02.0, center=true);
            }
            union(/*waveshare 1.8" tft screw holes*/) {
                translate([-13.2,-09.3,+01.0]) cylinder(d=+02.0,h=+02.0, center=true);
                translate([+13.2,-09.3,+01.0]) cylinder(d=+02.0,h=+02.0, center=true);
                translate([-13.2,+09.3,+01.0]) cylinder(d=+02.0,h=+02.0, center=true);
                translate([+13.2,+09.3,+01.0]) cylinder(d=+02.0,h=+02.0, center=true);
            }
        }

        difference(/*mount for PCF8591 for (analog) buttons*/) {
            union() {
                translate([-09.0,+04.5,+02.5]) cylinder(d=+04.0,h=+01.0, center=true);
                translate([+09.0,+04.5,+02.5]) cylinder(d=+04.0,h=+01.0, center=true);
                translate([-09.0,+25.0,+02.5]) cylinder(d=+04.0,h=+01.0, center=true);
                translate([+09.0,+25.0,+02.5]) cylinder(d=+04.0,h=+01.0, center=true);

                translate([-09.0,+04.5,+03.5]) cylinder(d=+02.0,h=+01.0, center=true);
                translate([+09.0,+04.5,+03.5]) cylinder(d=+02.0,h=+01.0, center=true);
            }
            union() {
                translate([-09.0,+25.0,+02.5]) cylinder(d=+02.0,h=+01.0, center=true);
                translate([+09.0,+25.0,+02.5]) cylinder(d=+02.0,h=+01.0, center=true);

            }
        }
        difference(/*screw hole raiser*/) {
            union() { 
                translate([-13.5,-18.0,+02.5]) cylinder(d=+04.0,h=+01.0, center=true);
                translate([+13.5,-18.0,+02.5]) cylinder(d=+04.0,h=+01.0, center=true);
            }
            union() { 
                translate([-13.5,-18.0,+02.5]) cylinder(d=+02.0,h=+01.0, center=true);
                translate([+13.5,-18.0,+02.5]) cylinder(d=+02.0,h=+01.0, center=true);
            }
        }

    }
}


module hal9000_component_display_ring() {
    color([0.625,0.625,0.625]) render()
    union() {
        difference() {
            translate([+00.0,+00.0,+01.5]) cylinder(d=+49.5,h=+03.0, center=true);
            translate([+00.0,+00.0,+01.5]) cylinder(d=+46.5,h=+03.0, center=true);
        }
        difference() {
            translate([+00.0,+00.0,+00.5]) cylinder(d=+52.5,h=+01.0, center=true);
            translate([+00.0,+00.0,+00.5]) cylinder(d=+46.5,h=+01.0, center=true);
        }
    }
}


module hal9000_component_rfid_cover() {
    if (conf_rfid == true) color([1,1,1]) render() difference(/*card holder*/) {
        union() {
            translate([+00.0,+15.0,+01.0]) cube([+59.0,+30.0,+02.0], center=true);
            translate([+00.0,+05.0,+01.0]) cube([+80.0,+10.0,+02.0], center=true);
        }
        translate([-34.5,+05.0,+01.0]) cylinder(d=3.0,h=2.0, center=true);
        translate([+34.5,+05.0,+01.0]) cylinder(d=3.0,h=2.0, center=true);
        difference() {
            translate([+00.0,+11.5,+01.0]) cube([+31.0,+21.0,+02.0], center=true);
            
            translate([+00.0,+21.5,+00.4]) cube([+31.0,+01.0,+00.8], center=true);
            translate([+00.0,+01.5,+00.4]) cube([+31.0,+01.0,+00.8], center=true);
        }
    }
}


module hal9000_material_acryl() {
    color([0,0,0,0.5]) render() difference() {
        translate([+00.0,+00.0,+01.5]) cube([+90.0,+185.0,+03.0], center=true);
        translate([+00.0,+42.5,+01.5]) cylinder(d=+50.0,h=+03.0, center=true);
    }
}


module hal9000_material_fisheye() {
    color([0.3,0.3,0.3,0.5]) render() scale([1,1,0.6]) intersection() {
        translate([+00.0,+00.0,+00.0]) sphere(d=+50.0);
        translate([+00.0,+00.0,+12.5]) cube([+50.0,+50.0,+25.0], center=true);
    }
}


module hal9000_material_wiremesh() {
    color([1,1,1,0.5]) render() difference() {
        translate([+00.0,+00.0,+00.5]) cube([+90.0,+45.0,+01.0], center=true);
    }
}

