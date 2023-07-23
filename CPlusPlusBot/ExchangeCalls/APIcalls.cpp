#include "APIcalls.h"
#include <iostream>

size_t WriteCallback(char* data, size_t size, size_t nmemb, std::string* buffer) {
    size_t totalSize = size * nmemb;
    buffer->append(data, totalSize);
    return totalSize;
}

json fetchData(const std::string& oauthBearer) {
    std::string response;
    CURL* curl = curl_easy_init();

    if (curl) {
        const char* url = "https://api-fxtrade.oanda.com/v3/instruments/USD_JPY/orderBook";
        struct curl_slist* headers = nullptr;
        headers = curl_slist_append(headers, "Content-Type: application/json");
        headers = curl_slist_append(headers, oauthBearer.c_str());
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);

        CURLcode res = curl_easy_perform(curl);

        if (res != CURLE_OK) {
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
        }

        curl_easy_cleanup(curl);
    }

    return json::parse(response);
}


json fetchMarketCandles(const std::string& oauthBearer, const std::string& currency, const std::string& count, const std::string& granularity) {
    std::string response;
    CURL* curl = curl_easy_init();

    if (curl) {
        // const char* url = "https://api-fxtrade.oanda.com/v3/instruments/USD_JPY/orderBook";
        //Note to self I should make all of these c-style strings for optimization purposes
        std::string url_ = "https://api-fxtrade.oanda.com/v3/instruments/" + currency + "/candles?count=" + count + "&price=M&granularity=" +"M15";
        const char* url = url_.c_str(); 
        struct curl_slist* headers = nullptr;
        headers = curl_slist_append(headers, "Content-Type: application/json");
        headers = curl_slist_append(headers, oauthBearer.c_str());
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);

        CURLcode res = curl_easy_perform(curl);

        if (res != CURLE_OK) {
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
        }

        curl_easy_cleanup(curl);
    }

    return json::parse(response);
}