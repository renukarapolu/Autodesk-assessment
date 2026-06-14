#include <string>
#include <cassert>
#include <algorithm>
#include <iostream>


std::string reverse_words(const std::string &str) {
    std::string result = str;
    size_t length = result.length();
    size_t start = 0;

    for (size_t i = 0; i <= length; ++i) {
        if (i == length || !std::isalnum(static_cast<unsigned char>(result[i]))) {
            if (i > start) {
                std::reverse(result.begin() + start, result.begin() + i);
            }
            start = i + 1;
        }
    }
    return result;
}

int main() {
    std::string test_str = "String; 2be reversed...";
    std::string expected = "gnirtS; eb2 desrever...";
    
    assert(reverse_words(test_str) == expected);
    
    std::cout << "Assignment 1: Assert passed successfully." << std::endl;
    return 0;
}
