#include "MeanReversion.h"
#include "../ExchangeCalls/APIcalls.h"
#include <iostream>
#include "../DataCleaner/json.hpp" 
#include <curl/curl.h>
//Packages to writing json to file
#include <fstream>

#include <chrono>
#include <functional>
#include <iostream>
#include <map>
#include <queue>
#include <thread>


#include "../StrategyManager/MeanReversion.h"

using namespace std::chrono;
using namespace std;
using json = nlohmann::json;


float MeanReversion::z_score = 3.0;
std::map<std::string, nlohmann::json> MeanReversion::assetToMeanSdMap = std::map<std::string, nlohmann::json>();
OandaManager* MeanReversion::oandaTradeManager = nullptr;
nlohmann::json  oanda5minEURUSD;///This should be a map of string of asset name to json, where the json is a map of time to mean and sd

//So ideally we would have
//hmm I am going to have to think about this as well.
//Right now I might only focus on EUR_USD one time frame
//But later I will want to focus on it on multiple time frames
//Then there are multiple assets to consider.....
//It might be best to either have a general z-score based strategy
//Or read from file, have a function that figures out the optimized values/sttrategy for that asset on that time frame....
//I think that is the best way to do it.
//Especially if I want to trade multiple assets at once.
//I probably should have both.
//If I run this on the stock market, scanning stocks to do this.
//Unless I have an api where I can pull a few megabytes of historial data at once
//I will have some stocks I can trade because I have the data locally and some 
//I am just going to have run a generic strategy on

//For now I will just have a generic strategy


MeanReversion::MeanReversion() {
    //TODO
    //For now load dictionaries of data I am dealing with
    //Later I will have to figure out how to load data live

}


MeanReversion::MeanReversion(OandaManager* tradeAndRiskManager) {
    oandaTradeManager=tradeAndRiskManager;
    //TODO
    //For now load dictionaries of data I am dealing with
    //Later I will have to figure out how to load data live

        //Read json from file, 
    //each  json  is a look up of
    // key :: string == "USD_JPY07:12:13"
    // value :: Tuple (float, float) == (mean , standard deviation) == (.003, .0005)
    std::ifstream inputfile1("OnStart/Data/Oanda/EUR_USD_M5_price_delta.json"); //TODO read each file name
    json EurUsdM5PriceDeltaMeanAndStdDev; //TODO then from file name parse out the currency pair and the granularity
    inputfile1 >> EurUsdM5PriceDeltaMeanAndStdDev; //TODO then create the lookup table
    inputfile1.close(); // Also abstract this out to one function call that takes no arguements
    oanda5minEURUSD = EurUsdM5PriceDeltaMeanAndStdDev;

}


void MeanReversion::evaluateAndProcess(json marketData, std::string assetPair, std::string timeFrame) {

    if (evaluateStrategy(marketData, assetPair, timeFrame)) {
        //TODO place trade
        //TODO log trade
        //TODO log trade to file
        //TODO un hard code quantity.
        //TODO research if I should be spinning off into its own thread.
        oandaTradeManager -> updateTradesToMake(assetPair, -3, timeFrame);

    }



}

bool MeanReversion::evaluateStrategy(json marketData, std::string assetPair, std::string timeFrame) {
        
        //First load the data associated with the asset pair and time frame
        // And clean the data

            ///HERE we are cleaning the data, by getting the time frame            
        int lastCandleIndex = marketData["candles"].size() - 1; //to make this part happen check the number of candles we have from Oanda 
        
        //TODO abstract out the string manipulation
        std::string timeData = marketData["candles"][lastCandleIndex]["time"];
        size_t tPos = timeData.find('T');
        size_t perioidPos = timeData.find('.');
        std::string timePart = (timeData.substr(0, perioidPos)).substr(tPos +1, tPos + 9) ;
        std::cout << "Time stripped: " << timePart << std::endl;
        
        // Second calculate the z-score
        // Third check if the z-score is greater than 3

                //Look up the mean and standard deviation from stripped time
       
        std::cout << "Lookup values: " <<  oanda5minEURUSD[timePart][0].type_name() << std::endl; //TODO then from file name parse out the currency pair and the granularity
        double open =  std::stof(marketData["candles"][lastCandleIndex]["mid"]["o"].get<std::string>())  ;
        double close = std::stof(marketData["candles"][lastCandleIndex]["mid"]["c"].get<std::string>())  ;

        double open_close_delta = close - open;
        
        std::cout << "what is this value: " <<  marketData["candles"][0]["mid"]["o"].type_name() << std::endl; //TODO then from file name parse out the currency pair and the granularity
        

        double mean = oanda5minEURUSD[timePart][0];
        double std_dev = oanda5minEURUSD[timePart][1];        
        double calculated_z_score = ( open_close_delta- mean )  / std_dev;
        std::cout << "Z score: " << calculated_z_score << std::endl;
        // Now I need to place a trade based on the z-score
        // If z-score send off to the trade manager bot
        // Trade manager has a bit of complicated logic
        // but for now I am going to keep it simple and just send off a trade
        // This also means the trade manager bot needs to calling the API endpoint as well
        // So the api call needs to send the z-score/strategy decision maker
        // and the trade manager bot
        // The trade manager bot will be most complicated for Oanda because they do not allow limit orders and holding orders
        // For not I think I should keep things very simple with only a 3> sd move buy
        
        /////////////////////////////////////////////////////////
        //So there should be some logic here.
        //If I am 3 minutes away from the end of the 5 minute candle
        //But I already have 3sd move, not sure what the proper action is?
        //That is something I need to do some more DS on.
        //For now I am going to get the time and see if it is close to the end of the candle,
        //If it is I will not place a trade.


        if (z_score <= calculated_z_score){
            return true;
        }
        return false;    
}


json MeanReversion::cleanData(json marketData) {
    //TODO implement this
    return marketData;
}    
