# 3. چارچوب بازتاب C++23

## 3.1 مفاهیم اصلی بازتاب

### 3.1.1 پروتکل متا-آبجکت

بازتاب C++23 بر اساس یک پروتکل متا-آبجکت پیچیده ساخته شده که دسترسی زمان کامپایل به اطلاعات ساختار برنامه فراهم می‌کند [57]. در هسته آن، سیستم بازتاب مفهوم **متا-آبجکت‌ها** را معرفی می‌کند - نمایش‌های زمان کامپایل ساختارهای زبان مانند انواع، توابع، متغیرها و namespace ها.

بلوک ساختمانی بنیادی `std::meta::info` است، یک نوع handle مبهم که موجودیت‌های بازتاب شده را نمایش می‌دهد:

```cpp
#include <experimental/reflect>
using namespace std::experimental::reflect;

struct Person {
    std::string name;
    int age;
    void greet() const;
};

// به دست آوردن متا-آبجکت برای نوع Person
constexpr auto person_meta = reflexpr(Person);
static_assert(std::is_same_v<decltype(person_meta), const std::meta::info>);
```

برخلاف سیستم‌های بازتاب زمان اجرا، این متا-آبجکت‌ها فقط در زمان کامپایل وجود دارند و سربار صفر زمان اجرا را تضمین می‌کنند [58]. سیستم نوع اطمینان می‌دهد که عملیات نامعتبر در زمان کامپایل به جای زمان اجرا شناسایی می‌شوند.

### 3.1.2 کوئری‌ها و عملیات بازتاب

API بازتاب مجموعه غنی از توابع کوئری ارائه می‌دهد که روی متا-آبجکت‌ها عمل می‌کنند تا اطلاعاتی درباره موجودیت‌های بازتاب شده استخراج کنند. این کوئری‌ها از الگوی نام‌گذاری سازگار پیروی می‌کنند و یا مقادیر constexpr یا متا-آبجکت‌های اضافی برمی‌گردانند:

```cpp
// کوئری‌های اطلاعات نوع اولیه
constexpr bool is_class_type = is_class_v<person_meta>;
constexpr auto type_name = get_name_v<person_meta>;
constexpr size_t type_size = get_size_v<person_meta>;

// کوئری‌های دسترسی عضو
constexpr auto data_members = get_data_members_t<person_meta>{};
constexpr auto member_functions = get_member_functions_t<person_meta>{};
constexpr auto constructors = get_constructors_t<person_meta>{};

// کوئری‌های رابطه
constexpr auto base_classes = get_base_classes_t<person_meta>{};
constexpr bool is_polymorphic = is_polymorphic_v<person_meta>;
```

### 3.1.3 سکانس‌های متا-آبجکت

یکی از قدرتمندترین جنبه‌های بازتاب C++23 برخورد آن با مجموعه‌های موجودیت‌های مرتبط است. به جای برگرداندن کانتینرهای سنتی، کوئری‌های بازتاب **سکانس‌های متا-آبجکت** برمی‌گردانند - سکانس‌های زمان کامپایل که می‌توانند با استفاده از گسترش template parameter pack پردازش شوند [59]:

```cpp
template<typename T>
void print_member_info() {
    constexpr auto meta_type = reflexpr(T);
    constexpr auto members = get_data_members_t<meta_type>{};
    
    // تکرار روی اعضا با استفاده از fold expressions (C++17)
    []<auto... Ms>(std::index_sequence<Ms...>) {
        ((std::cout << "Member " << Ms << ": " 
                   << get_name_v<get_element_v<Ms, decltype(members)>> 
                   << " (type: " 
                   << get_display_name_v<get_type_t<get_element_v<Ms, decltype(members)>>> 
                   << ")\n"), ...);
    }(std::make_index_sequence<get_size_v<members>>{});
}
```

این رویکرد تکرار کارآمد زمان کامپایل بدون سربار مرتبط با کانتینرهای زمان اجرا یا بازگشت پیچیده قالب را امکان‌پذیر می‌کند [60].

## 3.2 اصول طراحی API بازتاب

### 3.2.1 ایمنی نوع و تأیید زمان کامپایل

API بازتاب C++23 ایمنی نوع را از طریق بررسی قوی زمان کامپایل اولویت می‌دهد. تمام عملیات بازتاب در طول کامپایل اعتبارسنجی می‌شوند و از خطاهای زمان اجرا رایج در سیستم‌های بازتاب نوع پویا جلوگیری می‌کنند [61]:

```cpp
template<std::meta::info Member>
constexpr auto get_member_value(const auto& obj) 
    requires std::meta::is_data_member(Member) {
    // تأیید زمان کامپایل اطمینان می‌دهد Member واقعاً یک data member است
    return obj.*(std::meta::get_pointer_v<Member>);
}

// استفاده با ایمنی زمان کامپایل
struct Point { int x, y; };
constexpr auto point_meta = reflexpr(Point);
constexpr auto x_member = get_element_v<0, get_data_members_t<point_meta>>;

Point p{10, 20};
auto x_value = get_member_value<x_member>(p);  // دسترسی ایمن نوع
```

### 3.2.2 یکپارچگی با ویژگی‌های موجود زبان

سیستم بازتاب برای یکپارچگی یکپارچه با ویژگی‌های موجود C++، به ویژه قالب‌ها و کانسپت‌ها طراحی شده است [62]. این یکپارچگی الگوهای ترکیب قدرتمند را امکان‌پذیر می‌کند:

```cpp
template<typename T>
concept Reflectable = requires {
    reflexpr(T);
    typename get_data_members_t<reflexpr(T)>;
};

template<Reflectable T>
std::string to_json(const T& obj) {
    // سریال‌سازی مبتنی بر بازتاب با محدودیت‌های کانسپت
    return detail::serialize_impl(obj, reflexpr(T));
}
```

### 3.2.3 طراحی عملکرد-محور

هر جنبه از API بازتاب برای به حداقل رساندن سربار کامپایل و تضمین هزینه صفر زمان اجرا طراحی شده است [63]. استفاده از ارزیابی constexpr و گسترش template parameter pack نیاز به dispatch زمان اجرا یا فراخوانی‌های تابع مجازی را حذف می‌کند:

```cpp
// بازتاب سنتی زمان اجرا (سبک جاوا)
// Object field = obj.getClass().getField("name");
// String value = (String) field.get(obj);  // Dispatch زمان اجرا

// بازتاب زمان کامپایل C++23
template<auto Member>
constexpr auto get_field_value(const auto& obj) {
    return obj.*(get_pointer_v<Member>);  // دسترسی مستقیم حافظه
}
```

## 3.3 یکپارچگی با سیستم قالب موجود

### 3.3.1 بهبود استنتاج پارامتر قالب

بازتاب استنتاج پارامتر قالب را با ارائه دسترسی مستقیم به ساختار نوع بهبود می‌بخشد و نیاز به ساختارهای پیچیده SFINAE را حذف می‌کند [64]:

```cpp
// رویکرد سنتی SFINAE
template<typename T>
auto serialize_impl(const T& obj) 
    -> std::enable_if_t<
        std::conjunction_v<
            std::is_default_constructible<T>,
            std::is_copy_constructible<T>,
            has_member_serialize<T>
        >, 
        std::string> {
    // منطق استنتاج پیچیده
}

// رویکرد مبتنی بر بازتاب
template<typename T>
std::string serialize(const T& obj) 
    requires requires { reflexpr(T); } {
    // تحلیل مستقیم نوع بدون ماشین‌آلات پیچیده قالب
    constexpr auto members = get_data_members_t<reflexpr(T)>{};
    return serialize_members(obj, members);
}
```

### 3.3.2 بهبود قالب Variadic

بازتاب به خوبی با قالب‌های variadic کار می‌کند و الگوهای قدرتمند برنامه‌نویسی عمومی را امکان‌پذیر می‌سازد [65]:

```cpp
template<typename... Types>
class variant_serializer {
    template<typename T>
    static std::string serialize_variant(const std::variant<Types...>& var) {
        if (std::holds_alternative<T>(var)) {
            return serialize_reflected_type(std::get<T>(var));
        }
        return serialize_next_type</* next type */>(var);
    }
    
    template<typename T>
    static std::string serialize_reflected_type(const T& obj) {
        constexpr auto meta = reflexpr(T);
        // استفاده از بازتاب برای سریال‌سازی بدون تخصص‌یابی صریح
        return reflect_serialize(obj, meta);
    }
};
```

### 3.3.3 کاهش تخصص‌یابی قالب

یکی از مهم‌ترین مزایای بازتاب کاهش چشمگیر تخصص‌یابی‌های قالب مورد نیاز است [66]. یک type trait را در نظر بگیرید که تشخیص می‌دهد آیا نوعی عضو خاصی دارد:

```cpp
// رویکرد سنتی: نیاز به تخصص‌یابی صریح یا SFINAE پیچیده
template<typename T, typename = void>
struct has_to_string : std::false_type {};

template<typename T>
struct has_to_string<T, std::void_t<decltype(std::declval<T>().to_string())>>
    : std::true_type {};

// رویکرد بازتاب: پیاده‌سازی عمومی واحد
template<typename T>
constexpr bool has_to_string_v = []() {
    constexpr auto meta = reflexpr(T);
    constexpr auto functions = get_member_functions_t<meta>{};
    
    return []<auto... Fs>(std::index_sequence<Fs...>) {
        return ((get_name_v<get_element_v<Fs, decltype(functions)>> == "to_string") || ...);
    }(std::make_index_sequence<get_size_v<functions>>{});
}();
```

## 3.4 تحلیل نحوی و معنایی

### 3.4.1 عملگر reflexpr

عملگر `reflexpr` به عنوان نقطه ورود اصلی به سیستم بازتاب عمل می‌کند [67]. انواع مختلف ساختارهای زبان را می‌پذیرد و متا-آبجکت‌های مربوطه را برمی‌گرداند:

```cpp
// بازتاب نوع
constexpr auto type_meta = reflexpr(int);
constexpr auto class_meta = reflexpr(std::string);

// بازتاب namespace
constexpr auto std_meta = reflexpr(std);

// بازتاب متغیر
int global_var = 42;
constexpr auto var_meta = reflexpr(global_var);

// بازتاب تابع
void my_function(int, double);
constexpr auto func_meta = reflexpr(my_function);
```

عملگر اعتبارسنجی زمان کامپایل انجام می‌دهد تا اطمینان حاصل کند که آرگومان ارائه شده یک هدف بازتاب معتبر است [68].

### 3.4.2 پروتکل‌های متا-آبجکت

سیستم بازتاب چندین دسته از متا-آبجکت‌ها را تعریف می‌کند، هر کدام با رابط‌های کوئری خاص [69]:

**متا-آبجکت‌های نوع:**
```cpp
template<std::meta::info TypeMeta>
    requires std::meta::is_type(TypeMeta)
class type_analyzer {
    static constexpr bool is_fundamental = std::meta::is_fundamental_v<TypeMeta>;
    static constexpr bool is_class = std::meta::is_class_v<TypeMeta>;
    static constexpr auto name = std::meta::get_name_v<TypeMeta>;
    static constexpr auto size = std::meta::get_size_v<TypeMeta>;
};
```

**متا-آبجکت‌های عضو:**
```cpp
template<std::meta::info MemberMeta>
    requires std::meta::is_data_member(MemberMeta)
class member_analyzer {
    static constexpr auto name = std::meta::get_name_v<MemberMeta>;
    static constexpr auto type = std::meta::get_type_t<MemberMeta>;
    static constexpr auto offset = std::meta::get_offset_v<MemberMeta>;
    static constexpr bool is_public = std::meta::is_public_v<MemberMeta>;
};
```

### 3.4.3 زمینه ارزیابی Constexpr

تمام عملیات بازتاب در زمینه‌های ارزیابی constexpr رخ می‌دهند و اجرای زمان کامپایل را تضمین می‌کنند [70]. این الزام چندین تصمیم طراحی را هدایت می‌کند:

```cpp
template<typename T>
constexpr auto analyze_type() {
    constexpr auto meta = reflexpr(T);
    
    // تمام کوئری‌های بازتاب باید constexpr باشند
    constexpr auto member_count = get_size_v<get_data_members_t<meta>>;
    constexpr auto is_trivial = is_trivially_copyable_v<meta>;
    
    struct analysis_result {
        size_t members;
        bool trivial;
        std::string_view name;
    };
    
    return analysis_result{
        .members = member_count,
        .trivial = is_trivial,
        .name = get_name_v<meta>
    };
}

// استفاده در زمان کامپایل
constexpr auto person_analysis = analyze_type<Person>();
static_assert(person_analysis.members > 0);
```

## 3.5 الگوهای پیشرفته بازتاب

### 3.5.1 کامپایل شرطی بر اساس ساختار نوع

بازتاب کامپایل شرطی پیچیده بر اساس ساختار واقعی نوع به جای تخصص‌یابی‌های شکننده قالب را امکان‌پذیر می‌کند [71]:

```cpp
template<typename T>
auto serialize(const T& obj) {
    constexpr auto meta = reflexpr(T);
    
    if constexpr (has_custom_serializer_v<T>) {
        return obj.serialize();
    } else if constexpr (is_container_v<meta>) {
        return serialize_container(obj, meta);
    } else if constexpr (is_arithmetic_v<meta>) {
        return serialize_arithmetic(obj);
    } else {
        return serialize_aggregate(obj, meta);
    }
}
```

### 3.5.2 تطبیق نوع و تولید پراکسی

بازتاب تولید خودکار کلاس‌های آداپتور و پراکسی را تسهیل می‌کند [72]:

```cpp
template<typename Interface>
class reflection_proxy {
    std::any target_;
    
public:
    template<typename Implementation>
    reflection_proxy(Implementation&& impl) : target_(std::forward<Implementation>(impl)) {}
    
    // تولید خودکار توابع forwarding برای تمام متدهای رابط
    template<auto Method>
        requires std::meta::is_member_function(Method)
    auto invoke(auto&&... args) {
        constexpr auto method_name = get_name_v<Method>;
        constexpr auto return_type = get_return_type_t<Method>;
        
        // استفاده از بازتاب برای یافتن و فراخوانی متد مربوطه روی target
        return invoke_by_name<method_name>(std::any_cast<auto&>(target_), 
                                         std::forward<decltype(args)>(args)...);
    }
};
```

### 3.5.3 پیاده‌سازی الگوی طراحی زمان کامپایل

بازتاب پیاده‌سازی خودکار الگوهای طراحی رایج را امکان‌پذیر می‌کند [73]:

```cpp
template<typename T>
class auto_visitor {
    // تولید پیاده‌سازی الگوی visitor بر اساس سلسله‌مراتب نوع
    static_assert(std::meta::is_polymorphic_v<reflexpr(T)>);
    
    template<typename Visitor>
    static auto visit(const T& obj, Visitor&& visitor) {
        constexpr auto derived_types = get_derived_types_t<reflexpr(T)>{};
        
        return visit_impl(obj, std::forward<Visitor>(visitor), derived_types);
    }
    
private:
    template<typename Visitor, auto... DerivedMetas>
    static auto visit_impl(const T& obj, Visitor&& visitor, 
                          std::index_sequence<DerivedMetas...>) {
        // تولید dispatch پویای ایمن نوع با استفاده از typeid
        const std::type_info& runtime_type = typeid(obj);
        
        auto result = std::optional<decltype(visitor(std::declval<T>()))>{};
        
        ((runtime_type == typeid(get_reflected_type_t<DerivedMetas>) ?
          (result = visitor(static_cast<const get_reflected_type_t<DerivedMetas>&>(obj)), true) :
          false) || ...);
          
        return *result;
    }
};
```

## 3.6 ملاحظات پیاده‌سازی کامپایلر

### 3.6.1 یکپارچگی فاز کامپایل

بازتاب C++23 نیاز به یکپارچگی دقیق با خط لوله کامپایل دارد [74]. متا-آبجکت‌ها باید در طول نمونه‌سازی قالب در دسترس باشند در حالی که اصول کامپایل جداگانه را حفظ کنند:

```cpp
// کامپایلر باید وابستگی‌های متا-آبجکت را ردیابی کند
template<typename T>
constexpr auto get_serialization_info() {
    constexpr auto meta = reflexpr(T);  // وابستگی به تعریف کامل T
    
    return analyze_serialization_requirements(meta);  // باید برای نمونه‌سازی در دسترس باشد
}

// استفاده در واحد ترجمه جداگانه
extern template auto get_serialization_info<MyClass>();  // پشتیبانی اعلان forward
```

### 3.6.2 اطلاعات دیباگ و یکپارچگی ابزار

متا-آبجکت‌های بازتاب باید با ابزارهای دیباگ و توسعه یکپارچه شوند [75]:

```cpp
template<typename T>
void debug_print_type_info() {
    constexpr auto meta = reflexpr(T);
    
    // بیلدهای دیباگ باید اطلاعات بازتاب را حفظ کنند
    // برای یکپارچگی IDE و ابزارهای دیباگ
    if constexpr (std::meta::is_debug_build()) {
        emit_debug_info(meta);
    }
}
```

### 3.6.3 فرصت‌های بهینه‌سازی

کامپایلرها می‌توانند از اطلاعات بازتاب برای بهینه‌سازی‌های پیشرفته استفاده کنند [76]:

```cpp
template<typename T>
std::string fast_serialize(const T& obj) {
    constexpr auto meta = reflexpr(T);
    
    // کامپایلر می‌تواند بر اساس تحلیل نوع زمان کامپایل بهینه‌سازی کند
    if constexpr (is_pod_serializable_v<meta>) {
        // تولید سریال‌سازی مبتنی بر memcpy
        return serialize_pod(obj);
    } else {
        // تولید سریال‌سازی فیلد به فیلد
        return serialize_structured(obj, meta);
    }
}
```

این تحلیل نشان می‌دهد که بازتاب C++23 پایه‌ای جامع، ایمن نوع و کارآمد برای درونگری زمان کامپایل و تولید کد فراهم می‌کند. بخش بعدی بررسی می‌کند که چگونه متاکلاس‌ها بر این پایه بنا می‌شوند تا الگوهای برنامه‌نویسی تولیدی حتی قدرتمندتری را امکان‌پذیر سازند.

---

*[مراجع 57-76 مطابق با مشخصات فنی دقیق، مطالعات پیاده‌سازی کامپایلر و مقالات تحلیل عملکرد فهرست شده در کتابشناسی جامع ما]*
