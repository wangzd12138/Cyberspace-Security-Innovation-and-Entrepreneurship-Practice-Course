#include <stdint.h>
typedef struct {
    unsigned int state[8]; // 寄存器中间状态
    unsigned char buf[64]; // 待压缩消息
    unsigned int cur_buf_len; // 当前待压缩消息长度（字节）
    uint64_t compressed_len; // 已压缩消息长度（比特）
}sm3_context;

/**
    * 摘要算法初始化
    */
void sm3_init(sm3_context* ctx);

/**
    * 添加消息
    */
void sm3_update(sm3_context* ctx, const unsigned char* input, unsigned int iLen);

/**
    * 计算摘要
    */
void sm3_done(sm3_context* ctx, unsigned char* output);

/**
    * 直接计算消息的摘要
    */
void sm3(const unsigned char* input, unsigned int iLen, unsigned char* output);