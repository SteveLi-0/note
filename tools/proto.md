# proto
protocal buffers 是一种语言无关，平台无关，可扩展的序列化结构数据的方法，它独立于语言、独立于平台。
protobuf 灵活，高效，简单。
## 安装
## 语法
```
# 语法版本
syntax = "proto3";

# 包声明 可以理解为命名空间
package tutorial;

# 定义消息-定义数据结构
message Person {
  # 字段 Field
  int32 id = 1;
  string name = 2;
  string email = 3;
}

# 定义枚举
enum PhoneType {
  MOBILE = 0;
  HOME = 1;
  WORK = 2;
}

message PhoneNumber {
  string number = 1;
  PhoneType type = 2;
}
```

int32 id = 1; // int32 类型，字段号为 1

string name = 2; // string 类型，字段号为 2

```
# 嵌套类型
message AddressBook {
  message Person {
    int32 id = 1;
    string name = 2;
    string email = 3;
  }
  repeated Person people = 1; // 重复字段
}

# 重复类型-类似于数组
message AddressBook {
  repeated Person people = 1;
}
```

## 生成代码
在终端中运行以下命令，生成数据结构代码 example.pb.h example.pb.cc
```
protoc --proto_path=IMPORT_PATH --cpp_out=DST_DIR --java_out=DST_DIR  path/to/file.proto
```
在cmake中，使用 protobuf_generate 命令，生成代码

