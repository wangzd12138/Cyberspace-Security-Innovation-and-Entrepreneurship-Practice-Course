import SM3
import os

def rho_method(bit_len):
    hex_len = int(bit_len/4)

    message = os.urandom(32)
    message_a = SM3.sm3_gmssl(message)
    message_a_hex = message_a.hex()[:hex_len]

    message_b = SM3.sm3_gmssl_hex(message_a_hex)
    message_b_hex = message_b.hex()[:hex_len]

    index = 1
    while (message_a_hex != message_b_hex):
        message_a = SM3.sm3_gmssl_hex(message_a_hex)
        message_a_hex = message_a.hex()[:hex_len]
        message_b = SM3.sm3_gmssl_hex(SM3.sm3_gmssl_hex(message_b_hex[:hex_len]).hex()[:hex_len])
        message_b_hex = message_b.hex()[:hex_len]
        index=index+1
    collision = message_a_hex


    message_c = message
    message_c = SM3.sm3_gmssl(message_c)
    message_c_hex = message_c.hex()[:hex_len]

    message_a = SM3.sm3_gmssl_hex(message_a_hex)
    message_a_hex = message_a.hex()[:hex_len]

    while (message_c_hex != message_a_hex):
        message_c = SM3.sm3_gmssl_hex(message_c_hex)
        message_c_hex = message_c.hex()[:hex_len]
        message_a = SM3.sm3_gmssl_hex(message_a_hex)
        message_a_hex = message_a.hex()[:hex_len]
    ring_port = message_c_hex


    message_d_hex = message_c_hex
    message_a = SM3.sm3_gmssl_hex(message_a_hex)
    message_a_hex = message_a.hex()[:hex_len]
    ring_len=1
    while (message_d_hex != message_a_hex):
        message_a = SM3.sm3_gmssl_hex(message_a_hex)
        message_a_hex = message_a.hex()[:hex_len]
        ring_len += 1

    return collision,index,ring_port,ring_len


if __name__ == '__main__':
  bit_length = 20
  collision,index,ring_port,ring_len = rho_method(bit_length)
  print(f"hash值的前{bit_length}bit相同,16进制表示为:{collision}")
  print(f"进行了 {index} 步")
  # print(f"环口(hex) : {ring_port}" )
  print(f"环长 : {ring_len}")