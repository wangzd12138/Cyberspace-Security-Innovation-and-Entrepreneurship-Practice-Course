import random
import SM3

def birth_atk_dict(len):
    """Similar to counting sort, using space for time for birthday attacks

    Args:
          len (int) : Bit length of the collision

    Returns:
        same bits in hexadecimal in the hash message
        message1
        message2
    """
    tag = -1
    sizes = int( 2**len)  
    sm3_tag = [tag] * 2**len      
    for message in range(sizes):
        hash_msg = int(SM3.SM3(str(message))[:int(len / 4)], 16)
        if sm3_tag[hash_msg] == tag :
            sm3_tag[hash_msg] = message
        else:
            return hex(hash_msg), message, sm3_tag[hash_msg]


def birth_atk_collision(len):
    """Birthday attack by collision

    Args:
        len (int) : Bit length of the collision

    Returns:
        same bits in hexadecimal in the hash message
        message1
        message2
    """
    while True:
      msg1 = random.randint(0,2**256)
      msg2 = random.randint(0,2**256)
      hash_msg1 = int(SM3.SM3(str(msg1))[:int(len / 4)], 16)
      hash_msg2 = int(SM3.SM3(str(msg2))[:int(len / 4)], 16)
      if hash_msg1 == hash_msg2:
        return hex(hash_msg1), msg1, msg2

def birthday_attack(len):
    """根据寻找碰撞的bit长度进行生日攻击

    Args:
        len (int) : 碰撞的bit长度

    Returns:
        same bits in hexadecimal in the hash message
        message1
        message2
    """
    # bit长度过短时利用空间换时间的方法，较长时利用碰撞
    return birth_atk_dict(len) if len <= 28 else birth_atk_collision(len)
    
if __name__ == '__main__':
    # 碰撞bit长度
    bit_length = 20 
    collision, msg1, msg2 = birthday_attack(bit_length)
    print(f"消息{msg1}与{msg2}哈希值的前{bit_length}bit相同,16进制表示为:{collision}。")