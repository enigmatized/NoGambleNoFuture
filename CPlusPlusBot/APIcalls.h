#pragma once //What is this?

#include <string>
#include <curl/curl.h>
#include "DataCleaner/json.hpp"

using json = nlohmann::json;

size_t WriteCallback(char* data, size_t size, size_t nmemb, std::string* buffer);

json fetchData(const std::string& oauthBearer);