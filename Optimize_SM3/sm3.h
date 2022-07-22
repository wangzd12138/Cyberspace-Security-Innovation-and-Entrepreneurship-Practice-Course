#include <stdint.h>
typedef struct {
    unsigned int state[8]; // �Ĵ����м�״̬
    unsigned char buf[64]; // ��ѹ����Ϣ
    unsigned int cur_buf_len; // ��ǰ��ѹ����Ϣ���ȣ��ֽڣ�
    uint64_t compressed_len; // ��ѹ����Ϣ���ȣ����أ�
}sm3_context;

/**
    * ժҪ�㷨��ʼ��
    */
void sm3_init(sm3_context* ctx);

/**
    * �����Ϣ
    */
void sm3_update(sm3_context* ctx, const unsigned char* input, unsigned int iLen);

/**
    * ����ժҪ
    */
void sm3_done(sm3_context* ctx, unsigned char* output);

/**
    * ֱ�Ӽ�����Ϣ��ժҪ
    */
void sm3(const unsigned char* input, unsigned int iLen, unsigned char* output);