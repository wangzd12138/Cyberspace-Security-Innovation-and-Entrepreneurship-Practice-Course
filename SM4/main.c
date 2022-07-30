#pragma warning(disable:4996)
#include "sm4.h"
#include <stdio.h>
#include<time.h>

void benchmark_sm4(const unsigned char* key, int forEncryption,const unsigned char* input, int number) {

    int i = 0;
    unsigned char buf[16] = { 0 };
    char hash[33] = { 0 };

    memcpy(buf, input, 16);

    clock_t start_time = clock();

    for (i = 0; i < number; i++) {
        sm4_crypt(key, forEncryption, buf, buf);
    }

    clock_t end_time = clock();
    printf("进行 %d 次SM4加密需要 %d s\n", number, (end_time - start_time)/ CLOCKS_PER_SEC);
    /*
    for (i = 0; i < 16; i++) {
        sprintf(hash + i * 2, "%02X", (buf[i] & 0x0FF));
    }

    printf("hash = %s\n", hash);*/
}

int main() {
    unsigned char key[16] = {
            0x6B, 0x8B, 0x45, 0x67, 0x32, 0x7B, 0x23, 0xC6,
            0x64, 0x3C, 0x98, 0x69, 0x66, 0x33, 0x48, 0x73
    };
    unsigned char input[16] = {
        0x74, 0xB0, 0xDC, 0x51, 0x19, 0x49, 0x5C, 0xFF,
        0x2A, 0xE8, 0x94, 0x4A, 0x62, 0x55, 0x58, 0xEC
    };
    benchmark_sm4(key, 1, input,10000000);
    
    unsigned char buf[16] = { 0 };
    char hash[33] = { 0 };

    memcpy(buf, input, 16);
    sm4_crypt(key, 1, buf, buf);

    for (int i = 0; i < 16; i++) {
        sprintf(hash + i * 2, "%02X", (buf[i] & 0x0FF));
    }

    printf("hash = %s\n", hash);
    
}