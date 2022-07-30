# length_extension_attack

## Project
  implement length extension attack for SM3, SHA256, etc


## 代码说明
本项目使用Python实现对**SM3**和**SHA256**的长度拓展攻击


针对SM3进行长度扩展攻击，攻击过程大体如下：
- 对任意消息secret_message，首先对其进行填充，得到 m=secret_message||padding
- 调用SM3计算哈希值即 h1=SM3(m,IV)
- 自选extension作为进行攻击的消息，计算 h2=SM3(m||extension,IV)即h2=SM3(secret_message||padding||extension,IV)
- 计算 h3=SM3(extension,iv)，其中iv=h1即先前消息的哈希值
- 比较h2与h3是否相同，若相同，则攻击成功。




## 运行指导
- **SM3** : 进入SM3文件夹下直接运行length_extension_attack.py
- **SHA256** : 进入SHA256文件夹下直接运行length_extension_attack.py

## 运行截图
代码运行如图

### SM3

![SM3代码运行截图](https://github.com/wzd12138/Cyberspace-Security-Innovation-and-Entrepreneurship-Practice-Course/blob/main/image/Forge_a_signature/Forge_a_signature.png)

### SHA256
![SHA256代码运行截图](https://github.com/wzd12138/Cyberspace-Security-Innovation-and-Entrepreneurship-Practice-Course/blob/main/image/Forge_a_signature/Forge_a_signature.png)