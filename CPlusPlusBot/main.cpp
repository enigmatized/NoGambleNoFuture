#include <iostream>
#include <curl/curl.h>
//#include <nlohmann/json.hpp>
#include "DataCleaner/json.hpp"

#include "DataCleaner/JSONhelpers.h"
#include "ExchangeCalls/APIcalls.h"
#include "TradeManager/OandaManager.h"


//Below was added to make a list of json then eventually save that to file
#include <vector>

//Packages related to sleep a thread
#include <chrono>
#include <thread>

//Packages to writing json to file
#include <fstream>

//Package to get current time
#include <ctime>

#include <tuple>



using json = nlohmann::json;


std::tuple<int, int, int> getCurrentTime() {
    // Get the current system time
    auto currentTime = std::chrono::system_clock::now();

    // Convert the system time to a time_t object (representing seconds since epoch)
    std::time_t time = std::chrono::system_clock::to_time_t(currentTime);

    // Convert the time_t to a local time tm struct
    std::tm* localTime = std::localtime(&time);

    // Get the hours, minutes, and seconds from the time struct
    int hours = localTime->tm_hour;
    int minutes = localTime->tm_min;
    int seconds = localTime->tm_sec;

    // Return the tuple (hours, minutes, seconds)
    return std::make_tuple(hours, minutes, seconds);
}



int getCurrentMinutes(){
    // Get the current system time
    auto currentTime = std::chrono::system_clock::now();

    // Convert the system time to a time_t object (representing seconds since epoch)
    std::time_t time = std::chrono::system_clock::to_time_t(currentTime);

    // Convert the time_t to a local time tm struct
    std::tm* localTime = std::localtime(&time);

    // Get the minutes from the time struct
    int minutes = localTime->tm_min;

    return minutes;
}


int getMinuteFromStringTime(std::string timeString){
    // Create an istringstream from the time string
    std::istringstream iss(timeString);

    // Variables to store the extracted values
    int hours, minutes, seconds;

    // Use getline to extract the hours, minutes, and seconds from the time string
    char delimiter;
    iss >> hours >> delimiter >> minutes >> delimiter >> seconds;

    // Convert minutes to an int
    int minutesInt = minutes;

    return minutesInt;
}

int main()
{
   

    //API Setup tokens for Onanda
    std::ifstream inputfile("../APITokens/bearTokenAndAccountInfo.json");
    json jsonData;
    inputfile >> jsonData;
    inputfile.close();
    // Access the values from the JSON object
    std::string bearer = jsonData["bearer"];
    std::string account = jsonData["account"];
    //Setup the header for the API call    
    std::string oauthBearer = "Authorization: Bearer " + bearer;


    //Read json from file, 
    //each  json  is a look up of
    // key :: string == "USD_JPY07:12:13"
    // value :: Tuple (float, float) == (mean , standard deviation) == (.003, .0005)

    std::ifstream inputfile1("OnStart/Data/Oanda/EUR_USD_M5_price_delta.json"); //TODO read each file name
    json EurUsdM5PriceDeltaMeanAndStdDev; //TODO then from file name parse out the currency pair and the granularity
    inputfile1 >> EurUsdM5PriceDeltaMeanAndStdDev; //TODO then create the lookup table
    inputfile1.close(); // Also abstract this out to one function call that takes no arguements

    //SETUP trade managers (as of now I only have one)
    OandaManager oandaManager;

    std::thread tradeThread(&OandaManager::manageTrades, &oandaManager);
    

    //Container for respose data
    std::vector<json> arrays_of_order_books;
   int end___ = 3;

   for (int i =0; i < end___ ; i++){
        json data = fetchData(oauthBearer);
        json data_api = fetchMarketCandles(oauthBearer, "EUR_USD", "3", "M5");
        printJson(data_api);
        std::cout << data_api["candles"][0]["time"] << std::endl;

        //////////////////////
        //TODO abstract this out and catch if T or . is not found
        std::string timeData = data_api["candles"][0]["time"];
        size_t tPos = timeData.find('T');
        size_t perioidPos = timeData.find('.');
        std::string timePart = (timeData.substr(0, perioidPos)).substr(tPos +1, tPos + 9) ;
        std::cout << "Time stripped: " << timePart << std::endl;
        ////////////////////////


        //Look up the mean and standard deviation from stripped time
       
        std::cout << "Lookup values: " <<  EurUsdM5PriceDeltaMeanAndStdDev[timePart][0].type_name() << std::endl; //TODO then from file name parse out the currency pair and the granularity
        double open =  std::stof(data_api["candles"][0]["mid"]["o"].get<std::string>())  ;
        double close = std::stof(data_api["candles"][0]["mid"]["c"].get<std::string>())  ;

        double open_close_delta = close - open;
        
        std::cout << "what is this value: " <<  data_api["candles"][0]["mid"]["o"].type_name() << std::endl; //TODO then from file name parse out the currency pair and the granularity
        

        double mean = EurUsdM5PriceDeltaMeanAndStdDev[timePart][0];
        double std_dev = EurUsdM5PriceDeltaMeanAndStdDev[timePart][1];        
        double z_score = ( open_close_delta- mean )  / std_dev;
        std::cout << "Z score: " << z_score << std::endl;
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

        if (z_score > 3){
            auto [hour, minutes, seconds] = getCurrentTime();

            if (minutes % 5 == 4){
                if (seconds > 30) {
                    std::cout << "Order sent to Trade manager  "  << std::endl;
                    oandaManager.updateTradesToMake("EUR_USD" , 3, "M5");
                }
            }

        }        
        
        arrays_of_order_books.push_back(data);
        std::this_thread::sleep_for(std::chrono::seconds(11));
        

   }
    std::cout << "THe length of the vector is:  " << arrays_of_order_books.size() << std::endl;
    
    std::ofstream file("output_first_attempt_do_throw_away.json");
    file << json(arrays_of_order_books).dump(4);  // Use dump() with indentation of 4 spaces
    file.close();

    std::cout << "JSON data written to file." << std::endl;



    return 0;
}










