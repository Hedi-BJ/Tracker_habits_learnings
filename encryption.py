def encrypt_vigenere(key, message):
    encrypted = ""
    index = 0
    for c in message:
        if ord(c) >= 0x20 and ord(c) <= 0x7E:
            encrypted += chr((((ord(c) - 32) + (ord(key[index]) - 32)) % 95) + 32)
            if index < (len(key) - 1):
                index += 1
            else:
                index = 0
    return encrypted

def decrypt_vigenere(key, encrypted):
    message = ""
    index = 0
    for c in encrypted:
        if ord(c) >= 0x20 and ord(c) <= 0x7E:
            message += chr((((ord(c) - 32) - (ord(key[index]) - 32)) % 95) + 32)
            if index < (len(key) - 1):
                index += 1
            else:
                index = 0
    return message

if __name__ == "__main__":
    print(encrypt_vigenere('abcdefgh', 'python iter() and yied'))
    print(decrypt_vigenere('abcdefgh', encrypt_vigenere('abcdefgh', 'python iter() and yied')))