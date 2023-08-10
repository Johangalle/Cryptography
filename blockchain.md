# A smalll blockchain example
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
>>> b0.nonce
0
>>> b0.mine()
>>> b0.nonce
537256
>>> b1 = basic_bc.Block(1,[t3,t4,t5], b0.hash,"participant/miner 1", "sha256",0)
>>> b1.nonce
0
>>> b1.mine()
>>> b1.nonce
276597
>>> b2 = basic_bc.Block(2,[t6,t7], b1.hash,"participant/miner 2", "sha256",0)
>>> b2.nonce
0
>>> b2.mine()
>>> b2.nonce
606870
>>> b3 = basic_bc.Block(3,[t8], b2.hash,"participant/miner 1", "sha256",0)
>>> b3.nonce
0
>>> b3.mine()
>>> b3.nonce
747437
>>> b3.hash
'0000055a72f5a76e664dadb81122e90439ead1bfda40b3e47f5fc26505e4d709'
```
