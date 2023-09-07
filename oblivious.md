# Oblivious transfer (standard, basic) protocol
Code snippets to learn cryptography without the need to use other libraries. DO NOT USE IN PRODUCTION.

Oblivious transfer protocol allows Bob to have two messages M0 and M1. Alice chooses which of the two to receive (0 or 1).

The proper message is transferred from Bob to Alice. Bob cannot deduce which one of the messages Alice is interested in. Alice is only able to read the one (chosen) message.

## Perform oblivious transfer (Bob)
```
>>> from cryptocourse import basic_dh, aesModeOfOperation
>>> M0 = b"qwertyuioplkjhgfdsazxcvbnm"
>>> M1 = b"mnbvcxzlkjhgfdsapoiuytrewq"
>>> Bob = basic_dh.DiffieHellman()
>>> A = Bob.gen_public_key()
>>> A
173630115172759116384179185424067300198702218866936161035986573532475558811878923047678874572723326612027703425476777915949683296751517931297465305204533795318619267748238490097585492676636603304819995896972014459707944852881100504584995675730096209771769203575770952270627585937259294420255924606390703368965
>>> B = 104103657156943446122208061681353528959275088725897153227473425704214411027050127156103859754264979169861520164131752900139140156351940472279889337486720081765520621042482792791954486707137761681391763799662851310809930718467437962235794563256503512368997321085682229110148968169325227278286411639341907544957
>>> K0, K1 = Bob.gen_shared_keys_OT(B)
>>> len(K0), len(K1)
(32, 32)
>>> import secrets
>>> iv1 = secrets.token_bytes(16)
>>> iv2 = secrets.token_bytes(16)
>>> iv1, iv2
(b'\xf7\xf54\x08\x84\xdc\xd2i\xba[\xaes\xdcf\x1d\x9e', b'=\x98\x89\x16ml\x9f\x82\xffV\x08\x05\xebL\x84\xa4')
>>> moo = aesModeOfOperation.AESModeOfOperation()
>>> mode, orig_len, cipher0 = moo.encrypt(M0, moo.modeOfOperation["CTR"],K0, moo.aes.keySize["SIZE_256"], iv1)
>>> mode, orig_len, cipher1 = moo.encrypt(M1, moo.modeOfOperation["CTR"],K1, moo.aes.keySize["SIZE_256"], iv2)
>>> mode, orig_len, cipher0, cipher1
(3, 26, b'y0\xa2I\xbf\x0b\x05$\t?\xf4\xc5\xb4\xa4\xdd\xd3\xd4Q\x19\xd6\xc0e\x8c#\x03\x87', b'\x10g \xf8\x05\xdb\t\xfd_\x8cN%V}\xf3\x9ejE\x91\r\x88\x17]\xfbah')
>>> 
```
## Perform oblivious transfer (Alice)
```
>>> from cryptocourse import basic_dh, aesModeOfOperation
>>> choice = 1 # Alice is interested in the second message
>>> Alice = basic_dh.DiffieHellman()
>>> A = 173630115172759116384179185424067300198702218866936161035986573532475558811878923047678874572723326612027703425476777915949683296751517931297465305204533795318619267748238490097585492676636603304819995896972014459707944852881100504584995675730096209771769203575770952270627585937259294420255924606390703368965
>>> B0, B1 = Alice.gen_public_keys_OT(A)
>>> if choice == 0:
...     B = B0
... else:
...     B = B1
... 
>>> B
104103657156943446122208061681353528959275088725897153227473425704214411027050127156103859754264979169861520164131752900139140156351940472279889337486720081765520621042482792791954486707137761681391763799662851310809930718467437962235794563256503512368997321085682229110148968169325227278286411639341907544957
>>> KR = Alice.gen_shared_key(A)
>>> iv1 , iv2 = b'\xf7\xf54\x08\x84\xdc\xd2i\xba[\xaes\xdcf\x1d\x9e', b'=\x98\x89\x16ml\x9f\x82\xffV\x08\x05\xebL\x84\xa4'
>>> mode, orig_len, cipher0, cipher1 = 3, 26, b'y0\xa2I\xbf\x0b\x05$\t?\xf4\xc5\xb4\xa4\xdd\xd3\xd4Q\x19\xd6\xc0e\x8c#\x03\x87', b'\x10g \xf8\x05\xdb\t\xfd_\x8cN%V}\xf3\x9ejE\x91\r\x88\x17]\xfbah'
>>> moo = aesModeOfOperation.AESModeOfOperation()
>>> decrypt1 = moo.decrypt(cipher1, orig_len, mode, KR, moo.aes.keySize["SIZE_256"], iv2)
>>> decrypt1
b'mnbvcxzlkjhgfdsapoiuytrewq'
```
