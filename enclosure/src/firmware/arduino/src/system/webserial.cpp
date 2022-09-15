#include <TimeLib.h>
#include <ArduinoJson.h>
#include <etl/to_string.h>
#include "system/webserial.h"
#include "system/rp2040.h"
#include "system/time.h"
#include "globals.h"


void on_system_runtime(const JsonVariant& data) {
	static StaticJsonDocument<1024> result;

	result.clear();
	if(data.containsKey("list")) {
		for(Runtime::iterator iter=g_system_runtime.begin(); iter!=g_system_runtime.end(); ++iter) {
			result[iter->first.c_str()] = iter->second.c_str();
		}
		g_util_webserial.send("system/runtime#list", result.as<JsonVariant>());
	}
	if(data.containsKey("set")) {
		etl::string<GLOBAL_KEY_SIZE> key;
		etl::string<GLOBAL_VALUE_SIZE> value;

		key = data["set"]["key"].as<const char*>();
		value = data["set"]["value"].as<const char*>();
		if(key.length() > 0 && value.length() > 0) {
			g_system_runtime[key.c_str()] = value.c_str();
			g_util_webserial.send("syslog", "system/runtime#set => OK");
		} else {
			g_util_webserial.send("syslog", "system/runtime#set => ERROR");
		}
	}
}


void on_system_settings(const JsonVariant& data) {
	static StaticJsonDocument<1024> result;

	result.clear();
	if(data.containsKey("list")) {

		for(Settings::iterator iter=g_system_settings.begin(); iter!=g_system_settings.end(); ++iter) {
			result[iter->first.c_str()] = iter->second.c_str();
		}
		g_util_webserial.send("system/settings#list", result);
	}
	if(data.containsKey("get")) {
		etl::string<GLOBAL_KEY_SIZE> key;

		key = data["get"]["key"].as<const char*>();
		if(key.length() > 0) {
			if(g_system_settings.count(key) == 1) {
				result["key"] = key.c_str();
				result["value"] = g_system_settings[key].c_str();
			}
			g_util_webserial.send("system/settings#get", result);
			g_util_webserial.send("syslog", "system/settings#get => OK");
		} else {
			g_util_webserial.send("syslog", "system/settings#get => ERROR");
		}
	}
	if(data.containsKey("set")) {
		etl::string<GLOBAL_KEY_SIZE> key;
		etl::string<GLOBAL_VALUE_SIZE> value;

		key = data["set"]["key"].as<const char*>();
		value = data["set"]["value"].as<const char*>();
		if(key.length() > 0 && value.length() > 0) {
			g_system_settings[key] = value;
			g_util_webserial.send("syslog", "system/settings#set => OK");
		} else {
			g_util_webserial.send("syslog", "system/settings#set => ERROR");
		}
	}
	if(data.containsKey("load")) {
		if(g_system_settings.load() == true) {
			g_util_webserial.send("syslog", "system/settings#load => OK");
		} else {
			g_util_webserial.send("syslog", "system/settings#load => ERROR");
		}
	}
	if(data.containsKey("save")) {
		if(g_system_settings.save() == true) {
			g_util_webserial.send("syslog", "system/settings#save => OK");
		} else {
			g_util_webserial.send("syslog", "system/settings#save => ERROR");
		}
	}
	if(data.containsKey("reset")) {
		if(g_system_settings.reset() == true) {
			g_util_webserial.send("syslog", "system/settings#reset => OK");
		} else {
			g_util_webserial.send("syslog", "system/settings#reset => ERROR");
		}
	}
}


void on_system_time(const JsonVariant& data) {
	if(data.containsKey("sync")) {
		if(data["sync"].containsKey("epoch")) {
			system_time_set(data["sync"]["epoch"].as<long>());
		}
	}
	if(data.containsKey("config")) {
		int interval_secs = SYSTEM_RUNTIME_TIME_SYNC_INTERVAL;

		if(g_system_runtime.count("system/time:sync/interval") == 1) {
			interval_secs = atoi(g_system_runtime["system/time:sync/interval"].c_str());
		}
		if(data["config"].containsKey("interval")) {
			interval_secs = data["config"]["interval"].as<int>();
			etl::to_string(interval_secs, g_system_runtime["system/time:sync/interval"]);
		}
		setSyncProvider(system_time_sync);
		setSyncInterval(interval_secs);
	}
}


void on_system_reset(const JsonVariant& data) {
	bool  uf2 = false;

	if(data.containsKey("uf2")) {
		uf2 = data["uf2"].as<bool>();
	}
	if(uf2) {
		g_util_webserial.send("syslog", "Resetting RP2040 with boot target UF2...");
		system_rp2040_reset_uf2();
	}
	g_util_webserial.send("syslog", "Resetting RP2040...");
	system_rp2040_reset();
}

