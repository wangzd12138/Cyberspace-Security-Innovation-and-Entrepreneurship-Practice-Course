import base64
import random
from gmssl import sm2
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
import gmpy2
import secrets

# 有限域
P = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
# 椭圆曲线
N = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
A = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
B = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
G_X = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
G_Y = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
G = (G_X, G_Y)


def elliptic_add(p, q):
    if p == 0 and q == 0: return 0
    elif p == 0: return q
    elif q == 0: return p
    else:
        if p[0] > q[0]:
            p, q = q, p
        slope = (q[1] - p[1])*gmpy2.invert(q[0] - p[0], P) % P

        r = [(slope**2 - p[0] - q[0]) % P]
        r.append((slope*(p[0] - r[0]) - p[1]) % P)

        return (r[0], r[1])

def elliptic_double(p):
    slope = (3*p[0]**2 + A)*gmpy2.invert(2*p[1], P) % P

    r = [(slope**2 - 2*p[0]) % P]
    r.append((slope*(p[0] - r[0]) - p[1])%P)

    return (r[0], r[1])

def elliptic_multiply(s, p):
    n = p
    r = 0 
    s_binary = bin(s)[2:] 
    s_length = len(s_binary)
    for i in reversed(range(s_length)):
        if s_binary[i] == '1':
            r = elliptic_add(r, n)
        n = elliptic_double(n)

    return r

def generate_key():
    private_key = int(secrets.token_hex(32), 16)
    public_key = elliptic_multiply(private_key, G)
    # print("Private Key: ",private_key)
    # print("Public Key: " ,public_key)
    return private_key, public_key



def PGP_Encrypt(message,key):
    l = 16
    n = len(message)
    num = l - (n % l) if n % l != 0 else 0
    message = message + ('\0' * num)
    message = str.encode(message)
    key = str.encode(key)
    print(f"Message(str)：{message}")
    print(f"Key(bytes)：{base64.b16encode(key)}" )
    
    SM4 = CryptSM4()
    SM4.set_key(key, SM4_ENCRYPT)
    c1 = SM4.crypt_ecb(message)

    c2 = sm2_crypt.encrypt(key)
    print(f"Encrypt_message(bytes)：{base64.b16encode(c1)}" )
    print(f"Encrypt_key(bytes)：{base64.b16encode(c2)}")
    return c1, c2

def PGP_Decrypt(c1,c2):
    k = sm2_crypt.decrypt(c2)
    SM4 = CryptSM4()
    SM4.set_key(k, SM4_DECRYPT)
    m = SM4.crypt_ecb(c1)
    print(f"Decrypt_message(str)：{m}")
    print(f"Decrypt_key(bytes)：{base64.b16encode(k)}")
    
if __name__ == '__main__':
    sk,pk = generate_key()
    sk = hex(sk)[2:]
    pk = hex(pk[0])[2:] + hex(pk[1])[2:]

    sm2_crypt = sm2.CryptSM2(public_key=pk, private_key=sk)
    
    message = "May the flames guide your way"
    
    key = hex(random.randint(2 ** 127, 2 ** 128))[2:]
  
    c1,  c2 = PGP_Encrypt(message, key)
    PGP_Decrypt( c1,  c2)