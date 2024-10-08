# cpp_note
## 编译、动态库、静态库
### cpp 到 o 全过程
#### 1. 预处理阶段
```cpp
g++ -E test.cpp -o test.i
```
作用：
1. 删除注释
1. 预处理指令替换
1. 头文件展开
  
#### 2. 编译阶段
```cpp
g++ -S test.i -o test.s
```
作用：
1. 翻译成汇编语言
1. 检查代码报错？

#### 3. 汇编阶段
```cpp
g++ -c test.s -o test.o
```
作用：
1. 将 .s 文件，汇编成二进制文件（不能运行）
  
#### 4. 链接阶段
```cpp
g++ test.o -o test
```
作用：
1. 将目标文件 .o 和库文件链接

### 静态库
#### 制作和使用静态库
1. 首先，编写你想要包含在静态库中的C++源代码文件，并将其对应的头文件一并准备好。
1. 使用C++编译器（如 `g++`）将源文件编译为**对象文件**（`.o` 文件）。每个源文件都会生成一个对应的对象文件。
1. 使用`ar`工具将多个对象文件打包成一个**静态库文件**。静态库通常以 .a 作为扩展名。
1. 将生成的静态库文件（.a 文件）和相应的头文件（.h 文件）一起打包分发。头文件定义了外部程序可以调用的接口。
1. 在使用静态库的程序中，**包含相应的头文件**，以便编译器能够识别库中提供的函数和类。
1. 在编译外部程序时，需要使用静态库进行**链接**。编译时指定库的路径，并链接静态库。
1. 链接后生成的可执行文件已经包含了静态库中的代码，可以直接运行，无需依赖外部库文件。
``` bash
# 目标文件
g++ -c file1.cpp
g++ -c file2.cpp
# 制作静态库
ar rcs libmylibrary.a file1.o file2.o
# 包含头文件
# 链接静态库
g++ main.cpp -L/path/to/library -lmylibrary -o myprogram

```

#### 优点
- **独立性**：生成的可执行文件**包含了所有需要的代码**，运行时不依赖外部库文件，便于分发和部署。
- **运行效率**：**静态链接在编译阶段完成，运行时无需动态链接库**，因此程序启动速度快，运行时效率高。
- 版本稳定：一旦静态库编译进可执行文件，除非重新编译程序，否则不会受到库文件更新的影响，避免了因动态库更新而引入的不兼容问题。
#### 缺点
- 文件体积大：由于**每个使用静态库的可执行文件都包含了一份完整的库代码**，可能导致程序体积较大，尤其是当多个程序使用相同库时，这一问题尤为明显。
- **更新不便**：当静态库中的代码需要更新时，所有依赖该库的程序都必须重新编译，维护成本较高。
- **内存占用**：多个程序运行时，各自的内存中都包含了一份静态库代码，增加了内存的总体占用。

### 动态库

#### 制作和使用
1. 使用C++编译器编译源文件为对象文件。与静态库不同的是，在编译时需要使用特殊的选项来生成适合动态链接的对象文件。`-fPIC`（Position Independent Code）选项生成与地址无关的代码，适用于动态库。
1. 使用编译器将对象文件链接成动态库。动态库通常以 .so（在Linux/Unix上）或 .dll（在Windows上）作为扩展名。`-shared` 选项告诉编译器创建一个共享库（动态库）.
1. 将生成的动态库文件（.so 或 .dll 文件）与相应的头文件一起分发。头文件定义了外部程序可以调用的接口。
1. 在编译外部程序时，需要指定动态库的路径并链接该动态库。
1. 在运行程序时，系统需要能够找到动态库文件。可以通过以下几种方式设置动态库的路径。

#### 优点
- 节省内存和磁盘空间：多个程序可以共享同一个动态库的实例，减少了内存占用和磁盘空间使用。
- 更新方便：动态库可以独立于应用程序更新，修复库中的问题或添加功能时，无需重新编译依赖的程序。
- 更小的可执行文件：由于动态库不包含在最终的可执行文件中，生成的可执行文件体积通常较小。
#### 缺点
- 运行时依赖：程序运行时需要依赖动态库，如果动态库缺失或版本不匹配，程序可能无法正常运行。
- 加载时间：程序在启动时需要加载动态库，可能会导致启动时间稍长。
- 版本控制复杂：动态库的更新可能会导致版本兼容性问题，尤其是在API或ABI发生变化时。

### 多进程调用动态库和静态库是否会发生冲突
1. 静态库
不会发生冲突的原因：
- **独立副本**：**每个进程在编译时将静态库的代码嵌入到自己的可执行文件中**。运行时，进程在自己的内存空间中拥有**独立的代码和数据副本**，因此各进程之间互不干扰。
- **虚拟内存隔离**：操作系统为每个进程提供独立的虚拟内存空间，各进程之间的静态库代码和数据彼此隔离。
2. 动态库
一般不会发生冲突的原因：

- **代码段共享，数据段独立**：**动态库的代码段可以在多个进程间共享，减少内存占用，而每个进程的数据段是独立的**，确保进程之间的数据互不干扰。
- **虚拟内存隔离**：操作系统的虚拟内存机制确保每个进程的数据段是独立的，即使多个进程共享同一动态库，也不会因为数据冲突导致问题。

可能发生冲突的特殊情况：

- 全局状态或共享资源：如果动态库使用全局变量、静态变量或操作共享资源（如文件、数据库等），且没有合适的同步机制，可能导致进程间的冲突或资源竞争。
- 线程安全性：如果多个进程中的线程同时调用动态库中的非线程安全函数，可能引发竞态条件（Race Condition）和不确定行为。
  
**总结**

静态库：多进程调用时，由于每个进程都有独立的库代码副本和数据副本，不会发生冲突。

动态库：多进程调用时，代码段共享但数据段独立，一般不会发生冲突。但如果动态库中存在全局状态、共享资源操作或线程安全问题，可能导致进程间冲突，需要特别注意。


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
### move()
- 左值（lvalue）：表示可以持久存储的对象（可以取地址）。
- 亡值（xvalue）：表示即将被销毁或移动的对象资源。
- 纯右值（prvalue）：表示临时计算的结果，不具有内存地址。
#### 右值引用（Rvalue References）
##### 传统的左值引用
- 左值引用允许你引用一个左值（即在程序执行期间持续存在的对象）。

- 左值引用不能绑定到右值（如临时对象、字面值）。

##### 右值引用
- C++11引入了右值引用，这是一种可以绑定到右值的引用类型。右值通常是**临时对象或即将被销毁的对象**。

- 右值引用允许我们通过移动语义来避免不必要的对象拷贝，从而提升程序性能。

##### move
让左值表达式转换为亡值表达式，用于匹配移动构造或移动赋值等函数。
##### 移动构造和拷贝构造
```cpp
#include <iostream>
#include <utility> // std::move

class MyClass {
public:
    int* data;
    size_t size;

    // 构造函数
    MyClass(size_t n) : size(n), data(new int[n]) {
        std::cout << "Constructing MyClass with size " << size << std::endl;
        for (size_t i = 0; i < size; ++i) {
            data[i] = i;
        }
    }

    // 拷贝构造函数
    MyClass(const MyClass& other) : size(other.size), data(new int[other.size]) {
        std::cout << "Copy constructing MyClass" << std::endl;
        std::copy(other.data, other.data + size, data);
    }

    // 移动构造函数
    MyClass(MyClass&& other) noexcept : size(other.size), data(other.data) {
        std::cout << "Move constructing MyClass" << std::endl;
        other.data = nullptr;
        other.size = 0;
    }

    // 析构函数
    ~MyClass() {
        std::cout << "Destructing MyClass with size " << size << std::endl;
        delete[] data;
    }

    // 打印数据内容
    void print() const {
        if (data) {
            for (size_t i = 0; i < size; ++i) {
                std::cout << data[i] << " ";
            }
            std::cout << std::endl;
        } else {
            std::cout << "No data" << std::endl;
        }
    }
};

int main() {
    MyClass obj1(10);          // 正常构造
    MyClass obj2 = std::move(obj1); // 移动构造

    std::cout << "obj1 data: ";
    obj1.print();  // 应该输出 "No data" 因为资源已被移动

    std::cout << "obj2 data: ";
    obj2.print();  // 输出 obj1 原来的数据内容

    return 0;
}

```
## STL
### vector
#### emplace_back & push_back
**比较与区别**
性能：
- push_back：需要先构造对象，再将其复制或移动到容器中。因此，如果对象的复制或移动成本较高，push_back 的性能可能不如 emplace_back。
- emplace_back：直接在容器中构造对象，避免了额外的复制或移动操作，因此通常比 push_back 更高效，尤其是当对象构造成本高时。

使用便利性：

- push_back：适用于你已经有一个现成的对象，并且只是想把它添加到容器末尾的场景。
- emplace_back：适用于你希望直接在容器中构造对象的场景，尤其是构造函数有多个参数时。

临时对象：

- push_back：可能涉及临时对象的构造、复制或移动。
- emplace_back：避免临时对象的构造，直接在容器中构造元素。