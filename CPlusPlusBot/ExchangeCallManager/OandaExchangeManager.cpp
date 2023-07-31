#include "OandaExchangeManager.h"
#include "../ExchangeCalls/APIcalls.h"
#include <iostream>
#include "../DataCleaner/json.hpp" 
#include <curl/curl.h>
#include "../StrategyManager/MeanReversion.h"

//Packages to writing json to file
#include <fstream>

#include <chrono>
#include <functional>
#include <iostream>
#include <map>
#include <queue>
#include <thread>


using json = nlohmann::json;
using namespace std::chrono;
using namespace std;

int OandaExchangeManager:: secondCount = 0; // Initialize the class variable
int OandaExchangeManager:: minuteCount = 0; // Initialize the class variable
int OandaExchangeManager:: hourCount   = 0; // Initialize the class variable
std::string  OandaExchangeManager::bearerToken = "";
std::string  OandaExchangeManager::accountNumber = "";
MeanReversion OandaExchangeManager::strategyManager;


OandaExchangeManager::OandaExchangeManager(){};

OandaExchangeManager::OandaExchangeManager(MeanReversion toRevertTo) {
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
    strategyManager = toRevertTo;
}


void OandaExchangeManager::setupTokens() {

}


void OandaExchangeManager::mainCallLoop() {
    //So we want to make sure we are not calling the API more than 100 times per second
    //Well Actually we don't know the times.
    //All modern day APIs have a limit on how many times you can call them per second, per minute, per hour, per day, etc.
    //And the amount changes on daily basis
  const int secondCounter = 1; // Replace 10 with your desired queue size limit
  const int minuteCounter = 4; // Replace 10 with your desired queue size limit
  queue<time_point<system_clock>> timeQueue;
  queue<time_point<system_clock>> secondQueue;
  queue<time_point<system_clock>> minuteQueue;
  queue<time_point<system_clock>> hoursQueue;

  while (true) {
    // Check the queue size and perform an action if it's less than maxSize
    // The queue size represents the number of times we have called 
    // the API in the last period designated for that queue
    if (secondQueue.size() <= secondCounter &&
        minuteQueue.size() <= minuteCounter) {
      
      cout << "Performing an action at: "
           << system_clock::to_time_t(system_clock::now()) << endl;

      json marketData = getMarketData();

      // Create a thread using a lambda expression to pass arguments
      std::thread threadObj([marketData]() { 
            strategyManager.evaluateStrategy(marketData, "EUR_USD", "5M");
        });//TODO research if this will eat up too much memory down the road.
      
      
      //Didn't think how I should I send this out.
      //Should each strategy have its own module/thread?
      //That eventually connects to TradeManager?
      // Add the current time to the queue

      //For now I should keep it simple, but if I was to expand this.
      //Say I have a multi strategy
      //Running on the same exchange.... Which now that I think about it.... seems like an over complication
      //I should have one strategy per exchange
      //Otherwise there will be times I want to long and short at the same time
      //Coding wise that will add a lot more complexity
      //That really isn't needed
      //So I should have one strategy per exchange
      //That doesn't mean I shouldn't be using multiple exchanges as data feeds 
      //Or run mutliple strategies on the same exchange, but on different currencies.
      secondQueue.push(system_clock::now());
      minuteQueue.push(system_clock::now());
    }

    secondQueue = updateQueue(secondQueue, 1);
    minuteQueue = updateQueue(minuteQueue, 60);

    // Check if any entries are older than a minute (60 seconds) and remove them

    // Simulate a delay so that the loop doesn't run too frequently
    this_thread::sleep_for(seconds(1));
  }



}


// void OandaExchangeManager::getMarketData() {
//     json data_api = fetchMarketCandles(bearerToken, "EUR_USD", "3", "M5");
//     std::cout << data_api["candles"][0]["time"] << std::endl;
//     // Implement the API call to get market data
// }

//TODO, shouldn't I be making this private?
queue<time_point<system_clock>> OandaExchangeManager::updateQueue(queue<time_point<system_clock>> timeQueue, int timeLength) {

  while (!timeQueue.empty()) {
    auto frontTime = timeQueue.front();
    auto currentTime = system_clock::now();
    auto duration = duration_cast<seconds>(currentTime - frontTime).count();
    if (duration > timeLength) {
      timeQueue.pop();
    } else {
      break; // The queue is sorted by time, so if the front entry is not
             // older than a minute, the rest won't be either
    }
  }

  return timeQueue;
}


void OandaExchangeManager::sendToStrategyManager(json marketData) {

    // Implement the API call to make a limit order
}

json OandaExchangeManager::getMarketData() {
    json data_api = fetchMarketCandles(bearerToken, "EUR_USD", "3", "M5");
    std::cout << data_api["candles"][0]["time"] << std::endl;
    return data_api;
}

void OandaExchangeManager::makeLimitOrder() {
    // Implement the API call to make a limit order
}



void OandaExchangeManager::makeMarketOrder() {
    // Implement the API call to make a market order
}
