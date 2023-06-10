# Cryptography
Code snippets to learn cryptography without the need to use other libraries. DO NOT USE IN PRODUCTION

## The easiest (symmetric_xor) symmetric encryption algorithm
```
>>> import basic_crypto
>>> import secrets
>>> masterkey = secrets.token_bytes(16) # if you want to generate a random 16 bytes sequence
>>> masterkey = b"mfhskrncdsognwz".     # if you want to specify the key yourself
>>> cipher = basic_crypto.symmetric_encrypt_xor(plaintext,masterkey)
>>> decrypted = basic_crypto.symmetric_decrypt_xor(cipher, masterkey)
```

## We continue with asymmetric encryption algorithm
```
>>> import basic_crypto
>>> pub, priv = basic_crypto.asymmetric_generate_keys()
>>> plaintext = b"abcdefghijklmnop"
>>> cipher = basic_crypto.asymmetric_encrypt(plaintext, pub)  # you should give the public key to anyone who wants to encrypt
>>> decrypted = basic_crypto.asymmetric_decrypt(cipher, priv) # the only party who can decrypt, is the one in possession of the private key matching the public key
```

## We now take the most popular symmetric encryption algorithm: AES. 
### Note that the input size must be exactly equal to 128 bits
```
>>> import aes
>>> import secrets
>>> cleartext = b"This is a test! " # this is exactly 16 bytes = 128 bits
>>> key = secrets.token_bytes(32)
>>> enc = aes.AES()
>>> cipher = enc.encrypt(cleartext,key, enc.keySize["SIZE_256"])
>>> decr = enc.decrypt(cipher,key, enc.keySize["SIZE_256"])
```

## Now we solve the issue of the fixed block size by using so-called modes of operation
```
>>> import secrets
>>> import aesModeOfOperation
>>> moo = aesModeOfOperation.AESModeOfOperation()
>>> cleartext = b"This is a test! This is a test! This is a test!"
>>> cipherkey = secrets.token_bytes(16)
>>> iv = secrets.token_bytes(16)
>>> mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["CBC"], cipherkey, moo.aes.keySize["SIZE_128"], iv)
>>> decr = moo.decrypt(ciph, orig_len, mode, cipherkey, moo.aes.keySize["SIZE_128"], iv)
```

## Diffie-Hellman is used to generate shared secrets by exchanging only public key information
```
>>> import basic_dh
>>> a = basic_dh.DiffieHellman(2048,7)
>>> b = basic_dh.DiffieHellman(2048,7)
>>> puba = a.gen_public_key()
>>> pubb = b.gen_public_key()
>>> shared_secret_ab = a.gen_shared_key(pubb)
>>> shared_secret_ba = b.gen_shared_key(puba)
```

## In case you need to convert key material of size x into key material of size y, use HKDF
```
import secrets
import hkdf
input = secrets.token_bytes(16)
output = hkdf.Hkdf.(None,input)
```

## In case you need to convert int to bytes or bytes to int or int to hex-string or hex-string to int
```
>>> b = b"this is a byte string"
>>> i = int.from_bytes(b)
>>> i
170130276577738348141904353322542212591924105801319
>>> i_bytes = i.to_bytes((i.bit_length()+7)//8,"big")
>>> i_bytes
b'this is a byte string'
>>> hs = hex(i)
>>> hs
'0x746869732069732061206279746520737472696e67'
>>> i_fromh = int(hs[2:],16)
>>> i_fromh
170130276577738348141904353322542212591924105801319
j = 0x746869732069732061206279746520737472696e67 # you can also just create an int using the hex representation
```

## Elliptical Curve Cryptogtraphy is an alternative method that can also be used for Diffie-Hellman
```
>>> import basic_ec
>>> ec = basic_ec.StandardECS["secp256k1"]
>>> g = basic_ec.StandardBasePoints["secp256k1"]
>>> a = basic_ec.DiffieHellman(ec,g)
>>> b = basic_ec.DiffieHellman(ec,g)
>>> puba = a.gen_public_key()
>>> pubb = b.gen_public_key()
>>> shared_secret_ab = a.gen_shared_key(pubb)
>>> shared_secret_ba = b.gen_shared_key(puba)
```

## We use ECDSA (Elliptical Curve Cryptography Digital Signature Algorithm for digitally signing information
```
>>> import basic_ec
>>> ec = basic_ec.StandardECS["secp256k1"]
>>> g = basic_ec.StandardBasePoints["secp256k1"]
>>> d_sender = basic_ec.DSA(ec, g)
>>> public = d_sender.gen_public_key()
>>> signature = d_sender.sign(127,7)
>>> d_receiver = basic_ec.DSA(ec,g)
>>> d_receiver.validate(127,signature,public)
True
```

## In order to digitally sign in practice, you need a hash algorithm
### This can be done using a standard Python library
```
>>> import hashlib
>>> m1 = hashlib.sha3_256()
>>> message = b"this is not a secret, but you can calculate its hash so that you can compare it at a later stage"
>>> m1.update(message)
>>> # Try all three versions, but most of the time, you need an integer (third form)
>>> hash1 = m1.digest()
>>> hash2 = m1.hexdigest()
>>> hash3 = int.from_bytes(m1.digest())
```

## We create a blockchain of simple transactions.
### We also have identities, and each identity has a public key.
```
>>> import basic_bc
>>> me = basic_bc.MyIdentity("me",1)
>>> you = basic_bc.MyIdentity("you",2)
>>> him = basic_bc.MyIdentity("him",3)
>>> her = basic_bc.MyIdentity("her",4)
>>> me_pub = me.get_public_key()
>>> you_pub = you.get_public_key()
>>> him_pub = him.get_public_key()
>>> her_pub = her.get_public_key()
>>> t1 = basic_bc.MyTransaction(me,you,100)
>>> t1.sign()
>>> t2 = basic_bc.MyTransaction(me,him,30)
>>> t2.sign()
>>> t3 = basic_bc.MyTransaction(me,her,50)
>>> t3.sign()
>>> t4 = basic_bc.MyTransaction(you,him,20)
>>> t4.sign()
>>> t5 = basic_bc.MyTransaction(you,her,70)
>>> t5.sign()
>>> t6 = basic_bc.MyTransaction(him, her, 10)
>>> t6.sign()
>>> t7 = basic_bc.MyTransaction(her,you,20)
>>> t7.sign()
>>> t8 = basic_bc.MyTransaction(him,me,15)
>>> t8.sign()
>>> b0 = basic_bc.Block(0,[t1,t2], '0'*40,"genesis", "sha1",0)
>>> b0.mine()
>>> b1 = basic_bc.Block(1,[t3,t4,t5], b0.hash,"participant/miner 1", "sha256",0)
>>> b1.mine()
>>> b2 = basic_bc.Block(2,[t6,t7], b1.hash,"participant/miner 2", "sha256",0)
>>> b2.mine()
>>> b3 = basic_bc.Block(3,[t8], b2.hash,"participant/miner 1", "sha256",0)
>>> b3.mine()
>>> b3.hash
```
