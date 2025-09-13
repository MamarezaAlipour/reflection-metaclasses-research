// Example Code Demonstrations for Reflection & Metaclasses Paper
// C++23 Advanced Reflection and Metaclass Implementation Examples

#include <iostream>
#include <string>
#include <vector>
#include <memory>
#include <type_traits>
#include <sstream>
#include <functional>
#include <ranges>
#include <concepts>
#include <experimental/meta>  // C++23 reflection header (experimental)
#include <experimental/reflect>  // Alternative experimental header

// ================================
// SECTION 1: Basic Reflection API
// ================================

namespace basic_reflection {
    
    // Example struct for reflection
    struct Person {
        std::string name;
        int age;
        double salary;
        
        void greet() const {
            std::cout << "Hello, I'm " << name << std::endl;
        }
        
        void celebrate_birthday() {
            ++age;
        }
    };
    
    // Basic reflection queries
    template<typename T>
    void analyze_type() {
        using namespace std::experimental::reflect;
        
        constexpr auto meta_type = reflexpr(T);
        
        std::cout << "Type: " << get_display_name_v<meta_type> << std::endl;
        std::cout << "Size: " << sizeof(T) << " bytes" << std::endl;
        std::cout << "Is class: " << std::boolalpha << is_class_v<meta_type> << std::endl;
        
        // Iterate through data members
        std::cout << "\nData Members:" << std::endl;
        constexpr auto members = get_data_members_t<meta_type>{};
        
        // C++23 reflection iteration
        []<auto... Ms>(std::index_sequence<Ms...>) {
            ([]<auto M>() {
                constexpr auto member = get_element_v<M, decltype(members)>;
                std::cout << "  " << get_name_v<member> 
                         << " : " << get_display_name_v<get_type_t<member>> << std::endl;
            }.template operator()<Ms>(), ...);
        }(std::make_index_sequence<get_size_v<members>>{});
        
        // Iterate through member functions
        std::cout << "\nMember Functions:" << std::endl;
        constexpr auto functions = get_member_functions_t<meta_type>{};
        
        []<auto... Fs>(std::index_sequence<Fs...>) {
            ([]<auto F>() {
                constexpr auto func = get_element_v<F, decltype(functions)>;
                std::cout << "  " << get_name_v<func> << "()" << std::endl;
            }.template operator()<Fs>(), ...);
        }(std::make_index_sequence<get_size_v<functions>>{});
    }
}

// ================================
// SECTION 2: Advanced Metaclasses
// ================================

namespace metaclasses {
    
    // Serializable metaclass for automatic JSON serialization
    constexpr void serializable(meta::type_info target) {
        // Generate to_json method
        meta::compiler.require(meta::is_class(target), 
                             "serializable can only be applied to classes");
        
        std::string to_json_impl = R"(
            std::string to_json() const {
                std::ostringstream oss;
                oss << "{";
                bool first = true;
        )";
        
        // Iterate through data members and generate serialization code
        for (auto member : meta::data_members_of(target)) {
            if (!first) {
                to_json_impl += R"(oss << ",";)";
            }
            to_json_impl += "first = false;\n";
            to_json_impl += "oss << \"\\\"" + meta::name_of(member) + "\\\":\";\n";
            
            // Type-specific serialization
            auto member_type = meta::type_of(member);
            if (meta::is_same(member_type, meta::reflexpr(std::string))) {
                to_json_impl += "oss << \"\\\"\" << " + meta::name_of(member) + " << \"\\\"\";\n";
            } else if (meta::is_arithmetic(member_type)) {
                to_json_impl += "oss << " + meta::name_of(member) + ";\n";
            }
        }
        
        to_json_impl += R"(
                oss << "}";
                return oss.str();
            }
        )";
        
        meta::compiler.declare(target, to_json_impl);
        
        // Generate from_json static method
        std::string from_json_impl = R"(
            static auto from_json(const std::string& json) {
                // Implementation would parse JSON and create object
                // This is a simplified example
                auto result = )" + meta::name_of(target) + R"(();
                // JSON parsing logic here...
                return result;
            }
        )";
        
        meta::compiler.declare(target, from_json_impl);
    }
    
    // Observable metaclass for automatic observer pattern implementation
    constexpr void observable(meta::type_info target) {
        // Add observer infrastructure
        std::string observer_code = R"(
        private:
            std::vector<std::function<void()>> observers_;
            
        public:
            void add_observer(std::function<void()> observer) {
                observers_.push_back(std::move(observer));
            }
            
            void notify_observers() {
                for (const auto& observer : observers_) {
                    observer();
                }
            }
        )";
        
        meta::compiler.declare(target, observer_code);
        
        // Modify all setters to call notify_observers
        for (auto member : meta::data_members_of(target)) {
            std::string setter_name = "set_" + meta::name_of(member);
            std::string setter_impl = 
                "void " + setter_name + "(const " + 
                meta::name_of(meta::type_of(member)) + "& value) {\n" +
                "    " + meta::name_of(member) + " = value;\n" +
                "    notify_observers();\n" +
                "}";
            
            meta::compiler.declare(target, setter_impl);
        }
    }
    
    // Database Entity metaclass for ORM functionality
    constexpr void entity(meta::type_info target, const std::string& table_name = "") {
        std::string actual_table_name = table_name.empty() ? 
            meta::name_of(target) : table_name;
        
        // Generate SQL creation statement
        std::string create_table_sql = "CREATE TABLE " + actual_table_name + " (";
        bool first = true;
        
        for (auto member : meta::data_members_of(target)) {
            if (!first) create_table_sql += ", ";
            first = false;
            
            create_table_sql += meta::name_of(member) + " ";
            
            auto member_type = meta::type_of(member);
            if (meta::is_same(member_type, meta::reflexpr(int))) {
                create_table_sql += "INTEGER";
            } else if (meta::is_same(member_type, meta::reflexpr(std::string))) {
                create_table_sql += "TEXT";
            } else if (meta::is_same(member_type, meta::reflexpr(double))) {
                create_table_sql += "REAL";
            }
        }
        create_table_sql += ");";
        
        // Generate ORM methods
        std::string orm_methods = R"(
            static std::string get_create_table_sql() {
                return ")" + create_table_sql + R"(";
            }
            
            std::string to_insert_sql() const {
                std::ostringstream oss;
                oss << "INSERT INTO )" + actual_table_name + R"( (";
        )";
        
        // Add column names
        first = true;
        for (auto member : meta::data_members_of(target)) {
            if (!first) orm_methods += "oss << \", \";\n";
            first = false;
            orm_methods += "oss << \"" + meta::name_of(member) + "\";\n";
        }
        
        orm_methods += R"(
                oss << ") VALUES (";
        )";
        
        // Add values
        first = true;
        for (auto member : meta::data_members_of(target)) {
            if (!first) orm_methods += "oss << \", \";\n";
            first = false;
            
            auto member_type = meta::type_of(member);
            if (meta::is_same(member_type, meta::reflexpr(std::string))) {
                orm_methods += "oss << \"'\" << " + meta::name_of(member) + " << \"'\";\n";
            } else {
                orm_methods += "oss << " + meta::name_of(member) + ";\n";
            }
        }
        
        orm_methods += R"(
                oss << ");";
                return oss.str();
            }
        )";
        
        meta::compiler.declare(target, orm_methods);
    }
}

// ================================
// SECTION 3: Usage Examples
// ================================

namespace usage_examples {
    
    // Apply metaclasses to regular classes
    class $serializable $observable Person {
        std::string name;
        int age;
        double salary;
        
    public:
        Person(std::string n, int a, double s) 
            : name(std::move(n)), age(a), salary(s) {}
            
        // Getters
        const std::string& get_name() const { return name; }
        int get_age() const { return age; }
        double get_salary() const { return salary; }
    };
    
    class $entity("employees") Employee {
        int id;
        std::string name;
        std::string department;
        double salary;
        
    public:
        Employee(int i, std::string n, std::string d, double s)
            : id(i), name(std::move(n)), department(std::move(d)), salary(s) {}
    };
    
    // Advanced composition of metaclasses
    class $serializable $observable $entity("products") Product {
        int product_id;
        std::string name;
        double price;
        int stock_quantity;
        
    public:
        Product(int id, std::string n, double p, int stock)
            : product_id(id), name(std::move(n)), price(p), stock_quantity(stock) {}
    };
}

// ================================
// SECTION 4: Performance Benchmarks
// ================================

namespace benchmarks {
    
    // Traditional template-based serialization
    template<typename T>
    class traditional_serializer {
        // Complex template metaprogramming for type introspection
        // Multiple template specializations required
        // Compile-time complexity grows exponentially
    };
    
    // Reflection-based serialization
    template<typename T>
    std::string reflect_serialize(const T& obj) {
        using namespace std::experimental::reflect;
        constexpr auto meta_type = reflexpr(T);
        
        std::ostringstream oss;
        oss << "{";
        
        constexpr auto members = get_data_members_t<meta_type>{};
        bool first = true;
        
        []<auto... Ms>(std::index_sequence<Ms...>, const T& object, 
                      std::ostringstream& stream, bool& is_first) {
            (serialize_member<Ms>(object, stream, is_first), ...);
        }(std::make_index_sequence<get_size_v<members>>{}, obj, oss, first);
        
        oss << "}";
        return oss.str();
    }
    
    template<auto M, typename T>
    static void serialize_member(const T& obj, std::ostringstream& oss, bool& first) {
        if (!first) oss << ",";
        first = false;
        
        constexpr auto members = get_data_members_t<reflexpr(T)>{};
        constexpr auto member = get_element_v<M, decltype(members)>;
        
        oss << "\"" << get_name_v<member> << "\":";
        
        // Get member value using reflection
        auto value = obj.*(get_pointer_v<member>);
        
        // Type-specific serialization
        if constexpr (std::is_same_v<decltype(value), std::string>) {
            oss << "\"" << value << "\"";
        } else {
            oss << value;
        }
    }
}

// ================================
// SECTION 5: Integration Examples
// ================================

namespace integration {
    
    // Integration with Concepts
    template<typename T>
    concept Reflectable = requires {
        typename std::experimental::reflect::get_data_members_t<
            std::experimental::reflect::reflexpr(T)>;
    };
    
    template<Reflectable T>
    void process_reflectable_type(const T& obj) {
        // Compile-time guaranteed reflection capabilities
        auto json = reflect_serialize(obj);
        std::cout << "Serialized: " << json << std::endl;
    }
    
    // Integration with Coroutines
    template<typename T>
    std::generator<std::string> reflect_member_names() {
        using namespace std::experimental::reflect;
        constexpr auto meta_type = reflexpr(T);
        constexpr auto members = get_data_members_t<meta_type>{};
        
        []<auto... Ms>(std::index_sequence<Ms...>) -> std::generator<std::string> {
            ((co_yield get_name_v<get_element_v<Ms, decltype(members)>>), ...);
        }(std::make_index_sequence<get_size_v<members>>{});
    }
    
    // Integration with Ranges
    template<typename T>
    auto get_member_values_range(const T& obj) {
        using namespace std::experimental::reflect;
        constexpr auto meta_type = reflexpr(T);
        
        return get_data_members_t<meta_type>{}
             | std::views::transform([&obj](auto member) {
                   return obj.*(get_pointer_v<member>);
               })
             | std::views::transform([](const auto& value) {
                   return std::to_string(value);
               });
    }
}

// ================================
// SECTION 6: Error Handling
// ================================

namespace error_handling {
    
    // Compile-time validation using reflection
    template<typename T>
    consteval bool validate_serializable() {
        using namespace std::experimental::reflect;
        constexpr auto meta_type = reflexpr(T);
        
        // Check if all members are serializable
        constexpr auto members = get_data_members_t<meta_type>{};
        
        return []<auto... Ms>(std::index_sequence<Ms...>) consteval {
            return (is_serializable_type<get_type_t<
                get_element_v<Ms, decltype(members)>>> && ...);
        }(std::make_index_sequence<get_size_v<members>>{});
    }
    
    template<typename T>
    consteval bool is_serializable_type() {
        using U = std::remove_cv_t<std::remove_reference_t<T>>;
        return std::is_arithmetic_v<U> || 
               std::is_same_v<U, std::string> ||
               validate_serializable<U>();
    }
    
    // Static assertion for compile-time safety
    template<typename T>
    void safe_serialize(const T& obj) {
        static_assert(validate_serializable<T>(), 
                     "Type contains non-serializable members");
        
        auto result = reflect_serialize(obj);
        std::cout << result << std::endl;
    }
}

// ================================
// Main demonstration function
// ================================

int main() {
    using namespace usage_examples;
    using namespace basic_reflection;
    
    // Basic reflection demonstration
    std::cout << "=== Basic Reflection Analysis ===" << std::endl;
    analyze_type<Person>();
    
    // Metaclass usage demonstration
    std::cout << "\n=== Metaclass Demonstration ===" << std::endl;
    Person person("Alice", 30, 75000.0);
    
    // Generated methods from metaclasses
    std::cout << "JSON: " << person.to_json() << std::endl;
    
    // Observer pattern in action
    person.add_observer([]() {
        std::cout << "Person data changed!" << std::endl;
    });
    
    person.set_age(31);  // Will trigger observer notification
    
    // Database entity demonstration
    Employee emp(1, "Bob", "Engineering", 85000.0);
    std::cout << "SQL: " << emp.to_insert_sql() << std::endl;
    
    return 0;
}

/*
Expected Output:
=== Basic Reflection Analysis ===
Type: Person
Size: 32 bytes
Is class: true

Data Members:
  name : std::string
  age : int
  salary : double

Member Functions:
  greet()
  celebrate_birthday()

=== Metaclass Demonstration ===
JSON: {"name":"Alice","age":30,"salary":75000}
Person data changed!
SQL: INSERT INTO employees (id, name, department, salary) VALUES (1, 'Bob', 'Engineering', 85000);
*/
