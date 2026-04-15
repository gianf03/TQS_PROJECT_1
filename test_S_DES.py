import bitarray
from sdes import encrypt, decrypt, generate_keys

# Chiave a 10 bit
key = bitarray.bitarray('1010000010')

# Plaintext a 8 bit
plaintext = bitarray.bitarray('11010011')

# Genera i due sotto-chiavi (key1, key2)
key1, key2 = generate_keys(key)

# Cifra
ciphertext = encrypt(plaintext, key1, key2)
print("Ciphertext:", ciphertext)

# Decifra
decrypted = decrypt(ciphertext, key1, key2)
print("Decrypted:", decrypted)