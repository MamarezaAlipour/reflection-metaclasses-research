"""
Comprehensive Benchmark Suite for C++23 Reflection and Metaclasses Research
============================================================================

This module provides comprehensive benchmarking capabilities for analyzing
the performance characteristics of C++23 reflection and metaclasses compared
to traditional C++ metaprogramming approaches.

Author: Mohammadreza Alipour
Date: August 24, 2025
"""

import time
import subprocess
import os
import json
import statistics
import csv
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

# Optional imports for visualization (will work without them)
try:
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    HAS_VISUALIZATION = True
except ImportError:
    HAS_VISUALIZATION = False
    print("Note: Visualization packages not available. Continuing without plots.")

@dataclass
class BenchmarkResult:
    """Represents the result of a single benchmark run."""
    name: str
    compilation_time: float  # seconds
    binary_size: int  # bytes
    runtime_performance: float  # operations per second
    memory_usage: int  # bytes
    error_count: int
    warning_count: int
    
@dataclass
class ComparisonResult:
    """Represents comparison between reflection and traditional approaches."""
    test_case: str
    reflection_result: BenchmarkResult
    traditional_result: BenchmarkResult
    compilation_speedup: float
    runtime_speedup: float
    size_ratio: float
    memory_ratio: float

class CPPBenchmarkFramework:
    """Framework for running C++ compilation and runtime benchmarks."""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.benchmark_dir = self.project_root / "implementation" / "benchmarks"
        self.results_dir = self.project_root / "results"
        self.results_dir.mkdir(exist_ok=True)
        
        # Compiler configurations
        self.compilers = {
            "gcc": {
                "command": "g++",
                "flags": ["-std=c++23", "-O2", "-Wall", "-Wextra"],
                "reflection_flags": ["-freflection"]  # Hypothetical flag
            },
            "clang": {
                "command": "clang++", 
                "flags": ["-std=c++23", "-O2", "-Wall", "-Wextra"],
                "reflection_flags": ["-freflection"]  # Hypothetical flag
            }
        }
        
    def create_test_cases(self):
        """Create comprehensive test cases for benchmarking."""
        
        # Test Case 1: Basic Serialization
        self._create_serialization_benchmark()
        
        # Test Case 2: ORM/Database Mapping
        self._create_orm_benchmark()
        
        # Test Case 3: Property Binding
        self._create_binding_benchmark()
        
        # Test Case 4: Design Pattern Generation
        self._create_pattern_benchmark()
        
        # Test Case 5: Complex Template Hierarchies
        self._create_template_benchmark()
        
    def _create_serialization_benchmark(self):
        """Create serialization performance benchmark."""
        
        # Reflection-based implementation
        reflection_code = '''
#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <sstream>

// Simulated C++23 reflection (using placeholder implementation)
namespace std::meta {
    template<typename T> struct reflexpr_result {};
    template<typename T> constexpr auto reflexpr(T) { return reflexpr_result<T>{}; }
    template<auto meta> constexpr auto get_name() { return "member"; }
    template<auto meta> constexpr auto data_members_of(meta) { return std::array<int, 3>{}; }
}

// Metaclass simulation
#define $serializable

class $serializable Person {
public:
    std::string name;
    int age;
    std::string email;
    
    // Generated serialization (simulated)
    std::string to_json() const {
        std::ostringstream oss;
        oss << "{\\"name\\":\\"" << name << "\\",";
        oss << "\\"age\\":" << age << ",";
        oss << "\\"email\\":\\"" << email << "\\"}";
        return oss.str();
    }
    
    void from_json(const std::string& json) {
        // Simplified parsing simulation
        name = "Parsed Name";
        age = 25;
        email = "parsed@email.com";
    }
};

// Benchmark function
void benchmark_reflection_serialization() {
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
        serialized.push_back(person.to_json());
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "Reflection serialization: " << duration.count() << " microseconds\\n";
    std::cout << "Operations per second: " << (iterations * 1000000.0) / duration.count() << "\\n";
}

int main() {
    benchmark_reflection_serialization();
    return 0;
}
'''
        
        # Traditional template-based implementation
        traditional_code = '''
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
        oss << "{\\"name\\":\\"" << name << "\\",";
        oss << "\\"age\\":" << age << ",";
        oss << "\\"email\\":\\"" << email << "\\"}";
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
    
    std::cout << "Traditional serialization: " << duration.count() << " microseconds\\n";
    std::cout << "Operations per second: " << (iterations * 1000000.0) / duration.count() << "\\n";
}

int main() {
    benchmark_traditional_serialization();
    return 0;
}
'''
        
        # Write test files
        (self.benchmark_dir / "serialization_reflection.cpp").write_text(reflection_code)
        (self.benchmark_dir / "serialization_traditional.cpp").write_text(traditional_code)
        
    def _create_orm_benchmark(self):
        """Create ORM performance benchmark."""
        
        orm_reflection_code = '''
#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <map>

// Simulated ORM with reflection
class $entity User {
public:
    int id;
    std::string username;
    std::string email;
    int age;
    
    // Generated SQL methods (simulated)
    std::string to_insert_sql() const {
        return "INSERT INTO users (id, username, email, age) VALUES (" +
               std::to_string(id) + ", '" + username + "', '" + email + "', " +
               std::to_string(age) + ")";
    }
    
    std::string to_update_sql() const {
        return "UPDATE users SET username='" + username + "', email='" + email +
               "', age=" + std::to_string(age) + " WHERE id=" + std::to_string(id);
    }
    
    static std::string select_all_sql() {
        return "SELECT id, username, email, age FROM users";
    }
};

void benchmark_orm_reflection() {
    const int iterations = 50000;
    std::vector<User> users;
    users.reserve(iterations);
    
    // Generate test data
    for (int i = 0; i < iterations; ++i) {
        User user;
        user.id = i;
        user.username = "user" + std::to_string(i);
        user.email = "user" + std::to_string(i) + "@test.com";
        user.age = 20 + (i % 50);
        users.push_back(user);
    }
    
    auto start = std::chrono::high_resolution_clock::now();
    
    // Generate SQL statements
    std::vector<std::string> sql_statements;
    sql_statements.reserve(iterations);
    for (const auto& user : users) {
        sql_statements.push_back(user.to_insert_sql());
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "ORM Reflection: " << duration.count() << " microseconds\\n";
    std::cout << "SQL generations per second: " << (iterations * 1000000.0) / duration.count() << "\\n";
}

int main() {
    benchmark_orm_reflection();
    return 0;
}
'''
        
        orm_traditional_code = '''
#include <iostream>
#include <string>
#include <vector>
#include <chrono>

// Traditional ORM implementation
class User {
public:
    int id;
    std::string username;
    std::string email;
    int age;
    
    // Manual SQL generation
    std::string to_insert_sql() const {
        return "INSERT INTO users (id, username, email, age) VALUES (" +
               std::to_string(id) + ", '" + username + "', '" + email + "', " +
               std::to_string(age) + ")";
    }
    
    std::string to_update_sql() const {
        return "UPDATE users SET username='" + username + "', email='" + email +
               "', age=" + std::to_string(age) + " WHERE id=" + std::to_string(id);
    }
    
    static std::string select_all_sql() {
        return "SELECT id, username, email, age FROM users";
    }
};

// Manual ORM helper
template<typename T>
class ORM {
public:
    static std::string generate_insert(const T& obj);
    static std::string generate_update(const T& obj);
    static std::string generate_select();
};

template<>
class ORM<User> {
public:
    static std::string generate_insert(const User& user) {
        return user.to_insert_sql();
    }
    
    static std::string generate_update(const User& user) {
        return user.to_update_sql();
    }
    
    static std::string generate_select() {
        return User::select_all_sql();
    }
};

void benchmark_orm_traditional() {
    const int iterations = 50000;
    std::vector<User> users;
    users.reserve(iterations);
    
    // Generate test data
    for (int i = 0; i < iterations; ++i) {
        User user;
        user.id = i;
        user.username = "user" + std::to_string(i);
        user.email = "user" + std::to_string(i) + "@test.com";
        user.age = 20 + (i % 50);
        users.push_back(user);
    }
    
    auto start = std::chrono::high_resolution_clock::now();
    
    // Generate SQL statements
    std::vector<std::string> sql_statements;
    sql_statements.reserve(iterations);
    for (const auto& user : users) {
        sql_statements.push_back(ORM<User>::generate_insert(user));
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "ORM Traditional: " << duration.count() << " microseconds\\n";
    std::cout << "SQL generations per second: " << (iterations * 1000000.0) / duration.count() << "\\n";
}

int main() {
    benchmark_orm_traditional();
    return 0;
}
'''
        
        (self.benchmark_dir / "orm_reflection.cpp").write_text(orm_reflection_code)
        (self.benchmark_dir / "orm_traditional.cpp").write_text(orm_traditional_code)
    
    def _create_binding_benchmark(self):
        """Create property binding benchmark."""
        
        binding_reflection_code = '''
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
    
    std::cout << "Binding Reflection: " << duration.count() << " microseconds\\n";
    std::cout << "Property updates per second: " << (iterations * 3 * 1000000.0) / duration.count() << "\\n";
}

int main() {
    benchmark_binding_reflection();
    return 0;
}
'''
        
        binding_traditional_code = '''
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
    
    std::cout << "Binding Traditional: " << duration.count() << " microseconds\\n";
    std::cout << "Property updates per second: " << (iterations * 3 * 1000000.0) / duration.count() << "\\n";
}

int main() {
    benchmark_binding_traditional();
    return 0;
}
'''
        
        (self.benchmark_dir / "binding_reflection.cpp").write_text(binding_reflection_code)
        (self.benchmark_dir / "binding_traditional.cpp").write_text(binding_traditional_code)
    
    def _create_pattern_benchmark(self):
        """Create design pattern generation benchmark."""
        
        pattern_reflection_code = '''
#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <memory>

// Observer pattern with reflection
class $observable Subject {
private:
    std::string state_;
    std::vector<std::function<void(const std::string&)>> observers_;
    
public:
    void set_state(const std::string& new_state) {
        if (state_ != new_state) {
            state_ = new_state;
            notify_observers();
        }
    }
    
    const std::string& get_state() const { return state_; }
    
    // Generated observer management
    void add_observer(std::function<void(const std::string&)> observer) {
        observers_.push_back(observer);
    }
    
    void remove_observer(size_t index) {
        if (index < observers_.size()) {
            observers_.erase(observers_.begin() + index);
        }
    }
    
    void notify_observers() {
        for (auto& observer : observers_) {
            observer(state_);
        }
    }
};

void benchmark_pattern_reflection() {
    const int iterations = 10000;
    const int observers_per_subject = 10;
    
    std::vector<Subject> subjects;
    subjects.reserve(iterations);
    
    // Setup subjects with observers
    for (int i = 0; i < iterations; ++i) {
        subjects.emplace_back();
        for (int j = 0; j < observers_per_subject; ++j) {
            subjects[i].add_observer([i, j](const std::string& state) {
                // Observer callback
            });
        }
    }
    
    auto start = std::chrono::high_resolution_clock::now();
    
    // Trigger state changes
    for (int i = 0; i < iterations; ++i) {
        subjects[i].set_state("State" + std::to_string(i));
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "Pattern Reflection: " << duration.count() << " microseconds\\n";
    std::cout << "Notifications per second: " << (iterations * observers_per_subject * 1000000.0) / duration.count() << "\\n";
}

int main() {
    benchmark_pattern_reflection();
    return 0;
}
'''
        
        pattern_traditional_code = '''
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
    
    std::cout << "Pattern Traditional: " << duration.count() << " microseconds\\n";
    std::cout << "Notifications per second: " << (iterations * observers_per_subject * 1000000.0) / duration.count() << "\\n";
}

int main() {
    benchmark_pattern_traditional();
    return 0;
}
'''
        
        (self.benchmark_dir / "pattern_reflection.cpp").write_text(pattern_reflection_code)
        (self.benchmark_dir / "pattern_traditional.cpp").write_text(pattern_traditional_code)
    
    def _create_template_benchmark(self):
        """Create complex template hierarchy benchmark."""
        
        template_reflection_code = '''
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
            return "\"" + std::string(element) + "\"";
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
    
    std::cout << "Template Reflection: " << duration.count() << " microseconds\\n";
    std::cout << "Operations per second: " << (iterations * 1000000.0) / duration.count() << "\\n";
}

int main() {
    benchmark_template_reflection();
    return 0;
}
'''
        
        template_traditional_code = '''
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
            oss << "\"" << element << "\"";
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
            oss << "\"" << data_[i] << "\"";
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
    
    std::cout << "Template Traditional: " << duration.count() << " microseconds\\n";
    std::cout << "Operations per second: " << (iterations * 1000000.0) / duration.count() << "\\n";
}

int main() {
    benchmark_template_traditional();
    return 0;
}
'''
        
        (self.benchmark_dir / "template_reflection.cpp").write_text(template_reflection_code)
        (self.benchmark_dir / "template_traditional.cpp").write_text(template_traditional_code)

if __name__ == "__main__":
    # Initialize benchmark framework
    framework = CPPBenchmarkFramework("C:/Users/P - K/Downloads/cpp prop/reflection_metaclasses_paper")
    
    print("Creating comprehensive C++ benchmark test cases...")
    framework.create_test_cases()
    print("✅ Benchmark test cases created successfully!")
    
    print("\\nBenchmark files created:")
    benchmark_files = [
        "serialization_reflection.cpp", "serialization_traditional.cpp",
        "orm_reflection.cpp", "orm_traditional.cpp", 
        "binding_reflection.cpp", "binding_traditional.cpp",
        "pattern_reflection.cpp", "pattern_traditional.cpp",
        "template_reflection.cpp", "template_traditional.cpp"
    ]
    
    for file in benchmark_files:
        print(f"  📁 {file}")
    
    print("\\n🚀 Ready for compilation and benchmarking!")
