
#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <type_traits>
#include <sstream>

// Traditional complex template hierarchy
template<typename T>
class Container {
private:
    std::vector<T> data_;
    
public:
    void add(const T& item) { data_.push_back(item); }
    
    size_t size() const { return data_.size(); }
    
    std::string get_type_name() const {
        return std::string("Container<") + typeid(T).name() + ">";
    }
    
    std::string serialize() const {
        std::ostringstream oss;
        oss << "[";
        for (size_t i = 0; i < data_.size(); ++i) {
            if (i > 0) oss << ",";
            serialize_element(oss, data_[i]);
        }
        oss << "]";
        return oss.str();
    }
    
private:
    void serialize_element(std::ostringstream& oss, const T& element) const {
        if constexpr (std::is_arithmetic_v<T>) {
            oss << element;
        } else {
            oss << """ << element << """;
        }
    }
};

// Manual specializations for different types
template<>
class Container<std::string> {
private:
    std::vector<std::string> data_;
    
public:
    void add(const std::string& item) { data_.push_back(item); }
    
    size_t size() const { return data_.size(); }
    
    std::string get_type_name() const {
        return "Container<std::string>";
    }
    
    std::string serialize() const {
        std::ostringstream oss;
        oss << "[";
        for (size_t i = 0; i < data_.size(); ++i) {
            if (i > 0) oss << ",";
            oss << """ << data_[i] << """;
        }
        oss << "]";
        return oss.str();
    }
};

void benchmark_template_traditional() {
    const int iterations = 50000;
    
    Container<int> int_container;
    Container<std::string> string_container;
    Container<double> double_container;
    
    auto start = std::chrono::high_resolution_clock::now();
    
    // Fill containers and serialize
    for (int i = 0; i < iterations; ++i) {
        int_container.add(i);
        string_container.add("item" + std::to_string(i));
        double_container.add(i * 3.14);
        
        if (i % 1000 == 0) {
            auto int_ser = int_container.serialize();
            auto str_ser = string_container.serialize();
            auto dbl_ser = double_container.serialize();
        }
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "Template Traditional: " << duration.count() << " microseconds\n";
    std::cout << "Operations per second: " << (iterations * 1000000.0) / duration.count() << "\n";
}

int main() {
    benchmark_template_traditional();
    return 0;
}
