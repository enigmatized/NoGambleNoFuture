#include <iostream>
#include <curl/curl.h>
//#include <nlohmann/json.hpp>
#include "json.hpp"


//Below was added to make a list of json then eventually save that to file
#include <vector>

//Packages related to sleep a thread
#include <chrono>
#include <thread>

//Packages to writing json to file
#include <fstream>

using json = nlohmann::json;


// Callback function to handle the response data
size_t WriteCallback(char* data, size_t size, size_t nmemb, std::string* buffer) {
    size_t totalSize = size * nmemb;
    buffer->append(data, totalSize);
    return totalSize;
}




void printJson(const json& jsonObj) {
    for (auto& element : jsonObj.items()) {
        const auto& key = element.key();
        const auto& value = element.value();

        if (value.is_object()) {
            std::cout << "Key: " << key << ", Value: (Nested JSON Object)" << std::endl;
            printJson(value);  // Recursively call printJson for nested objects
        } else {
            std::cout << "Key: " << key << ", Value: " << value << std::endl;
        }
    }
}


int main()
{
   


    std::ifstream inputfile("bearTokenAndAccountInfo.json");
    json jsonData;
    inputfile >> jsonData;
    inputfile.close();

    // Access the values from the JSON object
    std::string bearer = jsonData["bearer"];
    std::string account = jsonData["account"];    
    
    std::vector<json> arrays_of_order_books;
   
    std::string oauthBearer = "Authorization: Bearer " + bearer;

   int end___ = 1000;

   for (int i =0; i < end___ ; i++){
    std::string response;

    std::string jsonResponse = "{\"key1\":\"value1\",\"key2\":42}";

    json data = json::parse(jsonResponse);

    std::string value1 = data["key1"];
    int value2 = data["key2"];

    std::cout << "Value1: " << value1 << std::endl;
    std::cout << "Value2: " << value2 << std::endl;


    std::cout << "No need to store this string? Or do I\n";
    CURL* curl = curl_easy_init();
    if (curl) {
        const char* url =  "https://api-fxtrade.oanda.com/v3/instruments/USD_JPY/orderBook";
  //"https://www.example.com";
        
	struct curl_slist* headers = nullptr;
        headers = curl_slist_append(headers, "Content-Type: application/json");
        
        
	
	
        headers = curl_slist_append(headers, oauthBearer.c_str());
	curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
	
	//This works, but will comment out to test something else
    	curl_easy_setopt(curl, CURLOPT_URL, url);
        //curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
	//
	// Set the callback function to capture the response
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
	curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);

        std::cout << "Do I get the output before this\n";

        CURLcode res = curl_easy_perform(curl);
	std::cout << "output after this\n";
	if (res == CURLE_OK) {
            long status_code = 0;
            //std::cout <<  "Garrett, trying wacky" << curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &status_code);
            
            
	    json data_ = json::parse(response);
	    //for (auto& element : data_.items()) {
	    //	     const auto& key = element.key();
            //         const auto& value = element.value();
           //	     std::cout << "Key: " << key << ", Value: " << value << std::endl;
	   // }
	   //
	   printJson(data_);
	   
	   arrays_of_order_books.push_back(data_);
	   std :: cout << "we added it to our vector?" << std::endl;
           
	    //std::cout << "We did it Marty"  << response << std::endl;
	    size_t length = data_.size();

    	    std::cout << "Length of JSON object: " << length << std::endl;	   	
	    //json data_ = json::parse(response);
            std::cout << "HTTP status code: " << status_code << std::endl;
        }
        else {
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
        }

        curl_easy_cleanup(curl);
    }

    std::this_thread::sleep_for(std::chrono::seconds(45));
   }
    std::cout << "THe length of the vector is:  " << arrays_of_order_books.size() << std::endl;
    
    std::ofstream file("output_first_attempt_do_throw_away.json");
    file << json(arrays_of_order_books).dump(4);  // Use dump() with indentation of 4 spaces
    file.close();

    std::cout << "JSON data written to file." << std::endl;



    return 0;
}





//https://api-fxtrade.oanda.com/v3/instruments/USD_JPY/orderBook

//Now can I do this for an exchange and order book?


//Finally, we clean up the CURL* handle using curl_easy_cleanup().

//Note that this is just a simple example and there are many ways to make HTTPS requests in C++ using different libraries and frameworks.







