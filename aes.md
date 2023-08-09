# Symmetric encryption and modes of operation
Code snippets to learn cryptography without the need to use other libraries. DO NOT USE IN PRODUCTION

AES (Advanced Encryption System) is the most popular symmetric encryption algorithm.

## Standard AES encryption (no modes of operation, exactly one block)
### Standard AES encryption (lists of integers, no modes of operation)
```
>>> import aes
>>> import secrets
>>> cleartext = [100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115]
>>> key = [143,194,34,208,145,203,230,143,177,246,97,206,145,92,255,84]
>>> my_aes = aes.AES()
>>> cipher = my_aes.encrypt(cleartext,key, my_aes.keySize["SIZE_128"])
>>> decr = my_aes._decrypt(cipher,key, my_aes.keySize["SIZE_128"])
>>> decr == cleartext
True
```
### Standard AES encryption (bytes, no modes of operation, AES-128, cleartext size = 128 bits / 16 bytes)
```
>>> cleartext = b"This is a test! "
>>> len(cleartext)
16
>>> key = secrets.token_bytes(16)
>>> my_aes = aes.AES()
>>> cipher = my_aes.encrypt(cleartext,key, my_aes.keySize["SIZE_128"])
>>> decr = my_aes.decrypt(cipher,key, my_aes.keySize["SIZE_128"])
>>> decr
b'This is a test! '
>>> decr == cleartext
True
```
### Standard AES encryption (bytes, no modes of operation, AES-256, cleartext size = 128 bits / 16 bytes)
```
>>> cleartext = b"This is a test! "
>>> len(cleartext)
16
>>> key = secrets.token_bytes(32)
>>> my_aes = aes.AES()
>>> cipher = my_aes.encrypt(cleartext,key, my_aes.keySize["SIZE_256"])
>>> decr = my_aes.decrypt(cipher,key, my_aes.keySize["SIZE_256"])
>>> decr
b'This is a test! '
>>> decr == cleartext
True
```
### Standard AES encryption (bytes, no modes of operation, AES-256, cleartext size = 17 bytes)
```
>>> cleartext = b"This is a test!  "
>>> len(cleartext)
17
>>> key = secrets.token_bytes(32)
>>> my_aes = aes.AES()
>>> cipher = my_aes.encrypt(cleartext,key, my_aes.keySize["SIZE_256"])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/johangalle/Public/Sources/cryptocourse2/aes.py", line 428, in encrypt
    raise ValueError("block size incorrect in encrypt input")
ValueError: block size incorrect in encrypt input
```
## AES encryption with modes of operation
### Standard AES encryption (key = list of integers, mode of operation CBC, key size 128 bits / 16 bytes)
```
>>> import aesModeOfOperation
>>> import secrets
>>> moo = aesModeOfOperation.AESModeOfOperation()
>>> cleartext = "This is a test! This is a test! This is a test!"
>>> cipherkey = [143,194,34,208,145,203,230,143,177,246,97,206,145,92,255,84]
>>> iv = [103,35,148,239,76,213,47,118,255,222,123,176,106,134,98,92]
>>> mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["CBC"],cipherkey, moo.aes.keySize["SIZE_128"], iv)
>>> decr = moo.decrypt(ciph, orig_len, mode, cipherkey,moo.aes.keySize["SIZE_128"], iv)
>>> decr == cleartext
True
```
### Standard AES encryption (key = list of integers, mode of operation OFB, key size 128 bits / 16 bytes)
```
>>> import aesModeOfOperation
>>> import secrets
>>> moo = aesModeOfOperation.AESModeOfOperation()
>>> cleartext = "This is a test! This is a test! This is a test!"
>>> cipherkey = [143,194,34,208,145,203,230,143,177,246,97,206,145,92,255,84]
>>> iv = [103,35,148,239,76,213,47,118,255,222,123,176,106,134,98,92]
>>> mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["OFB"],cipherkey, moo.aes.keySize["SIZE_128"], iv)
>>> decr = moo.decrypt(ciph, orig_len, mode, cipherkey,moo.aes.keySize["SIZE_128"], iv)
>>> decr == cleartext
True
```
### Standard AES encryption (key = list of integers, mode of operation CFB, key size 128 bits / 16 bytes)
```
>>> import aesModeOfOperation
>>> import secrets
>>> moo = aesModeOfOperation.AESModeOfOperation()
>>> cleartext = "This is a test! This is a test! This is a test!"
>>> cipherkey = [143,194,34,208,145,203,230,143,177,246,97,206,145,92,255,84]
>>> iv = [103,35,148,239,76,213,47,118,255,222,123,176,106,134,98,92]
>>> mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["CFB"],cipherkey, moo.aes.keySize["SIZE_128"], iv)
>>> decr = moo.decrypt(ciph, orig_len, mode, cipherkey,moo.aes.keySize["SIZE_128"], iv)
>>> decr == cleartext
True
```
### Standard AES encryption (key = list of integers, mode of operation CTR, key size 128 bits / 16 bytes)
```
>>> import aesModeOfOperation
>>> import secrets
>>> moo = aesModeOfOperation.AESModeOfOperation()
>>> cleartext = "This is a test! This is a test! This is a test!"
>>> cipherkey = [143,194,34,208,145,203,230,143,177,246,97,206,145,92,255,84]
>>> iv = [103,35,148,239,76,213,47,118,255,222,123,176,106,134,98,92]
>>> mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["CTR"],cipherkey, moo.aes.keySize["SIZE_128"], iv)
>>> decr = moo.decrypt(ciph, orig_len, mode, cipherkey,moo.aes.keySize["SIZE_128"], iv)
>>> decr == cleartext
True
```
### Standard AES encryption (key = bytes, mode of operation CBC, key size 128 bits / 16 bytes)
```
>>> import aesModeOfOperation
>>> import secrets
>>> moo = aesModeOfOperation.AESModeOfOperation()
>>> cleartext = "This is a test! This is a test! This is a test!"
>>> cipherkey = secrets.token_bytes(16)
>>> iv = secrets.token_bytes(16)
>>> mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["CBC"],cipherkey, moo.aes.keySize["SIZE_128"], iv)
>>> decr = moo.decrypt(ciph, orig_len, mode, cipherkey,moo.aes.keySize["SIZE_128"], iv)
>>> decr == cleartext
True
```
### Standard AES encryption (key = bytes, mode of operation CBC, key size 256 bits / 32 bytes)
```
>>> import aesModeOfOperation
>>> import secrets
>>> moo = aesModeOfOperation.AESModeOfOperation()
>>> cleartext = "This is a test! This is a test! This is a test!"
>>> cipherkey = secrets.token_bytes(32)
>>> iv = secrets.token_bytes(16)
>>> mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["CBC"],cipherkey, moo.aes.keySize["SIZE_256"], iv)
>>> decr = moo.decrypt(ciph, orig_len, mode, cipherkey,moo.aes.keySize["SIZE_256"], iv)
>>> decr == cleartext
True
```
### Standard AES encryption (key = bytes, mode of operation CTR, key size 128 bits / 16 bytes)
```
>>> import aesModeOfOperation
>>> import secrets
>>> moo = aesModeOfOperation.AESModeOfOperation()
>>> cleartext = "This is a test! This is a test! This is a test!"
>>> cipherkey = secrets.token_bytes(16)
>>> iv = secrets.token_bytes(16)
>>> mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["CTR"],cipherkey, moo.aes.keySize["SIZE_128"], iv)
>>> decr = moo.decrypt(ciph, orig_len, mode, cipherkey,moo.aes.keySize["SIZE_128"], iv)
>>> decr == cleartext
True
```
### Standard AES encryption (key = bytes, mode of operation CTR, key size 256 bits / 32 bytes)
```
>>> import aesModeOfOperation
>>> import secrets
>>> moo = aesModeOfOperation.AESModeOfOperation()
>>> cleartext = "This is a test! This is a test! This is a test!"
>>> cipherkey = secrets.token_bytes(32)
>>> iv = secrets.token_bytes(16)
>>> mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["CTR"],cipherkey, moo.aes.keySize["SIZE_256"], iv)
>>> decr = moo.decrypt(ciph, orig_len, mode, cipherkey,moo.aes.keySize["SIZE_256"], iv)
>>> decr == cleartext
True
```
## Small symmetric encryption example
A simple symmetric encryption algorithm with block size 128 bits. It consists of 1 round only. 
The sequence of operations is an S-box substitution, a permutation, and an XOR with a key.
* The S-box: see [slide](https://en.wikipedia.org/wiki/Rijndael_S-box)
* The permutation permutes bytes. Say we have b = 0x1234567890, and s = [3,2,4,1,0], then permute (b,s) = 0x5612347890. In this case, we need to permute the 128 bits sequence according to this sequence: [15, 0, 14, 1, 13, 2, 12, 3, 11, 4, 10, 5, 9, 6, 8, 7]
* The key is 0x1032547698BADCFE1032547698BADCFE
* The input is 0x01002300450067008900AB00CD00EF00
* Question: what is the cipher (in hex)?
```
>>> import permute
>>> key = bytes.fromhex('1032547698BADCFE1032547698BADCFE')
>>> input = 0x01002300450067008900AB00CD00EF00
>>> Sbox  = 0x766326636e638563a7636263bd63df63
>>> Sbox = bytes.fromhex('766326636e638563a7636263bd63df63')
>>> per = permute.permute(Sbox, [15, 0, 14, 1, 13, 2, 12, 3, 11, 4, 10, 5, 9, 6, 8, 7])
>>> import basic_crypto
>>> cipher = basic_crypto.byte_xor(per, key)
>>> cipher
b'f\x14:\xf3?\xd8a!sQ7\x15\xfb\xd9\xbf\x9d'
>>> cipher.hex()
'66143af33fd8612173513715fbd9bf9d'
```
