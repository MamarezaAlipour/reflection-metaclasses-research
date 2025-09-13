
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
    
    std::cout << "ORM Reflection: " << duration.count() << " microseconds\n";
    std::cout << "SQL generations per second: " << (iterations * 1000000.0) / duration.count() << "\n";
}

int main() {
    benchmark_orm_reflection();
    return 0;
}
