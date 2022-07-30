# PGP

## Project
 Implement a PGP scheme with SM2


## 代码说明
本项目使用Python实现


使用SM4与SM2实现PGP方案，思路如下图：



![思路](https://github.com/wzd12138/Cyberspace-Security-Innovation-and-Entrepreneurship-Practice-Course/blob/main/image/PGP/PPT.png)


加密时使用SM4加密message = "May the flames guide your way"，SM2加密会话密钥；

解密,使用SM2解密求得会话密钥，再使用SM4和会话密钥解密原消息。

## 运行指导
- 需要安装gmssl库
- 直接运行PGP.py

## 运行截图
代码运行如图

![代码运行截图](https://github.com/wzd12138/Cyberspace-Security-Innovation-and-Entrepreneurship-Practice-Course/blob/main/image/PGP/PGP.png)