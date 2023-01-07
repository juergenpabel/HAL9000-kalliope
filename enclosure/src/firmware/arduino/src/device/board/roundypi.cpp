#ifdef ARDUINO_ROUNDYPI

#include <Arduino.h>
#include <TimeLib.h>

#include "device/board/roundypi.h"
#include "globals.h"


Board::Board()
      :AbstractBoard("roundypi") {
}


void Board::start(bool& host_booting) {
	AbstractBoard::start(host_booting);
	if(TFT_BL >= 0) {
		pinMode(TFT_BL, OUTPUT);
		this->displayOff();
	}
}


bool Board::configure(const JsonVariant& configuration) {
	return g_device_microcontroller.configure(configuration);
}


void Board::reset(bool host_rebooting) {
	AbstractBoard::reset(host_rebooting);
}


void Board::halt() {
	AbstractBoard::halt();
}


void Board::displayOn() {
	if(TFT_BL >= 0) {
		digitalWrite(TFT_BL, HIGH);
	}
}


void Board::displayOff() {
	if(TFT_BL >= 0) {
		digitalWrite(TFT_BL, LOW);
	}
}


void Board::webserial_execute(const etl::string<GLOBAL_KEY_SIZE>& command, const JsonVariant& data) {
}

#endif

