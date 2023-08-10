# Elliptical curve cryptography
Code snippets to learn cryptography without the need to use other libraries. DO NOT USE IN PRODUCTION.

Elliptical curve is an alternative asymmetric encryption (or public key) algorithm. 
The reason for switching to elliptical is mainly because key sizes and performance are better for equal security.
Today, nobody still switches to elliptical because elliptical will be the first to be broken by a quantum computer.

Both elliptical and RSA are vulnerable to quantum attacks and will be replaced by other ( so-called postquantum cryptography) algorithms.

Elliptical curve cryptography is used for digital signature and key exchange, but is almost never used for encryption.

## Calculating with elliptical curves
```
>>> import basic_ec
>>> ec = basic_ec.StandardECS["secp256k1"]
>>> g = basic_ec.StandardBasePoints["secp256k1"]
>>> p = ec.mul(g,175000)
>>> p
Coord(x=78707596058261779084730250443339338769012516617671603792896826294246574460172, y=3240371869283042980224711801654570442889808188459581777163013544869753704814)
>>> q = ec.mul(g,325000)
>>> q
Coord(x=30757424214649016781486017169121183180296657608166595477311176357837774811655, y=25106589518167554550818752977796974764376091154002455502790839722891120847914)
>>> r1 = ec.add(p, q)
>>> r1
Coord(x=51820831388699414484946106851605147061940830728796901990555973801205894159136, y=54826908012524478572953314389919633950822601775097944649489449596046825198781)
>>> r2 = ec.mul(g, 500000)
>>> r2
Coord(x=51820831388699414484946106851605147061940830728796901990555973801205894159136, y=54826908012524478572953314389919633950822601775097944649489449596046825198781)
>>> r1 == r2
True
```
## Elliptical Diffie-Hellman
```
>>> import basic_ec
>>> ec = basic_ec.StandardECS["secp256k1"]
>>> g = basic_ec.StandardBasePoints["secp256k1"]
>>> 
>>> a = basic_ec.DiffieHellman(ec, g)
>>> b = basic_ec.DiffieHellman(ec, g)
>>> 
>>> pub_a = a.gen_public_key()
>>> pub_b = b.gen_public_key()
>>> 
>>> shared_secret_a = a.gen_shared_key(pub_b)
>>> shared_secret_b = b.gen_shared_key(pub_a)
>>> 
>>> shared_secret_a == shared_secret_b
True
```
## Transforming a shared secret into key material
```
>>> import hkdf
>>> new_key = hkdf.Hkdf(None, shared_secret_a)   # any Diffie-Hellman shared secret may still contain some bias and therefore, this step is required
                                                 # None is the salt
```
## Elgamal elliptical curve encryption
```
>>> import basic_ec
>>> ec = basic_ec.StandardECS["secp256k1"]
>>> g = basic_ec.StandardBasePoints["secp256k1"]
>>> 
>>> receiver_eg = basic_ec.ElGamal(ec, g)
>>> receiver_eg.gen_private_key()
>>> receiver_public_key = receiver_eg.gen_public_key()
>>> 
>>> sender_eg = basic_ec.ElGamal(ec, g)
>>> plain, _ = ec.at(2)    # the element to be encrypted should be a point on the elliptical curve
>>> plain
Coord(x=2, y=69211104694897500952317515077652022726490027694212560352756646854116994689233)
>>> 
>>> cipher = sender_eg.enc(plain, receiver_public_key)
>>> 
>>> decrypted = receiver_eg.dec(cipher)
>>> decrypted
Coord(x=2, y=69211104694897500952317515077652022726490027694212560352756646854116994689233)
>>> decrypted == plain
True
```
## ECDSA (Elliptical Curve Digital Signature)
```
>>> import basic_ec
>>> ec = basic_ec.StandardECS["secp256k1"]
>>> g = basic_ec.StandardBasePoints["secp256k1"]
>>> 
>>> d_sender = basic_ec.DSA(ec, g)
>>> public_sender = d_sender.gen_public_key()
>>> 
>>> message = b"hello"
>>> import hashlib
>>> m1 = hashlib.sha3_256()
>>> m1.update(message)
>>> hash_value = int.from_bytes(m1.digest())
>>> 
>>> import random
>>> signature = d_sender.sign(hash_value,random.randint(1,1000000))   # signatures always contain a random element; signing the same message twice results in two different signatures
>>> 
>>> d_receiver = basic_ec.DSA(ec, g)
>>> d_receiver.validate(hash_value,signature, public_sender)
True
>>> d_receiver.validate(hash_value+1,signature, public_sender)
False
```
## Elliptical curves supplied in basic_ec
```
"Anomalous"
"P-192"
"P-224"
"P-256"
"P-384"
"secp256k1"
"BN(2,254)"
"brainpoolP256t1"
"FRP256v1"
"brainpoolP384t1"
```
