import secrets
from gmssl import sm3, func
import gmpy2

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

def Legendre(y,p): 
    return pow(y,(p - 1) // 2,p)

def Tonelli_Shanks(y,p):
    assert Legendre(y,p) == 1
    if p % 4 == 3:
        return pow(y,(p + 1) // 4,p)
    q = p - 1
    s = 0
    while q % 2 == 0:
        q = q // 2
        s += 1
    for z in range(2,p):
        if Legendre(z,p) == p - 1:
            c = pow(z,q,p)
            break
    r = pow(y,(q + 1) // 2,p)
    t = pow(y,q,p)
    m = s
    if t % p != 1:
        i = 0
        while t % p != 1: 
            tmp = pow(t,2**(i+1),p)
            i += 1
            if tmp % p == 1:
                b = pow(c,2**(m - i - 1),p)
                r = r * b % p
                c = b * b % p
                t = t * c % p
                m = i
                i = 0 
    return r



def generate_key():
    private_key = int(secrets.token_hex(32), 16)
    public_key = elliptic_multiply(private_key, G)
    # print("Private Key: ",private_key)
    # print("Public Key: " ,public_key)
    return private_key, public_key


def Hash_Set(sett): 
    tag = True
    for i in sett:
        x = int(sm3.sm3_hash(func.bytes_to_list(i)), 16)
        temp = (x ** 2 + A * x + B) % P
        y = Tonelli_Shanks(temp, P)
        if tag:
            digest_value = [x,y]
            tag = False
        else:
            digest_value = elliptic_add(digest_value, [x, y])
    return digest_value

if __name__=='__main__':
    private_key, public_key = generate_key()
    print('public_key ',public_key)
    set1 = (b'111',)
    set3 = (b'111', b'77777')
    set4 = (b'77777', b'111')
    hash_set1 = Hash_Set(set1)
    hash_set3 = Hash_Set(set3)
    hash_set4 = Hash_Set(set4)
    print(f"hash({set1}) = {hash_set1}")
    print(f"hash({set3}) = {hash_set3}")
    print(f"hash({set4}) = {hash_set4}")