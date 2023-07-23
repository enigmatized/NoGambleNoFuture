#include <list>
#include <map>
#include <tuple>

#include <atomic>
#include <chrono>
#include <thread>

class OandaManager {
public:
    // Member variables
    int    myInt;
    double myDouble;
    std::atomic<bool> isUpdated{false};
    int tradeCount;
    //Most oanda orders will be market orders
    std::list<std::tuple<std::string, int, std::string>> tradeToMakeQueue;
    std::map<std::string, int> numberOfTradesInTimeFrameMap;


 //////////////////////////////////////////   
    // Member functions
//////////////////////////////////////////
    void printValues();

    //Lets us know if an update to the trades to be made is needed
    void updateTradesToMake(std::string, int , std::string) ;

    void manageTrades();
};