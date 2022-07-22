#include "sm3.h"

#define SM3_IV_A 0x7380166f
#define SM3_IV_B 0x4914b2b9
#define SM3_IV_C 0x172442d7
#define SM3_IV_D 0xda8a0600
#define SM3_IV_E 0xa96f30bc
#define SM3_IV_F 0x163138aa
#define SM3_IV_G 0xe38dee4d
#define SM3_IV_H 0xb0fb0e4e

#define SM3_T_0 0x79CC4519
#define SM3_T_1 0x7A879D8A

#define SM3_FF_0(x,y,z) ( (x) ^ (y) ^ (z) )
#define SM3_FF_1(x,y,z) ( ( (x) & (y) ) | ( (x) & (z) ) | ( (y) & (z) ) )

#define SM3_GG_0(x,y,z) ( (x) ^ (y) ^ (z) )
#define SM3_GG_1(x,y,z) ( ( (x) & (y) ) | ( (~(x)) & (z) ) )

#define  SM3_SHL(x,n) (((x) & 0xFFFFFFFF) << (n % 32))
#define  SM3_ROTL(x,n) ( SM3_SHL((x),n) | ((x) >> (32 - (n % 32))))

#define  SM3_P_0(x) ((x) ^   SM3_ROTL((x),9) ^  SM3_ROTL((x),17))
#define  SM3_P_1(x) ((x) ^   SM3_ROTL((x),15) ^  SM3_ROTL((x),23))

#ifndef  GET_UINT32_BE
#define  GET_UINT32_BE(n,b,i)                         \
{                                                       \
    (n) = ( (uint32_t) (b)[(i)    ] << 24 )             \
        | ( (uint32_t) (b)[(i) + 1] << 16 )             \
        | ( (uint32_t) (b)[(i) + 2] <<  8 )             \
        | ( (uint32_t) (b)[(i) + 3]       );            \
}
#endif

#ifndef  PUT_UINT32_BE
#define  PUT_UINT32_BE(n, b ,i)                            \
{                                                       \
    (b)[(i)    ] = (unsigned char) ( (n) >> 24 );       \
    (b)[(i) + 1] = (unsigned char) ( (n) >> 16 );       \
    (b)[(i) + 2] = (unsigned char) ( (n) >>  8 );       \
    (b)[(i) + 3] = (unsigned char) ( (n)       );       \
}
#endif

static void sm3_BiToW(const unsigned char* Bi, unsigned int* W)
{
    int i;
    unsigned int tmp;
     GET_UINT32_BE(W[0], Bi, 0);
     GET_UINT32_BE(W[1], Bi, 4);
     GET_UINT32_BE(W[2], Bi, 8);
     GET_UINT32_BE(W[3], Bi, 12);
     GET_UINT32_BE(W[4], Bi, 16);
     GET_UINT32_BE(W[5], Bi, 20);
     GET_UINT32_BE(W[6], Bi, 24);
     GET_UINT32_BE(W[7], Bi, 28);
     GET_UINT32_BE(W[8], Bi, 32);
     GET_UINT32_BE(W[9], Bi, 36);
     GET_UINT32_BE(W[10], Bi, 40);
     GET_UINT32_BE(W[11], Bi, 44);
     GET_UINT32_BE(W[12], Bi, 48);
     GET_UINT32_BE(W[13], Bi, 52);
     GET_UINT32_BE(W[14], Bi, 56);
     GET_UINT32_BE(W[15], Bi, 60);

    for (i = 16; i <= 67; i++)
    {
        tmp = W[i - 16] ^ W[i - 9] ^  SM3_ROTL(W[i - 3], 15);
        W[i] =  SM3_P_1(tmp) ^ ( SM3_ROTL(W[i - 13], 7)) ^ W[i - 6];
    }
}

static void sm3_WToW1(const unsigned int* W, unsigned int* W1)
{
    int i;

    for (i = 0; i <= 63; i++)
    {
        W1[i] = W[i] ^ W[i + 4];
    }
}

static void sm3_CF(const unsigned int* W, const unsigned int* W1, sm3_context* ctx)
{
    unsigned int SS1;
    unsigned int SS2;
    unsigned int TT1;
    unsigned int TT2;
    unsigned int A, B, C, D, E, F, G, H;
    unsigned int Tj;
    int j;

    A = ctx->state[0];
    B = ctx->state[1];
    C = ctx->state[2];
    D = ctx->state[3];
    E = ctx->state[4];
    F = ctx->state[5];
    G = ctx->state[6];
    H = ctx->state[7];

    for (j = 0; j < 64; j++)
    {
        if (j < 16)
        {
            Tj =  SM3_T_0;
        }
        else
        {
            Tj =  SM3_T_1;
        }
        SS1 =  SM3_ROTL(( SM3_ROTL(A, 12) + E +  SM3_ROTL(Tj, j)), 7);
        SS2 = SS1 ^  SM3_ROTL(A, 12);

        if (j < 16)
        {
            TT1 =  SM3_FF_0(A, B, C) + D + SS2 + W1[j];
            TT2 =  SM3_GG_0(E, F, G) + H + SS1 + W[j];
        }
        else
        {
            TT1 =  SM3_FF_1(A, B, C) + D + SS2 + W1[j];
            TT2 =  SM3_GG_1(E, F, G) + H + SS1 + W[j];
        }

        D = C;
        C =  SM3_ROTL(B, 9);
        B = A;
        A = TT1;
        H = G;
        G =  SM3_ROTL(F, 19);
        F = E;
        E =  SM3_P_0(TT2);
    }

    ctx->state[0] ^= A;
    ctx->state[1] ^= B;
    ctx->state[2] ^= C;
    ctx->state[3] ^= D;
    ctx->state[4] ^= E;
    ctx->state[5] ^= F;
    ctx->state[6] ^= G;
    ctx->state[7] ^= H;
}

static void sm3_compress(sm3_context* ctx)
{
    unsigned int W[68];
    unsigned int W1[64];

    sm3_BiToW(ctx->buf, W);

    sm3_WToW1(W, W1);

    sm3_CF(W, W1, ctx);
}

void sm3_init(sm3_context* ctx) {
    ctx->state[0] =  SM3_IV_A;
    ctx->state[1] =  SM3_IV_B;
    ctx->state[2] =  SM3_IV_C;
    ctx->state[3] =  SM3_IV_D;
    ctx->state[4] =  SM3_IV_E;
    ctx->state[5] =  SM3_IV_F;
    ctx->state[6] =  SM3_IV_G;
    ctx->state[7] =  SM3_IV_H;
    ctx->cur_buf_len = 0;
    ctx->compressed_len = 0;
}

void sm3_update(sm3_context* ctx, const unsigned char* input, unsigned int iLen) {
    while (iLen--)
    {
        ctx->buf[ctx->cur_buf_len] = *input++;
        ctx->cur_buf_len++;

        if (ctx->cur_buf_len == 64)
        {
            sm3_compress(ctx);
            ctx->compressed_len += 512;
            ctx->cur_buf_len = 0;
        }
    }
}

static const unsigned char sm3_padding[64] = {
        0x80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
};

void sm3_done(sm3_context* ctx, unsigned char* output) {
    uint32_t padn;
    unsigned char msglen[8];
    uint64_t total_len, high, low;

    total_len = ctx->compressed_len + (ctx->cur_buf_len << 3);
    high = (total_len >> 32) & 0x0FFFFFFFF;
    low = total_len & 0x0FFFFFFFF;

     PUT_UINT32_BE(high, msglen, 0);
     PUT_UINT32_BE(low, msglen, 4);

    padn = ((ctx->cur_buf_len + 1) < 56) ? (56 - ctx->cur_buf_len) : (120 - ctx->cur_buf_len);

    sm3_update(ctx, (unsigned char*)sm3_padding, padn);
    sm3_update(ctx, msglen, 8);

     PUT_UINT32_BE(ctx->state[0], output, 0);
     PUT_UINT32_BE(ctx->state[1], output, 4);
     PUT_UINT32_BE(ctx->state[2], output, 8);
     PUT_UINT32_BE(ctx->state[3], output, 12);
     PUT_UINT32_BE(ctx->state[4], output, 16);
     PUT_UINT32_BE(ctx->state[5], output, 20);
     PUT_UINT32_BE(ctx->state[6], output, 24);
     PUT_UINT32_BE(ctx->state[7], output, 28);
}

void sm3(const unsigned char* input, unsigned int iLen, unsigned char* output) {
    sm3_context ctx;
    sm3_init(&ctx);
    sm3_update(&ctx, input, iLen);
    sm3_done(&ctx, output);
}