# SM2

## Project
 impl sm2 with RFC6979

## 代码说明
本项目使用Python实现



SM2是一种非对称加密算法。它基于椭圆曲线密码的公钥密码算法标准，密钥长度为256bit，包含数字签名、密钥交换和公钥加密，可以满足电子认证服务系统等应用需求。SM2采用的是ECC 256位的一种，其安全强度比RSA 2048位高，且运算速度快于RSA。



**椭圆曲线参数**

SM2的椭圆曲线参数为

- A：0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
- B：0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
- P：0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF  
  

**预处理**

输入

- ID : 用户身份标识,本项目使用ID='wzd'
- PublicKey : 用户的公钥

输出

- Z：$hash(SM3(ENTL∣ID∣a∣b∣x_G∣y_G∣x_A∣y_A))$
- ENTL为由2个字节标识的ID的比特长度

**签名算法**

​	待签名的消息为message = "May the flames guide your way"，通过一下步骤得到消息message的签名 ( r , s ) 

- 置  $\overline{M}=Z_A||message $
- 计算$e=hash(\overline{M}) $
- 产生随机数$k$
- 计算椭圆曲线点$(x_1,y_1)=[k]G $
- $ r=(e+x_1) mod \ n$
- $ s=((1+d_A)^{-1}\cdot (k-r \cdot d_A)) mod\ n$

**验证算法**

验证消息message及其签名$( r , s )$：

- 置 $\overline{M}=Z_A||message $
- 计算$e=hash(\overline{M})$
- $t=(r+s) mod  n $
- 计算椭圆曲线点$ (x_1,y_1)=[s]G+[t]P_A$
- $ R=(e+x_1) mod  n$
- 检验 R = r是否成立，若成立则验证通过；否则验证不通过。

    



## 运行指导
直接运行SM2.py

## 运行截图
代码运行如图

![代码运行截图](https://github.com/wzd12138/Cyberspace-Security-Innovation-and-Entrepreneurship-Practice-Course/blob/main/image/SM2/SM2.png)