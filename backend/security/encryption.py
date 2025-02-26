from pqcrypto.kem.kyber import encrypt, decrypt

def secure_data_transfer(data):
    ciphertext, key = encrypt(data)
    return ciphertext
