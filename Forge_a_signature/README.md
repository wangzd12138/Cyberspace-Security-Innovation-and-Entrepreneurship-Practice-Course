# Forge_a_signature

## Project
 Forge a signature to pretend that you are Satoshi


## 代码说明
本项目使用Python实现

**伪造原理**
从ECDSA验证算法中可以看到，只需让$s^{-1}(eG+r_xP) =R $ 即可，构造 $R=uG+vP=(r_x',r'_y)$


由
$$ \left\{
\begin{aligned}
{s'}^{-1}e & = & u & mod n \\
{s'}^{-1}r_x & = & v & mod n 
\end{aligned}
\right.
$$
可以解得：
$$ \left\{
\begin{aligned}
e' & = & r'uv^{-1} & mod n \\
s' & = & r'v^{-1} & mod n 
\end{aligned}
\right.
$$
此时输出$sig =(r_x',s')$，皆可以通过对P的验证，但只能提供 $e'$，没办法提供原像



## 运行指导
- 直接运行forge_signature.py

## 运行截图
代码运行如图

![代码运行截图](https://github.com/wzd12138/Cyberspace-Security-Innovation-and-Entrepreneurship-Practice-Course/blob/main/image/ECMH/ECMH.png)