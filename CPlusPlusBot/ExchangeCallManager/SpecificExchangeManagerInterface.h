#ifndef EXCHANGE_H
#define EXCHANGE_H

class SpecificExchangeManagerInterface {
public:
    virtual void setupTokens()     = 0;
    virtual void getMarketData()   = 0;
    virtual void makeLimitOrder()  = 0;
    virtual void makeMarketOrder() = 0;
};

#endif // EXCHANGE_H