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
HOST = ''
PORT = 1234
client_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_2.bind((HOST, PORT))

print("Connection establishment!!!")
d2 = randint(1,N-1)

x, addr = client_2.recvfrom(1024)
x = int(x.decode(), 16)
y, addr = client_2.recvfrom(1024)
y = int(y.decode(), 16)
T1 = (x, y)

T2 = elliptic_multiply(invert(d2, P),T1)
x, y = hex(T2[0]), hex(T2[1])

client_2.sendto(x.encode('utf-8'), addr)
client_2.sendto(y.encode('utf-8'), addr)

print("Connection closed!!!")