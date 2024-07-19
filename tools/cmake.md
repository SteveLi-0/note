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
```
add_subdirectory (src)
```
将src目录下的所有文件添加到编译列表中。
### include_directories

制定头文件搜索路径。
### find_package

查找依赖的库。required参数表示是否必须。
### add_executable

指定编译生成的二进制文件名称，和依赖的源文件。
### target_link_libraries

将项目可执行文件链接到指定的库。
### add_dependencies
### add_custom_target
## 
