
#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <memory>
#include <algorithm>

// Traditional observer pattern
class Observer {
public:
    virtual ~Observer() = default;
    virtual void update(const std::string& state) = 0;
};

class Subject {
private:
    std::string state_;
    std::vector<std::shared_ptr<Observer>> observers_;
    
public:
    void set_state(const std::string& new_state) {
        if (state_ != new_state) {
            state_ = new_state;
            notify_observers();
        }
    }
    
    const std::string& get_state() const { return state_; }
    
    void add_observer(std::shared_ptr<Observer> observer) {
        observers_.push_back(observer);
    }
    
    void remove_observer(std::shared_ptr<Observer> observer) {
        observers_.erase(
            std::remove(observers_.begin(), observers_.end(), observer),
            observers_.end()
        );
    }
    
    void notify_observers() {
        for (auto& observer : observers_) {
            if (auto obs = observer.lock ? observer : observer) {
                obs->update(state_);
            }
        }
    }
};

class ConcreteObserver : public Observer {
private:
    int id_;
    
public:
    ConcreteObserver(int id) : id_(id) {}
    
    void update(const std::string& state) override {
        // Observer implementation
    }
};

void benchmark_pattern_traditional() {
    const int iterations = 10000;
    const int observers_per_subject = 10;
    
    std::vector<Subject> subjects;
    std::vector<std::vector<std::shared_ptr<Observer>>> observers;
    
    subjects.reserve(iterations);
    observers.reserve(iterations);
    
    // Setup subjects with observers
    for (int i = 0; i < iterations; ++i) {
        subjects.emplace_back();
        observers.emplace_back();
        
        for (int j = 0; j < observers_per_subject; ++j) {
            auto observer = std::make_shared<ConcreteObserver>(j);
            observers[i].push_back(observer);
            subjects[i].add_observer(observer);
        }
    }
    
    auto start = std::chrono::high_resolution_clock::now();
    
    // Trigger state changes
    for (int i = 0; i < iterations; ++i) {
        subjects[i].set_state("State" + std::to_string(i));
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "Pattern Traditional: " << duration.count() << " microseconds\n";
    std::cout << "Notifications per second: " << (iterations * observers_per_subject * 1000000.0) / duration.count() << "\n";
}

int main() {
    benchmark_pattern_traditional();
    return 0;
}
