# Deduce_pubkey

## Project
report on the application of this deduce technique in Ethereum with 
ECDSA

## 代码说明
本项目使用Python实现

​ ECDSA全称椭圆曲线数字签名算法，是使用椭圆曲线密码（ECC）对数字签名算法（DSA）的模拟。与普通的离散对数问题（DLP）和大数分解问题（IFP）不同，椭圆曲线离散对数问题没有亚指数时间的解决方法。因此椭圆曲线密码的单位比特强度要高于其他公钥体制。这带来的好处就是计算参数更小，密钥更短，运算速度更快，签名也更加短小。

使用编写的ECDSA签名方案，对message = "May_the_flames_guide_your_way"进行签名。

得到消息$m$和其对应的签名$(r,s)$后，我们需要恢复能够成功验证签名的公钥Q(曲线上的点)：

$s=k^{-1}(e+dr)\Rightarrow s\cdot kG=eG+dG\cdot r\Rightarrow s\cdot kG-eG=Q\cdot r\Rightarrow Q=r^{-1}(s\cdot kG-eG)$

已知上式中$s,r,e=H(m)$，则只需$P=kG$，即可恢复出正确的验签公钥$Q$.

但是敌手并不知道$P$，只知道$r \equiv x \mod n，x\in[1,p],p$为椭圆曲线上素域的阶，通常来说$n\lt p$，因此一个$r$可能对应两个$x$：

- 若$r\lt p-n$，则$x=r$或$ x=r+n$
- 若$r\gt p-n$，则$x=r$

在$x$被确定后，需要用其确定$P$，根据椭圆曲线的公式可知一个$x$对应了两个曲线上的点$P_1,P_2$，且这两个点生成的$Q$都可以用于验签，所以理论上来看最多可以恢复4个能够正确验签的公钥。



## 运行指导
直接运行ECDSA.py

## 运行截图
代码运行如图

![代码运行截图](https://github.com/wzd12138/Cyberspace-Security-Innovation-and-Entrepreneurship-Practice-Course/blob/main/image/birthday_attack/birthday_attack.png)