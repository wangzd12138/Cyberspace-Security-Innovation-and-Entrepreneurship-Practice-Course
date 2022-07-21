#pragma warning(disable:4996)
#include "sm3.h"
#include <stdio.h>
#include<time.h>




void benchmark_sm3(const unsigned char* input, unsigned int iLen, int number) {
    sm3_context ctx;
    int i = 0;
    unsigned char buf[32] = { 0 };
    char hash[65] = { 0 };
    clock_t start_time = clock();

    sm3(input, iLen, buf);

    sm3_init(&ctx);
    sm3_update(&ctx, input, iLen);

    for (i = 0; i < number; i++) { 
        sm3(buf, 31, buf);
        sm3_update(&ctx, buf, i % 32);
    }

    sm3_done(&ctx, buf);
    clock_t end_time = clock();
    printf("进行 %d 次SM3运算需要 %d 时钟周期\n",number,(end_time - start_time));

    for (i = 0; i < 32; i++) {
        sprintf(hash + i * 2, "%02X", (buf[i] & 0x0FF));
    }

    // printf("hash = %s\n", hash);
}


int main(int argc, char** argv) {
    unsigned char test_input[64] = { 0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,
                       0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,
                       0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,
                       0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,
                       0xaa,0xaa,0xaa,0xaa };
    
    benchmark_sm3(test_input, 64, 1000000);


    sm3_context ctx;
    int i = 0;
    unsigned char buf[32] = { 0 };
    char hash[65] = { 0 };
    char* message = "abc";
    // printf("%d\n",strlen(message));
    
    sm3(message, strlen(message), buf);

    for (i = 0; i < 32; i++) {
        sprintf(hash + i * 2, "%02X", (buf[i] & 0x0FF));
    }
    printf("message = %s\n", message);
    printf("hash = %s\n", hash);
    return 0;
}