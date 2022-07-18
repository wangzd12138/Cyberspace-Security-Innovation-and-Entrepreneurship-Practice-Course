import secrets
from hashlib import sha256

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

def extended_euclidean(j, k):
    if j == k:
        return (j, 1, 0)
    i = 0
    j_array = [j]
    k_array = [k]
    q_array = []
    r_array = []

    prev_r_tag = False

    while not (prev_r_tag):
        q_array.append(k_array[i]//j_array[i])
        r_array.append(k_array[i]%j_array[i])
        k_array.append(j_array[i])
        j_array.append(r_array[i])
        i += 1
        if r_array[i-1] == 0:
            prev_r_tag = True
    i -= 1
    gcd = j_array[i]
    x_array = [1]
    y_array = [0]
    i -= 1
    steps = i
    while i >= 0:
        y_array.append(x_array[steps-i])
        x_array.append(y_array[steps-i] - q_array[i]*x_array[steps-i])
        i -= 1

    return (gcd, x_array[-1], y_array[-1])

def mod_inverse(j, n):
    (gcd, x, y) = extended_euclidean(j, n)
    return x%n if gcd == 1 else -1


# 有限域
P = 115792089237316195423570985008687907853269984665640564039457584007908834671663
# 椭圆曲线
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
A = 0
B = 7


def elliptic_add(p, q):
    if p == 0 and q == 0: return 0
    elif p == 0: return q
    elif q == 0: return p
    else:
        return _extracted_from_elliptic_add_7(p, q)


def _extracted_from_elliptic_add_7(p, q):
    if p[0] > q[0]:
        p, q = q, p
    slope = (q[1] - p[1])*mod_inverse(q[0] - p[0], P) % P

    r = [(slope**2 - p[0] - q[0]) % P]
    r.append((slope*(p[0] - r[0]) - p[1]) % P)

    return (r[0], r[1])


def elliptic_double(p):
    slope = (3*p[0]**2 + A)*mod_inverse(2*p[1], P) % P

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


G_X = 55066263022277343669578718895168534326250603453777594175500187360389116729240
G_Y = 32670510020758816978083085130507043184471273380659243275938904335757337482424

G = (G_X, G_Y)

def generate_key():
    """生成公钥私钥

    Returns:
        private_key , public_key
    """
    private_key = int(secrets.token_hex(32), 16)
    public_key = elliptic_multiply(private_key, G)
    return private_key, public_key



def hash(message):
    """hash函数

    Args:
        message : 消息

    Returns:
        hash后消息
    """
    # hashmessage = sha256(message.encode('utf-8')).hexdigest()
    # # 双重hash
    # hashmessage = sha256(hashmessage.encode('utf-8')).hexdigest()
    return int(sha256(message.encode('utf-8')).hexdigest(), 16)



def Signature(private_key, message):
    """签名

    Args:
        private_key : 私钥
        message : 消息

    Returns:
        tuple : Signature
    """
    e = hash(message)
    k = secrets.randbelow(P)
    random_point = elliptic_multiply(k, G)
    r = random_point[0] % P
    s = mod_inverse(k, N) * (e + r*private_key) % N
    return (r, s)



def deduce_pubkey(signature,message):
    """从签名中推导出公钥

    Args:
        signature : 签名
        message : 消息

    Returns:
        猜测公钥
    """
    r=signature[0]
    s=signature[1]
    x = r % P
    y2=((x**3)+7)
    y=Tonelli_Shanks(y2,P)


    e = hash(message)
    point_1=(x,y)
    point_2=(x,P-y)

    skG=elliptic_multiply(s%N,point_1)
    eG=elliptic_multiply(e%N,G)
    negeG=(eG[0],P-eG[1])
    skGeG=elliptic_add(skG,negeG)
    deduce_key1=elliptic_multiply(mod_inverse(r,N),skGeG)

    skG=elliptic_multiply(s%N,point_2)
    skGeG=elliptic_add(skG,negeG)
    deduce_key2=elliptic_multiply(mod_inverse(r,N),skGeG)
    return deduce_key1,deduce_key2

if __name__ == "__main__":

    private_key, public_key = generate_key()
    print('public key',public_key)

    message = "May_the_flames_guide_your_way"
    signature = Signature(private_key, message)

    print("Signature: ",signature)

    deduce_pubkey1,deduce_pubkey2=deduce_pubkey(signature,message)
    print('Deduce public key from signature:')
    print('Deduce public key1:',deduce_pubkey1)
    print('Deduce public key2:',deduce_pubkey2)