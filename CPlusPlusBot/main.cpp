#include <iostream>
#include <curl/curl.h>
//#include <nlohmann/json.hpp>
#include "DataCleaner/json.hpp"

#include "DataCleaner/JSONhelpers.h"
#include "APIcalls.h"


//Below was added to make a list of json then eventually save that to file
#include <vector>

//Packages related to sleep a thread
#include <chrono>
#include <thread>

//Packages to writing json to file
#include <fstream>

using json = nlohmann::json;


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


    //Container for respose data
    std::vector<json> arrays_of_order_books;
   int end___ = 3;

   for (int i =0; i < end___ ; i++){
        json data = fetchData(oauthBearer);
        arrays_of_order_books.push_back(data);
        std::this_thread::sleep_for(std::chrono::seconds(10));
   }
    std::cout << "THe length of the vector is:  " << arrays_of_order_books.size() << std::endl;
    
    std::ofstream file("output_first_attempt_do_throw_away.json");
    file << json(arrays_of_order_books).dump(4);  // Use dump() with indentation of 4 spaces
    file.close();

    std::cout << "JSON data written to file." << std::endl;



    return 0;
}










