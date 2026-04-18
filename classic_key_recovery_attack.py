from sdes import generate_keys, encrypt, decrypt
import bitarray
import time


def brute_force(plaintext, ciphertext):
    
    for key in range(0, 1024):
        bitKey = bin(key)[2:].zfill(10)

        #print()

        subKey1, subKey2 = generate_keys(bitarray.bitarray(bitKey))
        decryption = decrypt(ciphertext, subKey1, subKey2)

        if (decryption == plaintext):
            #print("Chiave usata:\t", bitKey)
            return 



key = bitarray.bitarray("0011100000")
plaintext = bitarray.bitarray("10101010")

subKey1, subKey2 = generate_keys(key)

ciphertext = encrypt(plaintext, subKey1, subKey2)


print("Plaintext:\t", plaintext.to01())
print("Master key:\t", key.to01())
print("Ciphertext:\t", ciphertext.to01())
print("Decryption:\t", decrypt(ciphertext, subKey1, subKey2).to01())


start = time.perf_counter_ns()
brute_force(plaintext, ciphertext)
end = time.perf_counter_ns()

elapsed_time = end - start
print(elapsed_time, " ns")


