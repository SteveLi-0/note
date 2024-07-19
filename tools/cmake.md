# cmake
## 常用命令
### cmake_minimum_required
```
cmake_minimum_required(VERSION 3.0.0)
```
### project
```
project(DEMO)
```
这个项目名称是与ros中的package名称一致的。（在xml文件中可见）
### set
```
set(CMAKE_CXX_STANDARD 11)
SET(SRC_LIST XXX.CC YYY.cc zzz.cc)
set(CMAKE_BUILD_TYPE "Debug")
set(CMAKE_CXX_FLAGS_DEBUG "$ENV{CXXFLAGS} -O0 -Wall -g2 -ggdb")
set(CMAKE_CXX_FLAGS_RELEASE "$ENV{CXXFLAGS} -O3 -Wall")
```
设置一些变量，比如设置编译的c++标准，debug信息，文件/路径等。
### add_subdirectory
假设有如下的项目结构：
```
MyProject/
├── CMakeLists.txt
├── src/
│   ├── CMakeLists.txt
│   ├── main.cpp
│   └── ...
└── lib/
    ├── CMakeLists.txt
    ├── SomeLibrary.cpp
    └── ...
```
在根目录的CMakeLists.txt中添加：
```
# MyProject/CMakeLists.txt

cmake_minimum_required(VERSION 3.10)
project(MyProject)

# 添加子目录
add_subdirectory(src)
add_subdirectory(lib)
```
用于将指定的子目录加入到构建过程中。这个命令允许你在大型项目中分离不同的模块或组件，并且使它们能够独立管理各自的 CMake 配置文件。
- 子目录依赖：确保子目录之间的依赖关系正确。例如，如果 src 目录中的目标依赖于 lib 目录中的目标，lib 子目录**应该先被添加**。
- 命名空间：使用适当的命名空间和目标名称，以避免命名冲突。
### include_directories

制定头文件搜索路径。
### find_package

查找依赖的库。required参数表示是否必须。
### add_executable

指定编译生成的二进制文件名称，和依赖的源文件。
### target_link_libraries
```
target_link_libraries(ilqr_tree utils)
```
将项目目标（可执行文件/库）链接到指定的库。ilqr_tree 目标依赖于 utils 库。
### add_dependencies
### add_custom_target

### add_library
```
add_library(ilqr_tree 
            SHARED 
            ilqr_tree.cc 
            ilqr_taylor_expansions.cc 
            ilqr_node.cc 
            ilqrtree_helpers.cc
            )
```
创建一个名为 ilqr_tree 的共享库（动态库），ilqr_tree.cc, ilqr_taylor_expansions.cc, ilqr_node.cc, ilqrtree_helpers.cc：这些是组成 ilqr_tree 库的源文件。

## 参考案例
https://github.com/LAIRLAB/qr_trees

