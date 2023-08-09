# Stream cipher encryption
Code snippets to learn cryptography without the need to use other libraries. DO NOT USE IN PRODUCTION.

Stream ciphers essentially require you to generate a pseudo-random stream and to XOR this with plaintext / ciphertext.

Modern stream ciphers also have an initialisation. This is not shown in these (simple) examples.

LFSR (Linear Feedback Shift Registers) are a component opf modern stream ciphers. As a standalone means, they are not a suitable stream cipher.

## Obtain some stream of bytes and xor it with plain / cipher
```
>>> import random
>>> secret_number = 123456789
>>> random.seed(secret_number)    # to ensure that the other side can generate the same pseudo-random number 
>>> full_stream = random.randbytes(1000)
>>> plain = b"some very secret plaintext that I want to encrypt using a stream"
>>> len(plain)
64
>>> offset = 0
>>> part_of_stream = full_stream[offset:offset+len(plain)]
>>> import basic_crypto
>>> cipher = basic_crypto.byte_xor(plain, part_of_stream)   # Remember there is no Python XOR operation for bytes
>>> cipher
b'\xc4\xbb_\xc1\\\x01]\x03\x06\xca\xbf\xef\xa8\xd1\xda\xc1\xa1\xc8,\x9fh,i\x82J+\xff\xa3A\xa7\xa5\xca.\xeb\xba\xae}\xad>\xeeb\r\xc8\x0bi\xe2\x94\x8c|W\x90\x9c\xa20\xadmp(\x1a\xc4y\xbe\x19\x1a'
>>> decrypt = basic_crypto.byte_xor(cipher, part_of_stream)
>>> decrypt
b'some very secret plaintext that I want to encrypt using a stream'
>>> decrypt == plain
True
>>> offset = offset + len(plain)     # Do not reuse the same part of a stream more than once
>>> 
```
## Use a linear feedback shift register as stream cipher
```
>>> import permute
>>> seed = 0x12345678    # this is a 32 bit number; seed.bit_length() is actually 29, so the first 3 bits are 0
>>> mask = 0b10000000000000000000000000000100   # these are 32 bits; shift forward of the lfsr transforms s0-s31 by calculating s32 = s0 + s29 and dropping s0.
>>> result = permute.lfsr(seed, mask, 100*32)   # we generate 100 times 32 bits
>>> plain = b"some very secret plaintext that I want to encrypt using a stream"
>>> offset = 0
>>> part_of_stream = result[offset:offset+len(plain)]
>>> len(plain), len(part_of_stream)
(64, 64)
>>> import basic_crypto
>>> cipher = basic_crypto.byte_xor(plain, part_of_stream)
>>> decrypt = basic_crypto.byte_xor(cipher, part_of_stream)
>>> decrypt
b'some very secret plaintext that I want to encrypt using a stream'
>>> decrypt == plain
True
>>> offset = offset + len(plain)
```
