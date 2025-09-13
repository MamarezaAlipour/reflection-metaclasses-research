
#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <functional>

// Property binding with reflection simulation
class $bindable DataModel {
public:
    std::string name;
    int value;
    bool active;
    
    // Generated property change notifications
    std::vector<std::function<void()>> name_changed_callbacks;
    std::vector<std::function<void()>> value_changed_callbacks;
    std::vector<std::function<void()>> active_changed_callbacks;
    
    void set_name(const std::string& new_name) {
        if (name != new_name) {
            name = new_name;
            for (auto& callback : name_changed_callbacks) {
                callback();
            }
        }
    }
    
    void set_value(int new_value) {
        if (value != new_value) {
            value = new_value;
            for (auto& callback : value_changed_callbacks) {
                callback();
            }
        }
    }
    
    void set_active(bool new_active) {
        if (active != new_active) {
            active = new_active;
            for (auto& callback : active_changed_callbacks) {
                callback();
            }
        }
    }
    
    // Generated binding methods
    void bind_name_changed(std::function<void()> callback) {
        name_changed_callbacks.push_back(callback);
    }
    
    void bind_value_changed(std::function<void()> callback) {
        value_changed_callbacks.push_back(callback);
    }
    
    void bind_active_changed(std::function<void()> callback) {
        active_changed_callbacks.push_back(callback);
    }
};

void benchmark_binding_reflection() {
    const int iterations = 25000;
    std::vector<DataModel> models;
    models.reserve(iterations);
    
    // Create models with bindings
    for (int i = 0; i < iterations; ++i) {
        models.emplace_back();
        models[i].bind_name_changed([i]() { /* callback */ });
        models[i].bind_value_changed([i]() { /* callback */ });
        models[i].bind_active_changed([i]() { /* callback */ });
    }
    
    auto start = std::chrono::high_resolution_clock::now();
    
    // Trigger property changes
    for (int i = 0; i < iterations; ++i) {
        models[i].set_name("Name" + std::to_string(i));
        models[i].set_value(i * 2);
        models[i].set_active(i % 2 == 0);
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "Binding Reflection: " << duration.count() << " microseconds\n";
    std::cout << "Property updates per second: " << (iterations * 3 * 1000000.0) / duration.count() << "\n";
}

int main() {
    benchmark_binding_reflection();
    return 0;
}
