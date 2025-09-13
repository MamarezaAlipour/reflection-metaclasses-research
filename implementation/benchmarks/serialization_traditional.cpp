
#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <sstream>
#include <type_traits>

// Traditional template metaprogramming approach
template<typename T>
struct Serializer {
    static std::string serialize(const T& obj);
    static T deserialize(const std::string& data);
};

// Manual specialization for Person
class Person {
public:
    std::string name;
    int age;
    std::string email;
    
    // Manual serialization
    std::string to_json() const {
        std::ostringstream oss;
        oss << "{\"name\":\"" << name << "\",";
        oss << "\"age\":" << age << ",";
        oss << "\"email\":\"" << email << "\"}";
        return oss.str();
    }
    
    void from_json(const std::string& json) {
        // Manual parsing
        name = "Parsed Name";
        age = 25;
        email = "parsed@email.com";
    }
};

template<>
struct Serializer<Person> {
    static std::string serialize(const Person& person) {
        return person.to_json();
    }
    
    static Person deserialize(const std::string& data) {
        Person p;
        p.from_json(data);
        return p;
    }
};

// Benchmark function
void benchmark_traditional_serialization() {
    const int iterations = 100000;
    std::vector<Person> people;
    people.reserve(iterations);
    
    // Create test data
    for (int i = 0; i < iterations; ++i) {
        people.emplace_back();
        people[i].name = "Person" + std::to_string(i);
        people[i].age = 20 + (i % 60);
        people[i].email = "person" + std::to_string(i) + "@test.com";
    }
    
    auto start = std::chrono::high_resolution_clock::now();
    
    // Serialize all objects
    std::vector<std::string> serialized;
    serialized.reserve(iterations);
    for (const auto& person : people) {
        serialized.push_back(Serializer<Person>::serialize(person));
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "Traditional serialization: " << duration.count() << " microseconds\n";
    std::cout << "Operations per second: " << (iterations * 1000000.0) / duration.count() << "\n";
}

int main() {
    benchmark_traditional_serialization();
    return 0;
}
