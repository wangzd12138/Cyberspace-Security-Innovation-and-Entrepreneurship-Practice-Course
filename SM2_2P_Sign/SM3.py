IV = [0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600, 0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E]
T = [0x79cc4519, 0x7a879d8a]


def ROL(X, i):
    i = i % 32
    return ((X << i) & 0xFFFFFFFF) | ((X & 0xFFFFFFFF) >> (32 - i))


def FF(X, Y, Z, j):
    return X ^ Y ^ Z if j >= 0 and j <= 15 else ((X & Y) | (X & Z) | (Y & Z))


def GG(X, Y, Z, j):
    return X ^ Y ^ Z if j >= 0 and j <= 15 else ((X & Y) | (~X & Z))


def P0(X):
    return X ^ ROL(X, 9) ^ ROL(X, 17)


def P1(X):
    return X ^ ROL(X, 15) ^ ROL(X, 23)


def T_(j):
    return T[0] if j >= 0 and j <= 15 else T[1]


def Fill(message):
    """填充消息

    Args:
        message : 消息

    Returns:
        填充后消息
    """
    m = bin(int(message, 16))[2:]
    if len(m) != len(message) * 4:
        m = '0' * (len(message) * 4 - len(m)) + m
    l = len(m)
    l_bin = '0' * (64 - len(bin(l)[2:])) + bin(l)[2:]
    m = f'{m}1'
    if len(m) % 512 > 448:
        m = m + '0' * (512 - len(m) % 512 + 448) + l_bin
    else:
        m = m + '0' * (448 - len(m) % 512) + l_bin
    m = hex(int(m, 2))[2:]
    return m


def Group(m):
    """数据分组
    
    """
    n = len(m) / 128
    return [m[0 + 128 * i:128 + 128 * i] for i in range(int(n))]


def Expand(M, n):
    W = [int(M[n][0 + 8 * j:8 + 8 * j], 16) for j in range(16)]
    W.extend(P1(W[j - 16] ^ W[j - 9] ^ ROL(W[j - 3], 15)) ^ ROL(W[j - 13], 7) ^ W[j - 6] for j in range(16, 68))

    W_ = [W[j] ^ W[j + 4] for j in range(64)]
    Wstr = ''.join(f'{hex(x)[2:]} ' for x in W)
    W_str = ''.join(f'{hex(x)[2:]} ' for x in W_)
    return W, W_


def CF(V, M, i):
    A, B, C, D, E, F, G, H = V[i]
    W, W_ = Expand(M, i)
    for j in range(64):
        SS1 = ROL((ROL(A, 12) + E + ROL(T_(j), j % 32)) % (2 ** 32), 7)
        SS2 = SS1 ^ ROL(A, 12)
        TT1 = (FF(A, B, C, j) + D + SS2 + W_[j]) % (2 ** 32)
        TT2 = (GG(E, F, G, j) + H + SS1 + W[j]) % (2 ** 32)
        D = C
        C = ROL(B, 9)
        B = A
        A = TT1
        H = G
        G = ROL(F, 19)
        F = E
        E = P0(TT2)
    a, b, c, d, e, f, g, h = V[i]
    return [a ^ A, b ^ B, c ^ C, d ^ D, e ^ E, f ^ F, g ^ G, h ^ H]


def Iterate(M):
    """迭代

    """
    n = len(M)
    V = [IV]
    V.extend(CF(V, M, i) for i in range(n))
    return V[n]




def SM3(message):
    m = Fill(message) 
    M = Group(m) 
    Vn = Iterate(M) 
    return ''.join(hex(x)[2:] for x in Vn)