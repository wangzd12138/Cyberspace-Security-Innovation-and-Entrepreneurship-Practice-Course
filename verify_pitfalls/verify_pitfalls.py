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


def k_Leaking(message,r,s):
    e = hash(message)
    d =  gmpy2.invert(r,N)*(k*s-e) %N
    print("Leaking k leads to leaking of d ,private key:d=",d)
    return d




def k_Reusing(m1,m2):
    r1,s1=ECDSA_sign(pri_key1,m1)
    r2,s2=ECDSA_sign(pri_key1,m2)
    # print('true d:',pri_key1)
    e1=hash(m1)
    e2=hash(m2)
    d2=(s1*e2-s2*e1)* gmpy2.invert((s2*r1-s1*r2)%N,N)%N
    print('Reusing k leads to leaking of d,d2=',d2)
    return d2


def same_k_Reusing(m1,m2):
    r,s1=ECDSA_sign(pri_key1,m1)
    r,s2=ECDSA_sign(pri_key2,m2)
    e1=hash(m1)
    e2=hash(m2)
    d2=(s2 * e1 - s1 * e2 + s2 * r * pri_key1) * gmpy2.invert(s1 * r, N) % N
    print('User 2\'s actual private key：',pri_key2)
    print('User 1 calculates the private key of user 2：',d2)
    d1=(s1 * e2 - s2 * e1 + s1 * r * pri_key2) * gmpy2.invert(s2 * r, N) % N
    print('User 1\'s actual private key：',pri_key1)
    print('User 2 calculates the private key of user 1：',d1)
    return d2==pri_key2 and pri_key1==d1




def Pretend(m1):
    ran1=random.randint(1,N)
    ran2=random.randint(1,N)
    newpoint= elliptic_add( elliptic_multiply(ran1,G), elliptic_multiply(ran2,pub_key1))
    r_1=newpoint[0]
    e_1=r_1*ran1* gmpy2.invert(ran2,N)%N
    s_1=r_1* gmpy2.invert(ran2,N)%N
    return verify_without_m(e_1,r_1,s_1,pub_key1)




def Schnorr_sign(pri_key,message):
    R= elliptic_multiply(k,G)
    tem=str(R[0])+str(message)
    e=hash(tem)
    s=(k+e*pri_key)%N
    return R,e,s

def Same_dk(pri_key,m):
    R,e2,s2=Schnorr_sign(pri_key,m)
    r1,s1=ECDSA_sign(pri_key,m)
    e1=hash(m)

    s1=(e1+r1*pri_key)* gmpy2.invert((s2-e2*pri_key)%N,N)%N
    d_new=(s1*s2-e1)* gmpy2.invert(s1*e2+r1,N)%N
    # print('true d:',pri_key)
    print('Same d and k with ECDSA, leads to leaking of d:',d_new)
    return d_new
    

if __name__=='__main__':
    message1 = "Long may the sunshine"
    message2 ="May the flames guide your way"

    keys1=generate_key()
    pri_key1=keys1[0]
    pub_key1=keys1[1]

    print("--------------------------------1_Test signature and verification--------------------------------")
    r,s = ECDSA_sign(pri_key1,message1)
    print("Signature:",r,s)
    if ECDSA_verify(message1,r,s,pub_key1):
      print('ECDSA_verify (r,s) Success!!!')
    else:
      print('ECDSA_verify (r,s) Failure...')

    print("--------------------------------2_Leaking k leads to leaking of d--------------------------------")
    d = k_Leaking(message1,r,s)
    if d == pri_key1:
      print("The key has been leaked!!!")
    else:
      print("The key is not compromised...")

    print("--------------------------------3_Reusing k leads to leaking of d--------------------------------")
    d = k_Reusing(message1,message2)
    if d == pri_key1:
      print("The key has been leaked!!!")
    else:
      print("The key is not compromised...")

    print("--------------------------------4_Two users, using k leads to leaking of d, that is they can deduce each other’s d--------------------------------")
    keys2=generate_key()
    pri_key2=keys2[0]
    pub_key2=keys2[1]
    if same_k_Reusing(message1,message2):
        print("Mutual key calculation success!!!")
    else:
        print("Mutual calculation key error...")

    print("--------------------------------5_ r,-s is also a valid signature--------------------------------")
    if ECDSA_verify(message1,r,-s%N,pub_key1):
      print("ECDSA_verify (r,-s) Success!!!")
    else:
      print('ECDSA_verify (r,-s) Failure...')

    print("--------------------------------6_One can forge signature if the verification does not check m--------------------------------")
    if Pretend(message1):
        print('Successful forgery!!!')
    else:
        print('Failed forgery...')

    print("--------------------------------7_Schnorr_Sign signature, ECDSA signature use the same d,k, leading to key leakage--------------------------------")
    d = Same_dk(pri_key1,message1)
    if pri_key1==d:
        print('Cracked successfully!!!')
    else:
        print('Crack failure...')