# AES symmetric encryption and modes of operation

## Standard AES encryption (no modes of operation)
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
