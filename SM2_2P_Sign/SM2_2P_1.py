import SM3
import sys
import socket
import binascii
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

HOST = '127.0.0.1'
PORT = 1234
address = (HOST, PORT)
client_1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    client_1.connect((HOST, PORT))
    print("Connection establishment!!!")
except Exception:
    print('Connection failed...')
    sys.exit()
else:
    d1 = randint(1,N-1)
    
    P1 = elliptic_multiply(invert(d1,P),G)
    x,y = hex(P1[0]),hex(P1[1])
    
    client_1.sendto(x.encode('utf-8'), address)
    client_1.sendto(y.encode('utf-8'), address)

    message = "May the flames guide your way"
    message = hex(int(binascii.b2a_hex(message.encode()).decode(), 16)).upper()[2:]
    ID_A = "sdu_wangzd@163.com"
    ID_A = hex(int(binascii.b2a_hex(ID_A.encode()).decode(), 16)).upper()[2:]
    ENTL_A = '{:04X}'.format(len(ID_A) * 4)
    ma = ENTL_A + ID_A + '{:064X}'.format(A) + '{:064X}'.format(B) + '{:064X}'.format(G_X) + '{:064X}'.format(G_Y)
    ZA = SM3.SM3(ma)
    e = SM3.SM3(ZA + message)
    k1 = randint(1,N-1)
    Q1 = elliptic_multiply(k1,G)
    x,y = hex(Q1[0]),hex(Q1[1])

    client_1.sendto(x.encode('utf-8'),address)
    client_1.sendto(y.encode('utf-8'),address)
    client_1.sendto(e.encode('utf-8'),address)

    r,address = client_1.recvfrom(1024)
    r = int(r.decode(),16)
    s2,address = client_1.recvfrom(1024)
    s2 = int(s2.decode(),16)
    s3,address = client_1.recvfrom(1024)
    s3 = int(s3.decode(),16)
    s=((d1 * k1) * s2 + d1 * s3 - r)%N
    print(f"Signature : {hex(r)} {hex(s)}")
    client_1.close()