#ifndef MEANREVERSION_H 
#define MEANREVERSION_H


#include <iostream>

#include <chrono>

#include <queue>

#include "../DataCleaner/json.hpp" 
#include "../TradeManager/OandaManager.h"
#include "SpecificStratgeyInterface.h"

using namespace std::chrono;
using namespace std;
using json = nlohmann::json;

//TODO this will need some form of priority queue
class MeanReversion : public SpecificStratgeyInterface {
private:
    //TODO improve this
    static float z_score;
    static map<std::string, json> assetToMeanSdMap;
    //TODO make both a list or map to handle multiple excahnges
    // and multiple assets
    static OandaManager* oandaTradeManager;
    nlohmann::json  oanda5minEURUSD;
    


public:
    MeanReversion();
    MeanReversion(OandaManager*);
    void evaluateAndProcess(json, string, string)  override;
    bool evaluateStrategy(json, string, string)    override;
    json cleanData(json)                           override;
    
};

#endif //MEANREVERSION_H