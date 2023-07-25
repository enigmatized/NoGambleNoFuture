#ifndef SPECIFICEXCHANGE_H
#define SPECIFICEXCHANGE_H

#include <iostream>
#include "SpecificExchangeManagerInterface.h"


//TODO this will need some form of priority queue
class OandaExchangeManager : public SpecificExchangeManagerInterface {
private:
    //TODO improve this
    static int secondCount;
    static int minuteCount;
    static int hourCount;
    static std::string bearerToken;
    static std::string accountNumber;


public:
    OandaExchangeManager();

    void setupTokens()     override;
    void getMarketData()   override;
    void makeLimitOrder()  override;
    void makeMarketOrder() override;
};

#endif // SPECIFICEXCHANGE_H