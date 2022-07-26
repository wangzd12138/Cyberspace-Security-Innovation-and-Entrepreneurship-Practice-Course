import secrets
from gmssl import sm3, func
import gmpy2

# 有限域
P = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
# 椭圆曲线
N = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
A = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
B = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93


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

G_X = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
G_Y = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
G = (G_X, G_Y)

def pre_compute(ID,a,b,G_X,G_Y,x_A,y_A):
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

    r =( e+random_point[0] )% N

    s = (gmpy2.invert(1+private_key, N) * (k - r*private_key))%N 
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

    Z=pre_compute(ID,A,B,G_X,G_Y,public_key[0],public_key[1])

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
    Z_A=pre_compute(ID,A,B,G_X,G_Y,public_key[0],public_key[1])
    
    Signature = signature(private_key, message,str(Z_A))

    print('message : ',message)
    print('ID : ',ID)
    print('signature ',Signature)

    if verify(ID,public_key,message,Signature)==1:
        print('Verification PASS!!!')
    else:
        print('Verification failure...')