# merkel_tree

## Project
 Impl Merkle Tree following RFC6962

## 代码说明
本项目使用Python实现




MerkleTree可以看做Hash List的泛化（Hash List可以看作一种特殊的Merkle ree，即树高为2的多叉MerkleTree）。


MerkleTree的主要作用是快速归纳和校验区块数据的存在性和完整性。一般意义上来讲，它是哈希大量聚集数据“块”的一种方式，它依赖于将这些数据“块”分裂成较小单位的数据块，每一个bucket块仅包含几个数据“块”，然后取每个bucket单位数据块再次进行哈希，重复同样的过程，直至剩余的哈希总数仅变为1。



在最底层，和Hash List一样，把数据分成小的数据块，计算对应的哈希值。但之后并非直接去运算根哈希，而是把相邻的两个哈希合并成一个字符串，然后计算这个新字符串的哈希值，以此类推，最终形成一棵倒挂的树。倘若该层节点不足以两两分完，则将最后一个节点记录下来，并以它为头节点对应的树上的所有节点高度均加一作为下一层节点进行，以符合RFC6962要求。

按照下图所示结构实现MerkleTree，自底向上实现。

![mktree.png](https://github.com/wzd12138/Cyberspace-Security-Innovation-and-Entrepreneurship-Practice-Course/blob/main/image/merkel_tree/merkle_tree_md.png)
对于MerkleTree proof的实现参考了RFC6962，对于每个data都找到一条与之对应的audit path用于检验该数据是否属于该树

在项目中按照如下思路实现：

- 创建一棵MerkleTree，随机从其Data中挑选一个块检验其是否在MerkleTree中。

- 创建一棵MerkleTree，保证其Data中有一个块与之前创建的MerkleTree的Data中有一个块相同，并检验该块是否在MerkleTree中。

- 检验一个已知的不在MerkleTree的数据块是否在MerkleTree的Data中。


## 运行指导
直接运行merkle_tree.py


## 运行截图
代码运行如图

![代码运行截图](https://github.com/wzd12138/Cyberspace-Security-Innovation-and-Entrepreneurship-Practice-Course/blob/main/image/merkel_tree/merkle_tree.png)