# Hashing (including password hashing)
Code snippets to learn cryptography without the need to use other libraries. DO NOT USE IN PRODUCTION.

Hashing is a building block of many cryptograpohic constructs.

## Standard (cryptographic) hashing
```
>>> import hashlib
>>> m1 = hashlib.sha3_256()
>>> message = b"this is not a secret, but you can calculate its hash so that you can compare it at a later stage"
>>> m1.update(message)
>>> # Try all three versions, but most of the time, you need an integer (third form)
>>> hash1 = m1.digest()
>>> hash2 = m1.hexdigest()      # You could also do hash1.hex()
>>> hash3 = int.from_bytes(m1.digest())
>>> hash1
b'4 \xc9\xfc\xdd\xc0\xfc@\x06\xdc\xa1\x97\xca\xe9\xedX/s\x08\xcb?\x00Zb\x8a\xde1\x9b\x19\xde\x0c\x83'
>>> hash2
'3420c9fcddc0fc4006dca197cae9ed582f7308cb3f005a628ade319b19de0c83'
>>> hash3
23578201300678431547034496817196648039679733236024582416831510072713507900547
>>> hash1.hex()
'3420c9fcddc0fc4006dca197cae9ed582f7308cb3f005a628ade319b19de0c83'
```
## Hashing algorithms
```
>>> hashlib.algorithms_guaranteed
{'sha384', 'sha256', 'shake_128', 'blake2s', 'sha512', 'shake_256', 'sha3_384', 'md5', 'sha3_512', 'sha224', 'sha3_224', 'sha3_256', 'blake2b', 'sha1'}
>>> hashlib.algorithms_available
{'sha256', 'whirlpool', 'md5', 'sha3_512', 'sha512_256', 'blake2s', 'sm3', 'sha3_256', 'shake_128', 'sha224', 'md4', 'ripemd160', 'blake2b', 'sha512_224', 'sha384', 'sha512', 'shake_256', 'sha3_384', 'md5-sha1', 'sha3_224', 'sha1'}
```
## Password hashing with Argon2 or with PBKDF2
```
>>> from cryptocourse import argon2
>>> pw_hash = argon2.argon2(b"password", b"salt", 20, 1000, 1)    # 20 is the number of iterations, 1000 is the memory cost, 1 is the amount of threads
>>> pw_hash
b'\xb1\xd9\x1b\x0e\x8f\x07\x9f\x92\x05\xe9\x80\xa1\xbd\xfc\xdcg\x92\xce\xc1~i\x99\x90\x06\xef\xf1\xc6\xa9A\xad\nr'
>>> pw_hash.hex()
'b1d91b0e8f079f9205e980a1bdfcdc6792cec17e69999006eff1c6a941ad0a72'
>>> len(pw_hash)                # It is possible to add a parameter supplying the length required. 32 bytes = 256 bits
32
>>> pw_hash = argon2.argon2(b"password", b"salt", 20, 1000, 1, tag_length = 64)
>>> pw_hash
b'~\x06\x93\xc0\x8d\x19f\x9a \xde\x14:J\xed\xa8\x84\x18\xd6\xd8S\xe1\x11\x81\xdd\x98yS\x95}Xe\x97\xe6\xc5&\x18y\xd0\xa6\xe7\xb6m\xbdo[U\xf9keBtUo8/Gr\xa7\xd9=\xc5\xa3\x82\xc3'
>>> len(pw_hash)
64
>>> import hashlib
>>> pw_hash = hashlib.pbkdf2_hmac("sha256", b"password", b"salt", 1000)    # PBKDF2, password based key derivation function 2, is also a popular password hashing algorithm
>>> pw_hash
b'c,(\x12\xe4mF\x04\x10+\xa7a\x8e\x9dm}/\x81(\xf6&kJ\x03&M*\x04`\xb7\xdc\xb3'
```
