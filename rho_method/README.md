# Rho_method

## Project
implement the Rho method of reduced SM3

## 代码说明
本项目使用Python实现


**文件说明**
- **Rho_method.py** : Rho环路攻击代码，寻找碰撞
- **SM3.py** ： SM3的python版本简单实现

具体流程为 ：初始一个消息，然后对这个消息hash一下，算出具体的hash值后，因为使用SM3进行哈希，所以应选取前n位。然后对这个结果再次hash，再次选取前n位，直到找到一个环为止。


判环方法使用Floyd判环法：规定两个变量msg1和msg2。msg1每次做一次hash截取，msg2做两次哈希两次截取，用index记录当前走过的步数。直到msg1和msg2相等时，说明出现了一个环，且index是环长的整数倍。


然后寻找环口。此时保持msg2不变，规定msg3从开头开始走，msg1从当前位置开始走，直到碰撞，此时的值即为环口的值。

最后寻找环长，对于环长，只需要从上述环口位置，直到第一次走回环口，所经过的步数就是环长的值。

## 运行指导
Rho_method.py与SM3.py放于同级目录下，运行Rho_method.py

## 运行截图
以寻找前20bit碰撞为例，代码运行如图

![代码运行截图](https://github.com/wzd12138/Cyberspace-Security-Innovation-and-Entrepreneurship-Practice-Course/blob/main/image/rho_method/rho_method.png)