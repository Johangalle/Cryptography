#!/usr/bin/python3
#
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/
#
#
# This module can be used as an introduction to encryption / decryption.
# Both symmetric and asyymmetric and symmetric encrypt/decrypt operations are supported.
# As cleartext, ciphertext and key material, both byte strings and ints are supported.
#
# For asymmetric encryption, we use a slightl;y modified form of so-called vanilla RSA.
# We use Carmichael lcm (least common multiple) instead of the Euler phi function.
#
# For symmetric encryption, we use xor.
# When you use zor for symmetric encryption, you should use key material of at least
# the same length as the input cleartext material.
#
# No part of this module should be used for cryptography in production.
# This module is strictly for education purposes.
#

from operator import xor
import primes
import euclidean

# to have a good level of security, the key used should have approximately the same length as the plaintext

def byte_xor_old (ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])
    
def byte_xor(ba1, ba2):
    maxlen = max(len(ba1),len(ba2))
    int_ba1 = int.from_bytes(ba1)
    int_ba2 = int.from_bytes(ba2)
    int_xor = int_ba1 ^ int_ba2
    return int_xor.to_bytes(maxlen)

def symmetric_encrypt_xor(plaintext, key):
    if isinstance(plaintext,int) and isinstance(key,int):
        return xor(plaintext, key)
    elif isinstance(plaintext,bytes) and isinstance(key, bytes):
        return byte_xor(plaintext, key)
    else:
        raise ValueError("Both encrypt parameters should be int or both parameters should be bytes")

def show_repr(cipher):
    if isinstance(cipher,int):
        return hex(cipher)
    elif isinstance(cipher, bytes):
        return cipher
    else:
        raise ValueError("Input should be int or bytes")
        
def symmetric_decrypt_xor (ciphertext, key):
    if isinstance(ciphertext,int) and isinstance(key,int):
        return xor(ciphertext, key)
    elif isinstance(ciphertext,bytes) and isinstance(key,bytes):
        return byte_xor(ciphertext, key)
    else:
        raise ValueError("Both decrypt parameters should be int or both parameters should be bytes")

def asymmetric_generate_keys(base = 512):
    p = primes.findAPrime(pow(2,base -1),pow(2,base))
    q = primes.findAPrime(pow(2,base -1),pow(2,base))
    n = p*q
    
    public = 65537
    private = euclidean.mulinv(public,euclidean.lcm((p-1),(q-1)))
    
    return (n, public),(n, private)
    
def asymmetric_encrypt(plaintext, public):
    if isinstance(plaintext,int):
        if plaintext >= public[0] or plaintext < 0:
            raise ValueError("plaintext not between 0 and asymmetric key n value")
        return pow(plaintext,public[1],public[0])
    elif isinstance(plaintext,bytes):
        plain_concat =  b"X" + plaintext
        plaintexti = int.from_bytes(plain_concat,"big")
        if plaintexti >= public[0] or plaintexti < 0:
            raise ValueError("plaintext not between 0 and asymmetric key n value")
        ciphertexti = pow(plaintexti,public[1],public[0])
        nr_of_bytes = (public[0].bit_length() + 7) // 8
        return ciphertexti.to_bytes(nr_of_bytes,"big")
    else:
        raise ValueError("Plaintext encrypt input should be int or bytes")

def asymmetric_decrypt(cipher, private):
    if isinstance(cipher,int):
        return pow(cipher,private[1],private[0])
    elif isinstance(cipher, bytes):
        nr_of_bytes = (private[0].bit_length() + 7) // 8
        cipheri = int.from_bytes(cipher,"big")
        plaini = pow(cipheri,private[1],private[0])
        decrypted = plaini.to_bytes(nr_of_bytes, "big")
        index = decrypted.find(b"X")
        return decrypted[index+1:]
    else:
        raise ValueError("Cipher decrypt input should be int or bytes")
    
if __name__ == '__main__':
    import secrets
    # Int symmetric encrypt / decrypt
    masterkey = secrets.randbits(128)
    plaintext = 0x1234567890abcdeffedcba0987654321
    cipher = symmetric_encrypt_xor(plaintext,masterkey)
    # print ("plaintext in hex:", show_repr(plaintext), " cipher in hex:", show_repr(cipher))
    
    decrypted = symmetric_decrypt_xor(cipher, masterkey)
    assert decrypted == plaintext
    
    # Bytes symmetric encrypt / decrypt
    masterkey = secrets.token_bytes(16)
    plaintext = b"abcdefghijklmnop"
    cipher = symmetric_encrypt_xor(plaintext,masterkey)
    # print ("plaintext ", show_repr(plaintext), " cipher:", show_repr(cipher))
    
    decrypted = symmetric_decrypt_xor(cipher, masterkey)
    assert decrypted == plaintext
    
    # Int asymmetric encrypt / decrypt
    pub, priv = asymmetric_generate_keys()
    plaintext = 0x1234567890abcdeffedcba0987654321
    cipher = asymmetric_encrypt(plaintext, pub)
    # print ("plaintext ", show_repr(plaintext), " cipher:", show_repr(cipher))
    
    decrypted = asymmetric_decrypt(cipher, priv)
    assert decrypted == plaintext
    
    # bytes asymmetric encrypt / decrypt
    pub, priv = asymmetric_generate_keys()
    plaintext = b"abcdefghijklmnop"
    cipher = asymmetric_encrypt(plaintext, pub)
    # print ("plaintext ", show_repr(plaintext), " cipher:", show_repr(cipher))
    
    decrypted = asymmetric_decrypt(cipher, priv)
    assert decrypted == plaintext
