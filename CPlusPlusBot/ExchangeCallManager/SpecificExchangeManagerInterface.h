#ifndef EXCHANGE_H
#define EXCHANGE_H

#include "../DataCleaner/json.hpp" 
#include <chrono>
#include <iostream>
#include <queue>


using json = nlohmann::json;
using namespace std::chrono;
using namespace std;
class SpecificExchangeManagerInterface {
public:
    virtual void setupTokens()     = 0; //What does this =0 mean?
    virtual json getMarketData()   = 0;
    virtual void makeLimitOrder()  = 0;
    virtual void makeMarketOrder() = 0;
    virtual void mainCallLoop()    = 0;
    virtual queue<time_point<system_clock>> updateQueue(queue<time_point<system_clock>> timeQueue, int timeLength) =0;
    virtual void sendToStrategyManager(json data) = 0;
};

#endif // EXCHANGE_H