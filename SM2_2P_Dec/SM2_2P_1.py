import sys
import math
import socket
from gmpy2 import invert
from random import randint


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
        slope = (q[1] - p[1])*invert(q[0] - p[0], P) % P

        r = [(slope**2 - p[0] - q[0]) % P]
        r.append((slope*(p[0] - r[0]) - p[1]) % P)

        return (r[0], r[1])

def elliptic_double(p):
    slope = (3*p[0]**2 + A)*invert(2*p[1], P) % P

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

def KDF(z,key_len):
    tmp = 1
    key = ''
    for _ in range(math.ceil(key_len/256)):
        t = hex(int(z + '{:032b}'.format(tmp),2))[2:]
        # key = key + hex(int(SM3.SM3(t),16))[2:]
        key = key + hex(hash(t))[2:]
        tmp = tmp + 1
    key ='0'*((256-(len(bin(int(key,16))[2:])%256))%256)+bin(int(key,16))[2:]
    return key[:key_len]


HOST = '127.0.0.1'
PORT = 1234
client_1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    client_1.connect((HOST, PORT))
    print("Connection establishment!!!")
except Exception:
    print("Connection failed...")
    sys.exit()
else:
    d1 = randint(1,N-1)
    
    C1 = (0x26518fd38aa48284d30ce6e5c42d34b57840d1a03b64947b6a300ffe81797cc8,
          0x208be67614cc4562c219dc0cc060aeca05c52bfc1a990f9f02a4ed972ee91df6)
    C2 = 0x4e1d4176afeec9e0ddc7702c1bd9a0393b54bb
    C3 = 0xDF31DE4A7A859CF0E06297030D4F8DE7ACA5D182D89FE278423F7D12F9C3E03C
    
    T1 = elliptic_multiply(invert(d1, P),C1)
    x, y = hex(T1[0]), hex(T1[1])
    klen = len(hex(C2)[2:])*4
    
    addr = (HOST, PORT)
    client_1.sendto(x.encode('utf-8'), addr)
    client_1.sendto(y.encode('utf-8'), addr)

    x1, addr = client_1.recvfrom(1024)
    x1 = int(x1.decode(), 16)
    y1, addr = client_1.recvfrom(1024)
    y1 = int(y1.decode(), 16)
    T2 = (x1, y1)
    
    x2, y2 = elliptic_add(T2, (C1[0], -C1[1]))
    x2, y2 = '{:0256b}'.format(x2), '{:0256b}'.format(y2)
    t = KDF(x2 + y2, klen)
    M2 = C2 ^ int(t,2)
    m = hex(int(x2,2)).upper()[2:] + hex(M2).upper()[2:] + hex(int(y2,2)).upper()[2:]
    u = hash(m)
    if (u == C3):
        print(hex(M2).upper()[2:])
    print(f"Result : {hex(M2)}")
    client_1.close()