import hashlib
import struct
import sha256

KEY = b"KEYSUPER"
Key_length = 32
Original_Message = b"This Is An Original Message"
Extension = "I am the dragon"

def generate():
    h = hashlib.new('sha256')
    h.update(KEY)
    h.update(Original_Message)
    
    return Original_Message, h.hexdigest()

def check(message, hashValue):
    h = hashlib.new('sha256')
    h.update(KEY + message)

    if (hashValue == h.hexdigest()):
        print("   Received message:", message)
        print("   Recevied hash:", hashValue)
        print("   Calculateed the hash with secret key:", h.hexdigest())
        return True
    else:
        return False

class Padding:
    def __init__(self):
        self._message_byte_length = 0

    def pad(self, message):
        
        message_byte_length = self._message_byte_length + len(message)

        message += b'\x80'
        message += b'\x00' * ((56 - (message_byte_length + 1) % 64) % 64)

        message_bit_length = message_byte_length * 8
        message += struct.pack(b'>Q', message_bit_length)

        return message


def attack(origin_message, originHash, keyLen):

    pad = Padding()

    tmpStr = ('A' * keyLen).encode()
    attack_message = pad.pad(tmpStr + origin_message)[keyLen:] + Extension.encode()

    sha = sha256.Sha256(Extension, originHash.encode())
    attackHash = sha.sha256
    
    return attack_message, attackHash


if __name__ == "__main__":
    
    origin_message, origin_Hash = generate()
    print("Initial hash value correctness verification : ")
    check(origin_message, origin_Hash)

    print("Start length extension attack...")
    for keyLen in range(Key_length):
        attack_message, attackHash = attack(origin_message, origin_Hash, keyLen)
        if check(attack_message, attackHash) :
            print("Length extension attack Success!!!")
            print("keyLen:", keyLen)
            break
        elif keyLen >= Key_length:
            print("Length extension attack Fail...")