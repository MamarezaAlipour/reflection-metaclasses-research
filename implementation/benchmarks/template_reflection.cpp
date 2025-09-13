
#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <type_traits>

// Complex template hierarchy with reflection
template<typename T>
class $reflectable Container {
private:
    std::vector<T> data_;
    
public:
    void add(const T& item) { data_.push_back(item); }
    
    size_t size() const { return data_.size(); }
    
    // Generated introspection methods
    static std::string get_type_name() {
        return "Container<" + get_element_type_name() + ">";
    }
    
    static std::string get_element_type_name() {
        return typeid(T).name();
    }
    
    // Generated serialization
    std::string serialize() const {
        std::string result = "[";
        for (size_t i = 0; i < data_.size(); ++i) {
            if (i > 0) result += ",";
            result += serialize_element(data_[i]);
        }
        result += "]";
        return result;
    }
    
private:
    std::string serialize_element(const T& element) const {
        if constexpr (std::is_arithmetic_v<T>) {
            return std::to_string(element);
        } else {
            return """ + std::string(element) + """;
        }
    }
};

void benchmark_template_reflection() {
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
    
    std::cout << "Template Reflection: " << duration.count() << " microseconds\n";
    std::cout << "Operations per second: " << (iterations * 1000000.0) / duration.count() << "\n";
}

int main() {
    benchmark_template_reflection();
    return 0;
}
