import SM3
import random




def length_extension_atk(hash_m, extension, n):
    Hm = [int(hash_m[i*8:i*8+8], 16) for i in range(8)]
    
    len_e = hex((n + len(extension))*4)[2:]  
    len_e = (16 - len(len_e)) * '0' + len_e

    extension = f'{extension}8'
    extension = extension + '0' * (128 - len(extension) % 128 + 112) + len_e if len(extension) % 128 > 112 else extension + '0' * (112 - len(extension) % 128) + len_e
    ext_g = SM3.Group(extension)      
    n_g = len(ext_g)            
    V = [Hm]
    V.extend(SM3.CF(V, ext_g, i) for i in range(n_g))
    return ''.join(hex(x)[2:] for x in V[n_g])


if __name__ == '__main__':
    secret_message = str(random.randint(0 , 2 ** 128))
    # secret_message = '154343841'
    extension = '7777777'      

    n = (len(secret_message) // 128 + 1) * 128 if len(secret_message) % 128 < 112 else (len(secret_message) // 128 + 2) * 128
    len_m = hex(len(secret_message)*4)[2:]
    len_m = (16 - len(len_m)) * '0' + len_m 

    padding_num = n - len(secret_message) - 16 - 1   

    new_message = f'{secret_message}8' + padding_num * '0' + len_m + extension
    new_hash = SM3.SM3(new_message)

    attack_hash = length_extension_atk(SM3.SM3(secret_message), extension, n) 

    print("The hash of the new message : ", new_hash)
    print("Length extension attack results : ", attack_hash)
    if new_hash == attack_hash:
        print("Length extension attack Success!")
    else:
        print("Length extension attack Fail...")