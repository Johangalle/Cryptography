# Encryption using xor
Code snippets to learn cryptography without the need to use other libraries. DO NOT USE IN PRODUCTION

## XOR symmetric encryption using int
### XOR symmetric encryption using int with equal length
```
>>> import basic_crypto
>>> import secrets
>>> masterkey = secrets.randbits(128)
>>> plaintext = 0x1234567890abcdeffedcba0987654321
>>> len(hex(masterkey))
34
>>> len(hex(plaintext))
34
>>> cipher = basic_crypto.symmetric_encrypt_xor(plaintext,masterkey)
>>> decrypted = basic_crypto.symmetric_decrypt_xor(cipher, masterkey)
>>> decrypted == plaintext
True
```

### XOR symmetric encryption using int with unequal length
```
>>> plaintext = 0x1234567890
>>> len(hex(masterkey)), len(hex(plaintext))
(34, 12)
>>> cipher = basic_crypto.symmetric_encrypt_xor(plaintext,masterkey)
>>> decrypted = basic_crypto.symmetric_decrypt_xor(cipher, masterkey)
>>> decrypted == plaintext
True
>>> 
>>> 
>>> plaintext2 = 0x1234567890abcdeffedcba09876543211234567890abcdeffedcba09876543211234567890abcdeffedcba0987654321
>>> len(hex(masterkey)),len(hex(plaintext2))
(34, 98)
>>> cipher2 = basic_crypto.symmetric_encrypt_xor(plaintext2,masterkey)
>>> decrypted2 = basic_crypto.symmetric_decrypt_xor(cipher2, masterkey)
>>> decrypted2 == plaintext2
True
>>>
>>> hex(masterkey)
'0x97ea0a051f8e9421aa8f0310db5cb825'
>>> hex(plaintext)
'0x1234567890'
>>> hex(cipher)
'0x97ea0a051f8e9421aa8f0302ef0ac0b5'
>>> 
>>> hex(masterkey)
'0x97ea0a051f8e9421aa8f0310db5cb825'
>>> hex(plaintext2)
'0x1234567890abcdeffedcba09876543211234567890abcdeffedcba09876543211234567890abcdeffedcba0987654321'
>>> hex(cipher2)
'0x1234567890abcdeffedcba09876543211234567890abcdeffedcba098765432185de5c7d8f2559ce5453b9195c39fb04'
>>> 
```
### XOR symmetric encryption with ints using a long key and taking the appropriate length each time
...
>>> masterkey = secrets.randbits(1000)
>>> plaintext = 0x1234567890abcdeffedcba
>>> len(hex(masterkey)), len(hex(plaintext))
(252, 24)
>>> hex(plaintext)
'0x1234567890abcdeffedcba'
>>> piece_of_master_key_hex = hex(masterkey)[2:26]
>>> len(piece_of_master_key_hex)
24
>>> offset = 2
>>> true_length_of_plaintext = len(hex(plaintext)) - 2 #Because this representation starts with 0x
>>> true_length_of_plaintext
22
>>> piece_of_master_key_hex = hex(masterkey)[offset:offset+true_length_of_plaintext]
>>> piece_of_master_key = int(piece_of_master_key_hex,16)
>>> len(hex(piece_of_master_key))
24
>>> cipher = basic_crypto.symmetric_encrypt_xor(plaintext, piece_of_master_key)
>>> len(hex(cipher))
24
>>> decrypted = basic_crypto.symmetric_encrypt_xor(cipher, piece_of_master_key)
>>> decrypted == plaintext
True
>>> offset = offset + true_length_of_plaintext
>>> offset    #next time, we start with this offset
24
...
## XOR symmetric encryption using bytes
### XOR symmetric encryption using bytes with equal length
>>> masterkey = secrets.token_bytes(16)
>>> plaintext = b"abcdefghijklmnop"
>>> cipher = basic_crypto.symmetric_encrypt_xor(plaintext,masterkey)
>>> decrypted = basic_crypto.symmetric_decrypt_xor(cipher, masterkey)
>>> decrypted == plaintext
True
>>> len(plaintext), len(masterkey), len(cipher)
(16, 16, 16)
...
### XOR symmetric encryption using bytes with unequal length
...
>>> plaintext = b"12ab34cd56ef"
>>> len(plaintext)
12
>>> cipher = basic_crypto.symmetric_encrypt_xor(plaintext,masterkey)
>>> decrypted = basic_crypto.symmetric_decrypt_xor(cipher, masterkey)
>>> decrypted == plaintext
False
>>> hex(int.from_bytes(decrypted)), hex(int.from_bytes(plaintext))
('0x313261623334636435366566', '0x313261623334636435366566')
>>> hex(int.from_bytes(decrypted)) == hex(int.from_bytes(plaintext))
True
>>> len(decrypted), len(plaintext)
(16, 12)
>>> decrypted
b'\x00\x00\x00\x0012ab34cd56ef'
>>> plaintext
b'12ab34cd56ef'
>>>
>>> plaintext2 = bytes(0x1234567890abcdeffedcba09876543211234567890abcdeffedcba09876543211234567890abcdeffedcba0987654321)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
OverflowError: cannot fit 'int' into an index-sized integer
>>> plaintext2 = bytes.fromhex('1234567890abcdeffedcba09876543211234567890abcdeffedcba09876543211234567890abcdeffedcba0987654321')
>>> len(plaintext2)
48
>>> cipher2 = basic_crypto.symmetric_encrypt_xor(plaintext2,masterkey)
>>> decrypted2 = basic_crypto.symmetric_decrypt_xor(cipher2, masterkey)
>>> decrypted2 == plaintext2
True
...
### XOR symmetric encryption with bytes using a long key and taking the appropriate length each time
...
>>> masterkey = secrets.token_bytes(1000)
>>> plaintext = b"12ab34cd56ef"
>>> len(plaintext)
12
>>> len(plaintext[0:12])
12
>>> offset = 0
>>> length = len(plaintext)
>>> piece_of_master_key = masterkey[offset:offset+length]
>>> piece_of_master_key
b'~\xa7u\xfd\x91\x05\xc9\x9e\xcf\xb0P\xeb'
>>> len(piece_of_master_key)
12
>>> cipher = basic_crypto.symmetric_encrypt_xor(plaintext, piece_of_master_key)
>>> len(cipher)
12
>>> decrypted = basic_crypto.symmetric_decrypt_xor(cipher, piece_of_master_key)
>>> decrypted == plaintext
True
>>> offset = offset + length
...
## Note that encrypt_xor and decrypt_xor are actually identical and are just XOR
...
>>> decrypted = basic_crypto.symmetric_encrypt_xor(cipher, piece_of_master_key)
>>> decrypted == plaintext
True
...
