#ifndef SPECIFICEXCHANGE_H
#define SPECIFICEXCHANGE_H

#include "../DataCleaner/json.hpp" 
#include "../StrategyManager/MeanReversion.h"
// #include "../StrategyManager/SpecificStratgeyInterface.h"
#include <iostream>
#include "SpecificExchangeManagerInterface.h"
#include <queue>
#include <iostream>
#include <chrono>

using namespace std::chrono;
using namespace std;
using json = nlohmann::json;

//TODO this will need some form of priority queue
class OandaExchangeManager : public SpecificExchangeManagerInterface {
private:
    //TODO improve this
    static int secondCount;
    static int minuteCount;
    static int hourCount;
    static std::string bearerToken;
    static std::string accountNumber;
    static MeanReversion strategyManager;


public:
    OandaExchangeManager();
    OandaExchangeManager(MeanReversion toRevertTo);

    void setupTokens()     override;
    json getMarketData()   override;
    void makeLimitOrder()  override;
    void makeMarketOrder() override;
    void mainCallLoop()    override;
    queue<time_point<system_clock>> updateQueue(queue<time_point<system_clock>> timeQueue, int timeLength) override;
    void sendToStrategyManager(json data) override;

    
};

#endif // SPECIFICEXCHANGE_H