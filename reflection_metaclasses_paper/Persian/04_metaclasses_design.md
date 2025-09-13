# 4. متاکلاس‌ها: طراحی و پیاده‌سازی

## 4.1 مفهوم و انگیزه متاکلاس

### 4.1.1 چشم‌انداز برنامه‌نویسی تولیدی

متاکلاس‌ها نشان‌دهنده اوج دهه‌ها تحقیق در برنامه‌نویسی تولیدی و سنتز کد زمان کامپایل هستند [77]. در حالی که بازتاب توانایی درونگری ساختارهای کد موجود را فراهم می‌کند، متاکلاس‌ها **تولید** کد جدید بر اساس الگوها، محدودیت‌ها و الزامات خاص دامنه را امکان‌پذیر می‌سازند.

بینش بنیادی پشت متاکلاس‌ها این است که بسیاری از الگوهای برنامه‌نویسی شامل کد تکراری و غیرضروری هستند که از الگوهای قابل پیش‌بینی پیروی می‌کنند [78]. سناریوهای رایج را در نظر بگیرید:

- **پیاده‌سازی خصوصیت**: تولید خودکار getter ها، setter ها و منطق اعتبارسنجی
- **سریال‌سازی**: تبدیل خودکار به/از فرمت‌های JSON، XML یا باینری
- **الگوی Observer**: مکانیزم‌های اطلاع‌رسانی خودکار برای تغییرات وضعیت
- **نگاشت پایگاه داده**: نگاشت سبک ORM بین آبجکت‌ها و طرحواره‌های پایگاه داده
- **پیاده‌سازی رابط**: تولید خودکار delegation و پراکسی

رویکردهای سنتی به این مسائل شامل یا کدنویسی دستی گسترده یا متابرنامه‌نویسی قالب پیچیده است. متاکلاس‌ها گزینه سومی ارائه می‌دهند: **مشخصه اعلانی** رفتار مطلوب با تولید خودکار پیاده‌سازی [79].

### 4.1.2 فلسفه و اصول طراحی

طراحی متاکلاس C++23 از چندین اصل کلیدی پیروی می‌کند [80]:

**قصد اعلانی**: متاکلاس‌ها به توسعه‌دهندگان اجازه می‌دهند بیان کنند *چه* می‌خواهند به جای *چگونه* پیاده‌سازی کنند:

```cpp
// مشخصه اعلانی
class $serializable $observable Person {
    std::string name;
    int age;
    double salary;
};

// به طور خودکار تولید می‌کند:
// - متدهای to_json() / from_json()
// - ثبت/اطلاع‌رسانی Observer
// - دسترسی‌کننده‌های خصوصیت با اعتبارسنجی
// - عملگرهای برابری و مقایسه
```

**قابلیت ترکیب**: چندین متاکلاس می‌توانند به یک نوع اعمال شوند، با معناشناسی ترکیب به خوبی تعریف شده:

```cpp
class $entity("users") $auditable $cacheable User {
    // ترکیب نگاشت پایگاه داده، لاگ حسابرسی و کش
};
```

**ایمنی نوع**: تمام تبدیل‌های متاکلاس در زمان کامپایل نوع-بررسی و اعتبارسنجی می‌شوند و از خطاهای زمان اجرا رایج در رویکردهای تولید کد جلوگیری می‌کنند.

**سربار صفر زمان اجرا**: کد تولید شده از نظر ویژگی‌های عملکرد قابل تشخیص از کد دست‌نویس نیست.

### 4.1.3 رابطه با بازتاب

متاکلاس‌ها به طور بنیادی بر زیرساخت بازتاب توضیح داده شده در بخش 3 بنا می‌شوند. رابطه هم‌زیست است [81]:

```cpp
constexpr void serializable(std::meta::info target) {
    // پیاده‌سازی متاکلاس از بازتاب برای تحلیل نوع هدف استفاده می‌کند
    std::meta::compiler.require(std::meta::is_class(target), 
                               "serializable can only be applied to classes");
    
    // تکرار روی اعضای داده با استفاده از بازتاب
    for (auto member : std::meta::data_members_of(target)) {
        generate_serialization_code(member);
    }
    
    // تولید متدها بر اساس ساختار نوع
    std::meta::compiler.declare(target, generate_to_json_method(target));
    std::meta::compiler.declare(target, generate_from_json_method(target));
}
```

## 4.2 نحو تعریف متاکلاس

### 4.2.1 اعلان پایه متاکلاس

متاکلاس‌ها به عنوان توابع constexpr تعریف می‌شوند که روی آبجکت‌های `std::meta::info` نمایش‌دهنده نوع هدف عمل می‌کنند [82]:

```cpp
#include <experimental/meta>

constexpr void property(std::meta::info target) {
    // اعتبارسنجی که target یک کلاس است
    std::meta::compiler.require(std::meta::is_class(target),
                               "property metaclass requires a class");
    
    // تولید پیاده‌سازی خصوصیت
    for (auto member : std::meta::data_members_of(target)) {
        if (std::meta::is_private(member)) {
            generate_property_accessors(target, member);
        }
    }
}

// استفاده
class $property Person {
private:
    std::string name_;  // تولید getName()، setName()
    int age_;          // تولید getAge()، setAge()
};
```

### 4.2.2 متاکلاس‌های پارامتری

متاکلاس‌ها می‌توانند پارامترهایی برای شخصی‌سازی رفتار خود بپذیرند [83]:

```cpp
constexpr void entity(std::meta::info target, 
                     std::string_view table_name = "",
                     bool generate_crud = true) {
    auto actual_table = table_name.empty() ? 
        std::meta::get_name_v<target> : table_name;
    
    // تولید نگاشت جدول
    generate_table_mapping(target, actual_table);
    
    if (generate_crud) {
        generate_crud_operations(target);
    }
}

// استفاده با پارامترها
class $entity("user_accounts", true) User {
    int id;
    std::string username;
    std::string email;
};
```

### 4.2.3 اعمال شرطی متاکلاس

متاکلاس‌ها می‌توانند منطق شرطی بر اساس ویژگی‌های نوع شامل شوند [84]:

```cpp
constexpr void smart_serializable(std::meta::info target) {
    // استراتژی‌های مختلف بر اساس پیچیدگی نوع
    auto members = std::meta::data_members_of(target);
    
    if (std::meta::get_size_v<members> <= 5 && all_pod_members(members)) {
        generate_binary_serialization(target);
    } else if (has_string_members(members)) {
        generate_json_serialization(target);
    } else {
        generate_xml_serialization(target);
    }
    
    // همیشه اعتبارسنجی تولید کن
    generate_validation_methods(target);
}
```

## 4.3 مکانیزم‌های تولید کد

### 4.3.1 رابط کامپایلر

رابط `std::meta::compiler` مکانیزم اصلی برای تولید کد فراهم می‌کند [85]. این رابط به متاکلاس‌ها اجازه تزریق اعلان‌های جدید به نوع هدف را می‌دهد:

```cpp
namespace std::meta {
    struct compiler_interface {
        // تزریق یک تابع عضو جدید
        static constexpr void declare(info target, std::string_view code);
        
        // تزریق یک عضو داده جدید
        static constexpr void declare_member(info target, info type, 
                                           std::string_view name);
        
        // الزام یک شرط (assertion زمان کامپایل)
        static constexpr void require(bool condition, std::string_view message);
        
        // تولید پیام‌های تشخیصی
        static constexpr void warn(std::string_view message);
        static constexpr void error(std::string_view message);
    };
}
```

### 4.3.2 تولید کد مبتنی بر قالب

متاکلاس‌ها اغلب از تکنیک‌های قالب برای تولید کد ایمن نوع استفاده می‌کنند [86]:

```cpp
constexpr void comparable(std::meta::info target) {
    // تولید عملگرهای مقایسه بر اساس ساختار عضو
    std::string equality_impl = R"(
        bool operator==(const )" + std::meta::get_name_v<target> + R"(& other) const {
            return true)";
    
    for (auto member : std::meta::data_members_of(target)) {
        auto member_name = std::meta::get_name_v<member>;
        equality_impl += " && (" + member_name + " == other." + member_name + ")";
    }
    
    equality_impl += R"(;
        }
        
        bool operator!=(const )" + std::meta::get_name_v<target> + R"(& other) const {
            return !(*this == other);
        }
        
        auto operator<=>(const )" + std::meta::get_name_v<target> + R"(& other) const {
            // مقایسه سه‌طرفه با استفاده از std::tie
            return std::tie()";
    
    bool first = true;
    for (auto member : std::meta::data_members_of(target)) {
        if (!first) equality_impl += ", ";
        equality_impl += std::meta::get_name_v<member>;
        first = false;
    }
    
    equality_impl += R"() <=> std::tie()";
    
    first = true;
    for (auto member : std::meta::data_members_of(target)) {
        if (!first) equality_impl += ", ";
        equality_impl += "other." + std::meta::get_name_v<member>;
        first = false;
    }
    
    equality_impl += ");";
    equality_impl += "\n}";
    
    std::meta::compiler.declare(target, equality_impl);
}
```

### 4.3.3 الگوهای پیشرفته سنتز کد

متاکلاس‌های پیچیده ممکن است نیاز به استراتژی‌های پیچیده تولید کد داشته باشند [87]:

```cpp
constexpr void state_machine(std::meta::info target, 
                           std::span<const state_transition> transitions) {
    // اعتبارسنجی تعریف ماشین حالت
    validate_state_machine(target, transitions);
    
    // تولید شمارش حالت
    generate_state_enum(target, transitions);
    
    // تولید جدول انتقال
    generate_transition_table(target, transitions);
    
    // تولید متدهای ماشین حالت
    std::string machine_impl = R"(
    private:
        State current_state_ = State::)" + get_initial_state(transitions) + R"(;
        
    public:
        State get_state() const { return current_state_; }
        
        template<typename Event>
        bool process_event(const Event& event) {
            auto new_state = transition_table_.find({current_state_, typeid(Event)});
            if (new_state != transition_table_.end()) {
                auto old_state = current_state_;
                current_state_ = new_state->second;
                on_state_change(old_state, current_state_, event);
                return true;
            }
            return false;
        }
        
    protected:
        virtual void on_state_change(State from, State to, const auto& event) {}
    )";
    
    std::meta::compiler.declare(target, machine_impl);
}
```

## 4.4 الگوهای پیشرفته متاکلاس

### 4.4.1 تولید و پیاده‌سازی رابط

متاکلاس‌ها می‌توانند پیاده‌سازی‌های رابط را بر اساس الگوها به طور خودکار تولید کنند [88]:

```cpp
constexpr void rest_api(std::meta::info target, std::string_view base_path) {
    // تولید endpoint های REST API بر اساس متدهای عمومی
    for (auto method : std::meta::member_functions_of(target)) {
        if (std::meta::is_public(method)) {
            auto method_name = std::meta::get_name_v<method>;
            auto return_type = std::meta::get_return_type_t<method>;
            auto parameters = std::meta::get_parameters_t<method>;
            
            if (method_name.starts_with("get")) {
                generate_get_endpoint(target, method, base_path);
            } else if (method_name.starts_with("create") || method_name.starts_with("add")) {
                generate_post_endpoint(target, method, base_path);
            } else if (method_name.starts_with("update")) {
                generate_put_endpoint(target, method, base_path);
            } else if (method_name.starts_with("delete") || method_name.starts_with("remove")) {
                generate_delete_endpoint(target, method, base_path);
            }
        }
    }
    
    // تولید جدول مسیریابی
    generate_routing_table(target, base_path);
}

class $rest_api("/api/users") UserService {
public:
    User getUser(int id);           // تولید GET /api/users/{id}
    User createUser(const User&);   // تولید POST /api/users
    void updateUser(int id, const User&);  // تولید PUT /api/users/{id}
    void deleteUser(int id);        // تولید DELETE /api/users/{id}
};
```

### 4.4.2 تولید چارچوب سریال‌سازی

متاکلاس‌های سریال‌سازی پیشرفته می‌توانند سناریوهای پیچیده را مدیریت کنند [89]:

```cpp
constexpr void serializable(std::meta::info target,
                          serialization_format format = json,
                          naming_convention naming = snake_case) {
    // تولید سریال‌سازی خاص فرمت
    switch (format) {
        case json:
            generate_json_serialization(target, naming);
            break;
        case xml:
            generate_xml_serialization(target, naming);
            break;
        case binary:
            generate_binary_serialization(target);
            break;
        case protobuf:
            generate_protobuf_serialization(target, naming);
            break;
    }
    
    // تولید اعتبارسنجی طرحواره
    generate_schema_validation(target, format);
    
    // تولید پشتیبانی نسخه‌بندی
    generate_version_handling(target, format);
}

// مثال سریال‌سازی پیچیده
class $serializable(json, snake_case) $versioned(2) Person {
    std::string full_name;          // سریال‌سازی به عنوان "full_name"
    std::optional<int> age;         // مدیریت فیلد اختیاری
    std::vector<std::string> tags;  // سریال‌سازی آرایه
    
    // طرحواره خودکار: {"full_name": "string", "age": "int?", "tags": ["string"]}
    // مدیریت نسخه: مهاجرت خودکار از v1 به v2
};
```

### 4.4.3 ORM و یکپارچگی پایگاه داده

متاکلاس‌های جهت‌گیری پایگاه داده تولید کد پیچیده را نشان می‌دهند [90]:

```cpp
constexpr void entity(std::meta::info target,
                     std::string_view table_name,
                     database_dialect dialect = postgresql) {
    // تولید طرحواره جدول
    generate_create_table_sql(target, table_name, dialect);
    
    // تولید عملیات CRUD
    generate_find_methods(target, table_name, dialect);
    generate_save_method(target, table_name, dialect);
    generate_delete_method(target, table_name, dialect);
    
    // تولید متدهای query builder
    for (auto member : std::meta::data_members_of(target)) {
        if (std::meta::has_attribute<indexed>(member)) {
            generate_find_by_method(target, member, table_name, dialect);
        }
    }
    
    // تولید مدیریت رابطه
    generate_relationship_methods(target, table_name, dialect);
}

class $entity("users", postgresql) User {
    $primary_key int id;
    $indexed $unique std::string email;
    std::string name;
    $nullable std::optional<std::string> bio;
    
    $one_to_many("user_id") std::vector<Post> posts;
    $many_to_one Profile profile;
    
    // تولید می‌کند:
    // static User find(int id);
    // static std::vector<User> find_by_email(const std::string& email);
    // static std::vector<User> find_all();
    // void save();
    // void delete();
    // std::vector<Post> get_posts();
    // Profile get_profile();
};
```

### 4.4.4 اتوماسیون الگوی طراحی

متاکلاس‌ها می‌توانند الگوهای طراحی پیچیده را به طور خودکار پیاده‌سازی کنند [91]:

```cpp
constexpr void observer(std::meta::info target) {
    // تولید زیرساخت observer
    std::string observer_code = R"(
    private:
        mutable std::vector<std::function<void(const std::string&)>> observers_;
        
    public:
        void add_observer(std::function<void(const std::string&)> observer) {
            observers_.push_back(std::move(observer));
        }
        
        void remove_observer(const std::function<void(const std::string&)>& observer) {
            // پیاده‌سازی برای حذف observer
        }
        
    protected:
        void notify_observers(const std::string& property_name) const {
            for (const auto& observer : observers_) {
                observer(property_name);
            }
        }
    )";
    
    std::meta::compiler.declare(target, observer_code);
    
    // تغییر تمام setter ها برای شامل اطلاع‌رسانی
    for (auto member : std::meta::data_members_of(target)) {
        generate_notifying_setter(target, member);
    }
}

constexpr void visitor(std::meta::info target) {
    // تولید الگوی visitor برای سلسله‌مراتب
    std::meta::compiler.require(std::meta::is_polymorphic_v<target>,
                               "visitor requires polymorphic type");
    
    auto derived_types = std::meta::get_derived_types_t<target>;
    
    // تولید رابط visitor
    generate_visitor_interface(target, derived_types);
    
    // تولید متدهای accept
    generate_accept_methods(target, derived_types);
    
    // تولید کلاس پایه visitor مشخص
    generate_visitor_base(target, derived_types);
}
```

## 4.5 ترکیب و تعامل متاکلاس

### 4.5.1 معناشناسی ترکیب

زمانی که چندین متاکلاس به یک نوع اعمال می‌شوند، اثرات آن‌ها باید به شیوه‌ای قابل پیش‌بینی ترکیب شوند [92]:

```cpp
class $serializable $observable $entity("products") Product {
    // ترتیب ترکیب: serializable → observable → entity
    // هر متاکلاس می‌تواند اثرات قبلی‌ها را ببیند
};

// تضادهای ترکیب در زمان کامپایل شناسایی می‌شوند
class $immutable $observable BadExample {
    // خطا: immutable با observable متضاد است (نیاز به setter ها)
};
```

### 4.5.2 ارتباط بین متاکلاس‌ها

متاکلاس‌ها می‌توانند از طریق فراداده مشترک و قراردادها ارتباط برقرار کنند [93]:

```cpp
constexpr void auditable(std::meta::info target) {
    // بررسی اگر متاکلاس entity اعمال شده
    if (std::meta::has_generated_method(target, "save")) {
        // بهبود متد save با لاگ حسابرسی
        enhance_save_with_audit(target);
    } else {
        // تولید زیرساخت حسابرسی مستقل
        generate_audit_infrastructure(target);
    }
}

constexpr void cacheable(std::meta::info target) {
    // یکپارچگی با entity یا ایجاد کش مستقل
    if (std::meta::has_attribute<entity_table>(target)) {
        generate_database_cache(target);
    } else {
        generate_memory_cache(target);
    }
}
```

### 4.5.3 وابستگی‌ها و ترتیب متاکلاس

تعاملات پیچیده متاکلاس نیاز به مدیریت صریح وابستگی دارند [94]:

```cpp
// متاکلاس با وابستگی‌های صریح
constexpr void enhanced_entity(std::meta::info target) {
    // اطمینان از حضور متاکلاس‌های مورد نیاز
    std::meta::compiler.require(
        std::meta::has_metaclass<serializable>(target),
        "enhanced_entity requires serializable metaclass"
    );
    
    // بنا بر عملکرد serializable
    enhance_with_database_features(target);
}

// اعلان وابستگی
class $serializable $enhanced_entity Product {
    // ترتیب خودکار: serializable ابتدا اعمال می‌شود
};
```

## 4.6 مدیریت خطا و تشخیص

### 4.6.1 اعتبارسنجی زمان کامپایل

متاکلاس‌ها اعتبارسنجی گسترده زمان کامپایل برای شناسایی زودهنگام خطاها فراهم می‌کنند [95]:

```cpp
constexpr void validated_entity(std::meta::info target) {
    // اعتبارسنجی جامع
    std::meta::compiler.require(std::meta::is_class(target),
                               "entity can only be applied to classes");
    
    auto members = std::meta::data_members_of(target);
    
    // اعتبارسنجی حضور کلید اصلی
    bool has_primary_key = false;
    for (auto member : members) {
        if (std::meta::has_attribute<primary_key>(member)) {
            has_primary_key = true;
            validate_primary_key_type(member);
        }
    }
    
    std::meta::compiler.require(has_primary_key,
                               "entity requires a primary key field");
    
    // اعتبارسنجی انواع عضو قابل سریال‌سازی هستند
    for (auto member : members) {
        validate_member_serializable(member);
    }
}
```

### 4.6.2 تولید پیام تشخیصی

متاکلاس‌های خوب طراحی شده پیام‌های تشخیصی مفید ارائه می‌دهند [96]:

```cpp
constexpr void helpful_serializable(std::meta::info target) {
    for (auto member : std::meta::data_members_of(target)) {
        auto member_type = std::meta::get_type_t<member>;
        
        if (!is_serializable_type(member_type)) {
            std::string message = "Member '" + 
                std::meta::get_name_v<member> + 
                "' of type '" + 
                std::meta::get_display_name_v<member_type> + 
                "' is not serializable. Consider:\n" +
                "  - Adding serializable metaclass to the type\n" +
                "  - Providing custom serialization functions\n" +
                "  - Marking the member as transient";
            
            std::meta::compiler.error(message);
        }
    }
}
```

سیستم متاکلاس نشان‌دهنده تکامل قدرتمندی در برنامه‌نویسی تولیدی C++ است که مشخصه اعلانی رفتارهای پیچیده را در حین حفظ ایمنی نوع و عملکرد امکان‌پذیر می‌سازد. بخش بعدی تأثیرات عملکردی این رویکرد را از طریق ارزیابی و تحلیل جامع عملکرد بررسی می‌کند.

---

*[مراجع 77-96 مطابق با تئوری برنامه‌نویسی تولیدی، مطالعات پیاده‌سازی متاکلاس و تحقیق اتوماسیون الگوی طراحی فهرست شده در کتابشناسی جامع ما]*
