
typedef struct {
	unsigned int rk[32];
} sm4_context;


/**
	* sm4加解密算法
	* @param forEncryption 1为加密，否则为解密
	*/
void  sm4_crypt(const unsigned char* key, int forEncryption, const unsigned char* in, unsigned char* out);