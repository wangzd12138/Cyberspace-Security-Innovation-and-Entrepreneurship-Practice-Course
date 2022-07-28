import secrets
import random
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
        return _extracted_from_elliptic_add_9(p, q)


def _extracted_from_elliptic_add_9(p, q):
    if p[0] > q[0]:
        p, q = q, p
    slope = (q[1] - p[1])*pow(q[0] - p[0],-1, P) % P

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
    return private_key, public_key

k = secrets.randbelow(P)

def ECDSA_sign(private_key, message):
    e = hash(message)
    random_point = elliptic_multiply(k, G)
    r = random_point[0] % N
    s = gmpy2.invert(k, N) * (e + r*private_key) %N
    return r, s

def ECDSA_verify(m,r,s,pub_key):
    e=hash(m)
    W= gmpy2.invert(s,N)%N
    recovered_point= elliptic_add( elliptic_multiply(e*W%N,G) ,  elliptic_multiply(r*W %N,pub_key))
    r_new = recovered_point[0]
    return 1 if r_new == r else 0

def verify_without_m(e,r,s,pub_key):
    s_1= gmpy2.invert(s,N)%N
    recovered_point= elliptic_add( elliptic_multiply(e*s_1%N,G) ,  elliptic_multiply(r*s_1 %N,pub_key))
    r_new=recovered_point[0]
    return r_new == r

def forge_signature(m1):
    ran1=random.randint(1,N)
    ran2=random.randint(1,N)
    newpoint= elliptic_add( elliptic_multiply(ran1,G), elliptic_multiply(ran2,pub_key1))
    r_1=newpoint[0]
    e_1=r_1*ran1* gmpy2.invert(ran2,N)%N
    s_1=r_1* gmpy2.invert(ran2,N)%N
    print(f"The forged signature : {r_1} {s_1}")
    return verify_without_m(e_1,r_1,s_1,pub_key1)




    

if __name__=='__main__':
    message1 ="May the flames guide your way"

    keys1=generate_key()
    pri_key1=keys1[0]
    pub_key1=keys1[1]

    print(f"Satoshi Nakamoto's public key is {pub_key1}")

    r,s = ECDSA_sign(pri_key1,message1)
    print("Signature:",r,s)

    if forge_signature(message1):
        print('Successful forgery!!!')
    else:
        print('Failed forgery...')

    