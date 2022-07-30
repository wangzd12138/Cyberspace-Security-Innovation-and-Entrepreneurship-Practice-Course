# Birthday Attack

## Project
Implement the naïve birthday attack of reduced SM3

## 代码说明
本项目使用Python实现


**文件说明**
- **birthday_attack.py** : 生日攻击代码，根据寻找碰撞的比特长度使用两种思想进行生日攻击
- **SM3.py** ： SM3的python版本简单实现

使用生日攻击的思想对为$l$ bit的串进行攻击，则进行$2^{l/2}$次搜索即可以较高概率找到碰撞。如果我们只考虑前$l$比特，那么在前$0-2^l$范围内，几乎至少存在一组碰撞。


- 使用**空间换时间思想**，确定原像空间大小后，建立一个对应大小的列表并进行碰撞。消耗了较多的存储空间但缩短代码运行时间，但当攻击的串较长时，可能会空间不足。
- 当攻击的串较长时，直接寻找对应前$l$bit的碰撞

## 运行指导
birthday_attack.py与SM3.py放于同级目录下，运行birthday_attack.py

## 运行截图
以寻找前20bit碰撞为例，代码运行如图

![代码运行截图](https://github.com/wzd12138/Cyberspace-Security-Innovation-and-Entrepreneurship-Practice-Course/blob/main/image/birthday_attack/birthday_attack.png)