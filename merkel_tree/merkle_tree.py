import random
import string
from hashlib import sha256
import math

def create_tree(source_data):
    """create merkle tree from source data

    Args:
        source_data : source_data

    Returns:
        list : merkle tree
    """
    depth = math.ceil(math.log2(len(source_data)) + 1) 
    tree = [[sha256(i.encode()).hexdigest() for i in source_data]]
    for i in range(depth - 1):
        len_lay = len(tree[i])  
        mkt_lay = [sha256(tree[i][j * 2].encode() + tree[i][j * 2 + 1].encode()).hexdigest() for j in range(len_lay // 2)]
        if len_lay % 2 == 1:
            mkt_lay.append(tree[i][-1]) 
        tree.append(mkt_lay)
    return tree

def get_merkle_root(tree):
    return tree[-1][0]


def merkle_proof(spec_elmment, tree, root):
    hash_se = (sha256(spec_elmment.encode())).hexdigest()
    if hash_se in tree[0]:
        index_se = tree[0].index(hash_se)  
    else:
        return "Not in the data."
    depth = len(tree)  
    audit_path = []  
    for i in range(depth - 1):
        if index_se % 2 == 0: 
            if len(tree[i]) - 1 != index_se:  
                audit_path.append(['l', tree[i][index_se + 1]])
        else:  
            audit_path.append(['r', tree[i][index_se - 1]])
        index_se = int(index_se / 2)    # 更新索引值
    for ele in audit_path:
        if ele[0] == 'l':
            hash_se = sha256(hash_se.encode() + ele[1].encode()).hexdigest()
        else:
            hash_se = sha256(ele[1].encode() + hash_se.encode()).hexdigest()
    if hash_se != root:
        return "In the data but not in merkle tree."
    else:
        return "In the merkle tree."


def create_data(length):
    """Randomly generated data

    Args:
        length (int): length of the data

    Returns:
        randomly source data
    """

    return [''.join([random.choice(string.digits + string.ascii_letters) for _ in range(5)]) for _ in range(length)]


if __name__ == "__main__":
    data1 = create_data(100000)
    data2 = create_data(100000)

    index = random.randint(0, 99999)

    # inclusion proof
    spec_element = data1[index]    
    
    # exclusion proof : 指定消息在data   
    data2[index] = spec_element      

    # exclusion proof : 指定消息不在data
    while True:
      spec_element2 = ''.join([random.choice(string.digits + string.ascii_letters) for _ in range(5)])          
      if spec_element2 not in data1:
        break

    merkle_tree = create_tree(data1)
    merkle_tree2 = create_tree(data2)
    root = get_merkle_root(merkle_tree)

    # for i in merkle_tree:   
    #     print(i, "\n")

    # inclusion proof
    print(spec_element," : ", merkle_proof(spec_element, merkle_tree, root))
    # exclusion proof : 指定消息在data   
    print(spec_element," : ", merkle_proof(spec_element, merkle_tree2, root))
    # exclusion proof : 指定消息不在data
    print(spec_element2," : ", merkle_proof(spec_element2, merkle_tree, root))