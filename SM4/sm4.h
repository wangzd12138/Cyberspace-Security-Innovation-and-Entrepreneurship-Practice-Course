
typedef struct {
	unsigned int rk[32];
} sm4_context;


/**
	* sm4�ӽ����㷨
	* @param forEncryption 1Ϊ���ܣ�����Ϊ����
	*/
void  sm4_crypt(const unsigned char* key, int forEncryption, const unsigned char* in, unsigned char* out);