
#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <functional>

// Traditional property binding implementation
class DataModel {
private:
    std::string name_;
    int value_;
    bool active_;
    
public:
    std::vector<std::function<void()>> name_changed_callbacks;
    std::vector<std::function<void()>> value_changed_callbacks;
    std::vector<std::function<void()>> active_changed_callbacks;
    
    const std::string& name() const { return name_; }
    void set_name(const std::string& new_name) {
        if (name_ != new_name) {
            name_ = new_name;
            for (auto& callback : name_changed_callbacks) {
                callback();
            }
        }
    }
    
    int value() const { return value_; }
    void set_value(int new_value) {
        if (value_ != new_value) {
            value_ = new_value;
            for (auto& callback : value_changed_callbacks) {
                callback();
            }
        }
    }
    
    bool active() const { return active_; }
    void set_active(bool new_active) {
        if (active_ != new_active) {
            active_ = new_active;
            for (auto& callback : active_changed_callbacks) {
                callback();
            }
        }
    }
    
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

void benchmark_binding_traditional() {
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
    
    std::cout << "Binding Traditional: " << duration.count() << " microseconds\n";
    std::cout << "Property updates per second: " << (iterations * 3 * 1000000.0) / duration.count() << "\n";
}

int main() {
    benchmark_binding_traditional();
    return 0;
}
