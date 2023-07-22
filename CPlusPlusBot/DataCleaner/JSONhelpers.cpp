#include <iostream>
#include "json.hpp"

using json = nlohmann::json;



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
