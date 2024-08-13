# cpp_note
## C++ base
### 类型转换
在C++中，类型转换（Type Casting）是一种将一个数据类型的值转换为另一个数据类型的值的方法。C++支持多种类型转换方式，主要分为两大类：隐式转换（Implicit Conversion）和显式转换（Explicit Conversion）。下面详细介绍这两类转换以及C++中常用的几种显式转换操作符。
#### 隐式转换（Implicit Conversion）
隐式转换也称为自动类型转换，由编译器自动完成。通常在下列情况下发生：
- 从一个较小的数据类型转换到一个较大的数据类型，例如从int转换到double。
- 从一个派生类指针转换到基类指针。
#### 显式转换（Explicit Conversion）
**C风格转换（C-style Cast）**
```cpp
int i = 42;
double d = (double)i; // C风格转换，从int到double
```
**函数风格转换（Function-style Cast）**
```cpp
int i = 42;
double d = double(i); // 函数风格转换，从int到double
```
**C++标准转换操作符**
**`static_cast`**
`static_cast < type-id > (expression)`
该运算符把`expression`转换为`type-id`类型，但没有运行时类型检查来保证转换的安全性。它主要有如下几种用法：
- 用于类层次结构中基类（父类）和派生类（子类）之间指针或引用引用的转换
  - 进行上行转换（把派生类的指针或引用转换成基类表示）是安全的
  - 进行下行转换（把基类指针或引用转换成派生类表示）时，由于没有动态类型检查，所以是不安全的
- 用于基本数据类型之间的转换，如把int转换成char，把int转换成enum。这种转换的安全性也要开发人员来保证。
- 把空指针转换成目标类型的空指针
- 把任何类型的表达式转换成void类型
注意：static_cast不能转换掉expression的const、volatile、或者__unaligned属性。
```cpp
int i = 42;
double d = static_cast<double>(i); // 使用static_cast转换
```
**`dynamic_cast`**
主要用于将基类指针或引用安全地转换为派生类指针或引用，通常用于有多态的类层次结构中，转换失败时返回nullptr。
```cpp
class Base {
    virtual void foo() {}
};
class Derived : public Base {
    void foo() override {}
};

Base* b = new Derived();
Derived* d = dynamic_cast<Derived*>(b); // 使用dynamic_cast进行转换
```
**`const_cast`**
用于增加或移除const属性，但不能用于转换非指针或非引用类型。
```cpp
const int* p = &i;
int* q = const_cast<int*>(p); // 使用const_cast去除const属性
```
**`reinterpret_cast`**
用于在几乎所有类型之间进行低级别的位模式转换，这种转换非常危险，只有在非常特殊的情况下才应使用。
```cpp
int i = 42;
void* p = reinterpret_cast<void*>(&i); // 使用reinterpret_cast进行转换
```

## OOP
### 静态成员/静态方法 vs. 普通成员/普通方法
- 静态成员变量
  - 属于类而不是对象，可以用过类调用，不需要创建类的实例
  - 在类内声明，在类外定义和初始化。
  - 属于数据段。
- 普通成员方法
  - 编译器会添加this指针形参变量
  - 属于类的作用域
  - 调用该方法依赖于一个对象
  - 可以任意访问类的私有成员
- 静态成员方法
  - 编译不添加this形参
  - 属于类的作用域
  - 用类名作用域来调用静态成员方法
  - 可以任意访问**不依赖于对象**的成员（其他的静态成员）
### 常方法
- 生成的this是常指针，普通对象和常对象都可以调用。
- 常方法只能读不能写。
- 常对象不能调用普通方法。
## C++ 11
### 