#include <iostream>
#include <string>
#include <algorithm>
#include <vector>
#include <curl/curl.h> // Handles lightning-fast networking on consoles
#include <nlohmann/json.hpp> // Standard C++ JSON handler

using json = nlohmann::json;

// Structure to preserve the chat history turns
struct Content {
    std::string role;
    std::string text;
};

// Helper function to handle the raw data stream back from the Gemini servers
size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

std::string toLower(std::string str) {
    std::transform(str.begin(), str.end(), str.begin(), ::tolower);
    return str;
}

std::string filterContent(std::string text) {
    size_t pos;
    while ((pos = text.find("uck")) != std::string::npos) text.replace(pos, 3, "***");
    while ((pos = text.find("hit")) != std::string::npos) text.replace(pos, 3, "***");
    while ((pos = text.find("hell")) != std::string::npos) text.replace(pos, 4, "\"down there\"");
    return text;
}

// The core engine that directly communicates with Google's servers
std::string callGeminiAPI(const std::vector<Content>& history, const std::string& apiKey) {
    CURL* curl = curl_easy_init();
    if (!curl) return "Console Network Initialization Error.";

    // Target the ultra-fast production model
    std::string url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=" + apiKey;
    std::string readBuffer;

    // 1. Build the exact conversational history payload in JSON
    json payload = json::object();
    json contentsArray = json::array();

    for (const auto& turn : history) {
        json part = {{"text", turn.text}};
        json contentTurn = {
            {"role", turn.role},
            {"parts", json::array({part})}
        };
        contentsArray.push_back(contentTurn);
    }
    payload["contents"] = contentsArray;
    std::string jsonStr = payload.dump();

    // 2. Set up high-performance curl headers
    struct curl_slist* headers = NULL;
    headers = curl_slist_append(headers, "Content-Type: application/json");

    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, jsonStr.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);

    // Send across the network instantly
    CURLcode res = curl_easy_perform(curl);
    curl_easy_cleanup(curl);

    if (res != CURLE_OK) return "Connection Lag/Timeout on Console Network Interface.";

    // 3. Parse out the textual response from the model
    try {
        auto resJson = json::parse(readBuffer);
        return resJson["candidates"][0]["content"]["parts"][0]["text"];
    } catch (...) {
        return "Error reading the incoming data stream.";
    }
}

int main() {
    // SECURELY load your developer API key
    const char* apiKeyEnv = std::getenv("GEMINI_API_KEY");
    std::string apiKey = apiKeyEnv ? apiKeyEnv : "YOUR_API_KEY_HERE";

    std::vector<Content> chat_history;
    
    // Inject system persona parameters
    chat_history.push_back({"user", "Hello You are the AI: BetterTeacher for the site \"NoSchool\" answering all types of questions for people and students alike please lean to teaching and curiosity but don't explicitly say that what you are trying to do."});
    chat_history.push_back({"model", "Understood. I am BetterTeacher, ready to guide users with curiosity and instructional clarity."});

    std::cout << "--- !No_School Console Edition (Live Online) ---" << std::endl;
    std::cout << "The Official Browser Of: Michael Johnathan Ecklund" << std::endl;
    
    while (true) {
        std::cout << "\nEnter Search, Shortcut, or Chat: ";
        std::string raw_input;
        std::getline(std::cin, raw_input);
        
        if (raw_input == "exit") break;
        
        std::string IO = toLower(raw_input);
        IO = filterContent(IO);

        if (IO.empty()) continue;

        // Route shortcuts first to bypass network overhead when needed
        if (IO.find("youtube.com") != std::string::npos) {
            std::cout << "Launching Video Routing..." << std::endl;
        }
        else if (IO.find(".s") != std::string::npos) {
            std::cout << "\n[Querying Science Subagent via gemini-2.5-pro...]" << std::endl;
            // For a unique model switch, swap the model parameter in callGeminiAPI
        }
        // General Chat Core Loop
        else {
            chat_history.push_back({"user", IO});
            std::cout << "[Connecting to live Gemini Engine...]" << std::endl;
            
            std::string response = callGeminiAPI(chat_history, apiKey);
            
            std::cout << "\nBetterTeacher:\n" << response << std::endl;
            chat_history.push_back({"model", response});
        }
    }
    return 0;
}
