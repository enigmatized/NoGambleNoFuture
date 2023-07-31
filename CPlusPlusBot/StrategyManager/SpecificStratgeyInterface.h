#ifndef STRAT_H
#define STRAT_H

#include "../DataCleaner/json.hpp" 
#include <chrono>
#include <iostream>
#include <queue>


using json = nlohmann::json;
using namespace std::chrono;
using namespace std;
class SpecificStratgeyInterface {
public:
    virtual void evaluateAndProcess(json, string, string) = 0; //What does this =0 mean?
    virtual bool evaluateStrategy(json, string, string) = 0;
    virtual json cleanData(json)        = 0; //What does this =0 mean?
};

#endif // STRAT_H