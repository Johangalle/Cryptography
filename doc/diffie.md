# Diffie-Hellman key exchange and Elgamal encryption
Code snippets to learn cryptography without the need to use other libraries. DO NOT USE IN PRODUCTION.

Diffie-Hellman is an interactive protocol that allows to derive a shared secret between two parties. 
The protocol is based on public key cryptography. This shared secret can then be used to derive a symmetric encryption key.
## Diffie-Hellman key exchange
### Diffie-Hellman, discrete logarithm (small numbers)
```
>>> alpha = 7
>>> q = 71
>>> 
>>> XA = 5
>>> YA = pow(alpha,XA,q)
>>> YA
51
>>> 
>>> 
>>> XB = 12
>>> YB = pow(alpha, XB, q)
>>> YB
4
>>> 
>>> 
>>> shared_secret_a = pow(YB, XA, q)
>>> shared_secret_b = pow(YA, XB, q)
>>> shared_secret_a == shared_secret_b
True
>>> shared_secret_a
30
```
### Diffie-Hellman, default example
```
>>> from cryptocourse import basic_dh
>>> a = basic_dh.DiffieHellman()
>>> pub_a = a.gen_public_key()
>>> 
>>> from cryptocourse import basic_dh
>>> b = basic_dh.DiffieHellman()
>>> pub_b = b.gen_public_key()
>>> 
>>> shared_secret_a = a.gen_shared_key(pub_b)
>>> shared_secret_b = b.gen_shared_key(pub_a)
>>> shared_secret_a == shared_secret_b
True
```
### Diffie-Hellman, example with standard group parameters
```
>>> from cryptocourse import basic_dh
>>> a = basic_dh.DiffieHellman(8192,2)
>>> pub_a = a.gen_public_key()
>>> 
>>> from cryptocourse import basic_dh
>>> b = basic_dh.DiffieHellman(8192,2)
>>> pub_b = b.gen_public_key()
>>> 
>>> shared_secret_a = a.gen_shared_key(pub_b)
>>> shared_secret_b = b.gen_shared_key(pub_a)
>>> shared_secret_a == shared_secret_b
True
```
### Transforming a shared secret into key material
```
>>> from cryptocourse import hkdf
>>> hkdf_object = hkdf.Hkdf(None, shared_secret_a)
            # any Diffie-Hellman shared secret may still contain some bias and therefore, this step is required
            # None is the salt
>>> newkey = hkdf_object.expand()
            # There are two (default) parameters:
            # info = b'' (the context to generate the key material
            # length = 32 (in bytes)
>>> new_key
b'X\x97\x08\x17\xa30\xe8\x84\xcf;\xdd\xe8\xa9\xb5O@\x93\xe8\xd8\x1f\xc82\xa4D\x8e\x10\x06))\xc8a\xcb'
```

### Diffie-Hellman, example with non-standard group parameters
```
>>> from cryptocourse import basic_dh
>>> a = basic_dh.DiffieHellman(1024,0)
determining non standard group parameters (takes some time)
>>> b = basic_dh.DiffieHellman()
>>> b.copy(a)
>>> 
>>> pub_a = a.gen_public_key()
>>> pub_b = b.gen_public_key()
>>> 
>>> shared_secret_a = a.gen_shared_key(pub_b)
>>> shared_secret_b = b.gen_shared_key(pub_a)
>>> shared_secret_a == shared_secret_b
True
```
## Asymmetric encryption with Elgamal
```
>>> from cryptocourse import basic_dh
>>> eg_a = basic_dh.ElGamal(4096,3)
>>> eg_b = basic_dh.ElGamal(4096,3)
>>> 
>>> pub = eg_b.gen_public_key()
>>> plain = 123456
>>> cipher = eg_a.enc(plain, pub)
>>> 
>>> decrypt = eg_b.dec(cipher)
>>> decrypt == plain
True
```
