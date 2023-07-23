#include "OandaManager.h" // Include the header file
#include <iostream>
#include <chrono>
#include <list>
#include <map>
#include <tuple>

#include <atomic>

void OandaManager::printValues() {
    std::cout << "myInt: " << myInt << ", myDouble: " << myDouble << std::endl;
}


void OandaManager::updateTradesToMake(std::string currency, int count, std::string granularity) {
        
        std::cout << "Updating trades to make..." << std::endl;
        
        //Add to queue to proccess trade in manageTrades
        tradeToMakeQueue.push_back(std::make_tuple(currency, count, granularity));

        isUpdated = true;
}

void OandaManager::manageTrades() {
        while (true) {
            // Check if MyClass is updated
            if (isUpdated.load()) {// Why do I use a bool here and not just the list size?
                // Your trade management logic here
                std::cout << "Managing trades..." << std::endl;
                // Reset the isUpdated flag after processing the update
                //
                auto& frontTuple   = tradeToMakeQueue.front();
                std::string currency;
                int orderSize;
                std::string granularity;
                std::tie(currency, orderSize, granularity) = frontTuple;

                //Make the trade
                //Then check if it was a success
                //If it was a success then pop the front of the queue
                //Then send this info back to the data manager
                //Who will send you info on new trades
                //This means I need another queue
                //That is trade management queue rather than the trade making queue
                //This also means the exchangeRequestManager needs to be a class
                //Which will manage the amount each exchange is allowed to be called
                //Also wether it is getting data for a specific trade or just general data
                //In this way I can throttle the calls to the exchange
                //Where I make more calls for trades I am in and less for trades I am not in, but looking for opportunities
                tradeToMakeQueue.pop_front();
                
                isUpdated = false;
            }

            // Sleep for a short time to avoid busy-waiting
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }
}