# Verify_pitfalls

## Project
 verify the above pitfalls with proof-of-concept cod

## 代码说明
本项目使用Python实现

本项目测试了SM2签名存在的几种缺陷：
- Leaking *k* leads to leaking of *d*
- Reusing *k* leads to leaking of *d*
- Two users, using *k* leads to leaking of *d*, that is they can deduce each other’s *d* 
- Malleability of ECDSA, e.g. (*r*, *s*) and (*r*,*-s*) are both valid signatures
- One can forge signature if the verification does not check *m* 
- Same *d* and *k* used in ECDSA & Schnorr signature, leads to leaking of *d*


## 运行指导
直接运行verify_pitfalls.py

## 运行截图
代码运行如图

![代码运行截图](https://github.com/wzd12138/Cyberspace-Security-Innovation-and-Entrepreneurship-Practice-Course/blob/main/image/verify_pitfalls/verify_pitfalls.png)