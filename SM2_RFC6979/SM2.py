import secrets
from gmssl import sm3, func

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

def get_bit_num(x):
    if isinstance(x, int):
        return _extracted_from_get_bit_num_3(x)
    elif isinstance(x, str):
        return len(x.encode()) << 3
    elif isinstance(x, bytes):
        return len(x) << 3
    return 0


def _extracted_from_get_bit_num_3(x):
    num = 0
    tmp = x >> 64
    while tmp:
        num += 64
        tmp >>= 64
    tmp = x >> num >> 8
    while tmp:
        num += 8
        tmp >>= 8
    x >>= num
    while x:
        num += 1
        x >>= 1
    return num

G_X = 55066263022277343669578718895168534326250603453777594175500187360389116729240
G_Y = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = (G_X, G_Y)

def precompute(ID,a,b,G_X,G_Y,x_A,y_A):
    """
    Args:
        ID : ID
        a : 椭圆曲线参数a
        b : 椭圆曲线参数b
        G_X : G点x
        G_Y : G点y
        x_A : 公钥x
        y_A : 公钥y

    Returns:
        int
    """
    a=str(a)
    b=str(b)
    G_X=str(G_X)
    G_Y=str(G_Y)
    x_A=str(x_A)
    y_A=str(y_A)
    ENTL=str(get_bit_num(ID))
    joint=ENTL+ID+a+b+G_X+G_Y+x_A+y_A
    joint_b=bytes(joint,encoding='utf-8')
    digest= sm3.sm3_hash(func.bytes_to_list(joint_b))
    return int(digest, 16)

def generate_key():
    private_key = int(secrets.token_hex(32), 16)
    public_key = elliptic_multiply(private_key, G)
    # print("Private Key: ",private_key)
    # print("Public Key: " ,public_key)
    return private_key, public_key

def signature(private_key, message,Z_A):
    """使用私钥进行签名

    Args:
        private_key : private_key
        message : message
        Z_A : Z_A

    Returns:
        tuple: 签名
    """
    _M=Z_A+message
    _M_b=bytes(_M,encoding='utf-8')
    e = sm3.sm3_hash(func.bytes_to_list(_M_b))
    e=int(e, 16)

    k = secrets.randbelow(P)
    random_point = elliptic_multiply(k, G)

    # print('randpoint ', random_point)
    r =( e+random_point[0] )% N

    s = (mod_inverse(1+private_key, N) * (k - r*private_key))%N 
    return (r, s)




def verify(ID, public_key,message, signature):
    """Verify

    Args:
        public_key : public key
        ID : ID
        message : message
        signature : 待验证signature

    Returns:
        bool: yes or no
    """
    r=signature[0]
    s=signature[1]

    Z=precompute(ID,A,B,G_X,G_Y,public_key[0],public_key[1])

    _M=str(Z)+message
    _M_b=bytes(_M,encoding='utf-8')
    e=sm3.sm3_hash(func.bytes_to_list(_M_b))
    e=int(e, 16)
    t=(r+s) % N
    point=elliptic_multiply(s ,G)
    point=elliptic_add(point,elliptic_multiply(t ,  public_key))
    x1=point[0]
    x2=point[1]
    R=(e+x1)%N

    return R==r



if __name__=='__main__':
    
    private_key, public_key = generate_key()
    print('public_key ',public_key)

    message = "May the flames guide your way"
    ID='wzd'
    Z_A=precompute(ID,A,B,G_X,G_Y,public_key[0],public_key[1])
    
    Signature = signature(private_key, message,str(Z_A))
    print('signature ',Signature)

    if verify(ID,public_key,message,Signature)==1:
        print('PASS!!!')