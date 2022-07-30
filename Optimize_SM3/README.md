# Optimize_SM3

## Project
 do your best to optimize SM3 implementation (software)


## 代码说明
该项目文件为Visual Studio编写的C项目文件

**文件说明**

- **main.c** : benchmark代码，并给出一个压缩实例
- **sm3.c** ： SM3算法函数定义，宏函数定义及实现过程
- **sm3.h** ： SM3算法函数声明
- **Debug** ： Visual Studio x86下debug模式运行生成
- **Release** ： Visual Studio x86下release模式运行生成
- **x64** ： Visual Studio x64下release模式运行生成
- **其余文件为运行时Visual Studio生成**

本项目参考openssl对sm3的实现，通过使用宏函数对sm3进行加速。最终在x64 Release实现200w+/s的SM3运算，在x86 Release实现160w+/s的SM3运算

## 运行指导
直接运行main.c,使用Visual Studio时x64 Release可达到最快。

## 运行截图
**x64 Release**

![x64 Release代码运行截图](https://github.com/wzd12138/Cyberspace-Security-Innovation-and-Entrepreneurship-Practice-Course/blob/main/image/Optimize_SM3/SM3_benchmark_x64.png)

**x86 Release**

![x64 Release代码运行截图](https://github.com/wzd12138/Cyberspace-Security-Innovation-and-Entrepreneurship-Practice-Course/blob/main/image/Optimize_SM3/SM3_benchmark.png)