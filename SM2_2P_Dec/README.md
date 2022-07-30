# SM2_2P_Dec

## Project
 Implement sm2 2P decrypt with real network communication

## 代码说明
本项目使用Python实现


**文件说明**
- **SM2_2P_1.py** : SM2 2P decrypt方案中用户1(客户端)
- **SM2_2P_2.py** ：SM2 2P decrypt方案中用户2(服务器端)

首先，socket编程也叫套接字编程,应用程序可以通过它发送或者接受数据,可对其像打开文件一样打开/关闭/读写等操作.套接字允许应用程序将I/O插入到网络中,并与网络中的其他应用程序进行通信.网络套接字是IP地址与端口号TCP协议的组合.Socket就是为网络编程提供的一种机制,通信的两端都有Socket.网络通信其实就是Socket之间的通信,数据在两个Socket之间通过I/O进行传输.



SM2 2P decrypt方案思路如图：
![方案思路](https://github.com/wzd12138/Cyberspace-Security-Innovation-and-Entrepreneurship-Practice-Course/blob/main/image/SM2_2P_Dec/PPT.png)


## 运行指导
首先运行**SM2_2P_2.py**，再运行**SM2_2P_1.py**。代码均可直接运行。

## 运行截图
代码运行如图

![代码运行截图](https://github.com/wzd12138/Cyberspace-Security-Innovation-and-Entrepreneurship-Practice-Course/blob/main/image/SM2_2P_Dec/SM2_2P_Dec.png)