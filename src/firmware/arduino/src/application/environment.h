#ifndef __APPLICATION_ENVIRONMENT_H__
#define __APPLICATION_ENVIRONMENT_H__

#include <etl/string.h>
#include <etl/map.h>
#include <ArduinoJson.h>


typedef etl::map<etl::string<GLOBAL_KEY_SIZE>, etl::string<GLOBAL_VALUE_SIZE>, APPLICATION_ENVIRONMENT_MAX> EnvironmentMap;
class Application;

class Environment : public EnvironmentMap {
};


class EnvironmentWriter {
	private:
		Application& m_application;
		etl::string<GLOBAL_KEY_SIZE> m_key;
	public:
		EnvironmentWriter(Application& application, const etl::string<GLOBAL_KEY_SIZE>& key);

		size_t write(uint8_t c);
		size_t write(const uint8_t *buffer, size_t length);
};

#endif

