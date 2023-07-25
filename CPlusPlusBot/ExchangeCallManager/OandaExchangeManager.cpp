#include "OandaExchangeManager.h"
#include "../ExchangeCalls/APIcalls.h"
#include <iostream>
#include "../DataCleaner/json.hpp" 
#include <curl/curl.h>
//Packages to writing json to file
#include <fstream>


using json = nlohmann::json;

int OandaExchangeManager:: secondCount = 0; // Initialize the class variable
int OandaExchangeManager:: minuteCount = 0; // Initialize the class variable
int OandaExchangeManager:: hourCount   = 0; // Initialize the class variable
std::string  OandaExchangeManager::bearerToken = "";
std::string  OandaExchangeManager::accountNumber = "";


OandaExchangeManager::OandaExchangeManager() {
    std::ifstream configFile("../../APITokens/bearTokenAndAccountInfo.json");
    if (configFile.is_open()) {
        nlohmann::json configJson;
        configFile >> configJson;
        // Read and set the values for accountNumber and bearerToken
        accountNumber = configJson["accountNumber"];
        bearerToken  = configJson["bearerToken"];
    } else {
        std::cerr << "Error: Failed to open exchange_config.json." << std::endl;
    }
}


void OandaExchangeManager::setupTokens() {

}


void OandaExchangeManager::getMarketData() {
    json data_api = fetchMarketCandles(bearerToken, "EUR_USD", "3", "M5");
    std::cout << data_api["candles"][0]["time"] << std::endl;
    // Implement the API call to get market data
}

void OandaExchangeManager::makeLimitOrder() {
    // Implement the API call to make a limit order
}

void OandaExchangeManager::makeMarketOrder() {
    // Implement the API call to make a market order
}