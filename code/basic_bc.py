#!/usr/bin/python3
#
# Based on several implementations:
# - Juan Cruz Martinez blockchain in Python: https://gist.github.com/bajcmartinez/b3a6113721962a8d1d3b4b3f221ff567
# - Kennedy Kairu Kariuki blockchain implementation: https://github.com/kkairu/blockchain
# - Develop a blockchain application from scratch in Python: https://zhangruochi.com/Develop-a-blockchain-application-from-scratch-in-Python/2020/04/21/
#
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/
#
# This module supports the functions required to construct and build a blockchain.
# The blockchain is a list of elements of class Block.
# A Block contains elements of class Transaction.
# A Transaction is a monetary thing between a sender and a receiver.
# Both sender and receiver are identified using a class Identity.
#
# No part of this module should be used for cryptography in production.
# This module is strictly for education purposes.
#
from cryptocourse import basic_ec
from cryptocourse import basic_merkle_tree
import datetime
import json
import hashlib

BeginningOfAllTime = datetime.datetime(2000, 1, 1, 0, 0)

class MyIdentity:
    def __init__(self, name, randomized = 0):
        ec = basic_ec.StandardECS["secp256k1"]
        g = basic_ec.StandardBasePoints["secp256k1"]
        self.DSA_object = basic_ec.DSA(ec,g, randomized)
        self.name = name
        self.public_key = self.DSA_object.gen_public_key()

    def sign(self, data):
        signature = self.DSA_object.sign(data)
        return signature
        
    def get_public_key(self):
        return self.public_key
        
    def serialize(self):
        d = self.__dict__
        del d['DSA_object']
        return json.dumps(d)

class YourIdentity:
    def __init__(self, public_key):
        # the name is not required, just the public key
        ec = basic_ec.StandardECS["secp256k1"]
        g = basic_ec.StandardBasePoints["secp256k1"]
        self.DSA_object = basic_ec.DSA(ec,g)
        self.public_key = public_key
        
    def validateSignature (self, hashval, signature):
        return self.DSA_object.validate(hashval, signature, self.public_key)
    
    def serialize(self):
        d = self.__dict__
        d.pop('DSA_object', None)
        return json.dumps(d)
        
    def deserialize(self, d):
        d = json.loads(d)
        self.public_key = d['public_key']

class MyTransaction:
    def __init__(self, senderIdentity, recipientIdentity, amount, hash_function='sha256', signature_function = 'ecdsa', timestamp = 0):
        """
        Creates a new transaction

        :param sender: <str> sender account
        :param recipient: <str> recipient account
        :param amount: <float> amount to be transferred
        """
        self.senderId = senderIdentity.public_key
        self.senderName = senderIdentity.name
        self.recipientId = recipientIdentity.public_key
        self.recipientName = recipientIdentity.name
        if timestamp == 0:
            self.timestamp = (datetime.datetime.now() - BeginningOfAllTime).total_seconds()
        else:
            self.timestamp = timestamp
        self.timestamp = timestamp
        assert hash_function in basic_merkle_tree.SECURE_HASH_FUNCTIONS, ("{} is not a valid hash function".format(hash_function))
        self._hash_function = hash_function
        self.senderIdentity = senderIdentity
        self.amount = amount
        self.signature = 0
        self.signature_function = signature_function
    
    def dataToBeHashed(self):
        return str(self.senderId[0]) + "$" + str(self.senderId[1]) + "$" + str(self.recipientId[0]) + "$" + str(self.recipientId[1]) + "$" + str(self.timestamp) + "$" + str(self.amount) + "$" + self._hash_function

    def dataHashed(self):
        return basic_merkle_tree.hash_data(self.dataToBeHashed(), True, self._hash_function)

    def sign(self):
        self.signature = self.senderIdentity.sign(self.dataHashed())
        
    def validateSignature(self, signature=0, sender_public_key=0):
        hashval = self.dataHashed()
        
        if signature == 0:
            signature = self.signature
        if sender_public_key == 0:
            sender_public_key = self.senderId
        party = YourIdentity (sender_public_key)
        return party.validateSignature (hashval, signature)

    def serialize(self):
        d = {}
        d['senderId'] = self.senderId
        d['recipientId'] = self.recipientId
        d['amount'] = self.amount
        d['timestamp'] = self.timestamp
        d['_hash_function'] = self._hash_function
        d['signature_function'] = self.signature_function
        d['signature'] = self.signature
        return json.dumps(d)

class YourTransaction:
    def __init__(self, senderId=0, recipientId=0, amount=0, timestamp=0, hash_function='sha256', signature_function = 'ecdsa'):
        """
        Creates a new transaction

        :param sender: <str> sender account
        :param recipient: <str> recipient account
        :param amount: <float> amount to be transferred
        """
        self.senderId = senderId
        self.recipientId = recipientId
        self.amount = amount
        self.timestamp = timestamp
        self._hash_function = hash_function
        self.signature = 0
        self.signature_function = signature_function
    
    def dataToBeHashed(self):
        return str(self.senderId[0]) + "$" + str(self.senderId[1]) + "$" + str(self.recipientId[0]) + "$" + str(self.recipientId[1]) + "$" + str(self.timestamp) + "$" + str(self.amount) + "$" + self._hash_function

    def dataHashed(self):
        return basic_merkle_tree.hash_data(self.dataToBeHashed(), True, self._hash_function)
        
    def validateSignature(self, signature=0):
        hashval = self.dataHashed()
        party = YourIdentity (self.senderId)
        if signature == 0:
            signature = self.signature
        return party.validateSignature (hashval, signature)

    def serialize(self):
        d = {}
        d['senderId'] = self.senderId
        d['recipientId'] = self.recipientId
        d['amount'] = self.amount
        d['timestamp'] = self.timestamp
        d['_hash_function'] = self._hash_function
        d['signature_function'] = self.signature_function
        d['signature'] = self.signature
        return json.dumps(d)

    def deserialize(self, d):
        d = json.loads(d)
        self.senderId = basic_ec.Coord(d['senderId'][0],d['senderId'][1])
        self.recipientId = basic_ec.Coord(d['recipientId'][0],d['recipientId'][1])
        self.amount = d['amount']
        self.timestamp = d['timestamp']
        self._hash_function = d['_hash_function']
        self.signature_function = d['signature_function']
        self.signature = d['signature']
        
class Block:
    def __init__(self, index=0, transactions=[0], previous_hash='0', miner='0', hash_function='sha256', nonce = 0, timestamp = 0):
        """
        Constructs a new block

        :param index:
        :param transactions:
        :param previous_hash:
        """
        self.index = index
        if timestamp == 0:
            self.timestamp = (datetime.datetime.now() - BeginningOfAllTime).total_seconds()
        else:
            self.timestamp = timestamp
        self.timestamp = timestamp
        self.transactions = basic_merkle_tree.MerkleTree(transactions, hash_function)
        self.nonce = nonce
        self.previous_hash = previous_hash
        self.miner = miner
        self._hash_function = hash_function
        self.hash = self.dataHashed()

    def addTransactions (self, transactions):
        self.transactions.add_tx(transactions)
        self.hash = self.dataHashed()
        
    def dataToBeHashed(self):
        return str(self.index) + "$" + str(self.timestamp) + "$" + str(self.nonce) + "$" + self.previous_hash + "$" + self.miner + "$" + self.transactions.block_header + "$" + self._hash_function

    def dataHashed(self,string_digest = True):
        return basic_merkle_tree.hash_data(self.dataToBeHashed(), string_digest, self._hash_function)

    def serialize(self):
        d = {}
        d['index'] = self.index
        d['timestamp'] = self.timestamp
        d['nonce'] = self.nonce
        d['previous_hash'] = self.previous_hash
        d['miner'] = self.miner
        d['_hash_function'] = self._hash_function
        d['transactions'] = self.transactions.serialize()
        d['hash'] = self.hash
        return json.dumps(d)

    def deserialize(self, d):
        d = json.loads(d)
        self.index = d['index']
        self.timestamp = d['timestamp']
        self.nonce = d['nonce']
        self.previous_hash = d['previous_hash']
        self.miner = d['miner']
        self._hash_function = d['_hash_function']
        self.transactions = basic_merkle_tree.MerkleTree()
        self.transactions.deserialize(d['transactions'])
        self.hash = self.dataHashed()
        if self.hash != d['hash']:
            raise ValueError
        
    def validate(self):
        merkle_tree = self.transactions
        transaction_list = []
        for t in merkle_tree._leaves:
            if t.validateSignature():
                transaction_list.append(t)
            else:
                print ("invalid transaction ignored")
        merkle_tree._leaves = transaction_list
        merkle_tree._reevaluate()
        
    def mine(self, difficulty = 5):
        # difficulty is the number of hexadecimal digits the hash value should start with
        # difficulty level corresponds with 5 hex digits = 20 binary digits
        # so, typically, a brute force requires 2^20 / 2 = 2^19 = 500 000 trials
        # This brute force number is only determined by the difficulty level and not by the length of the hash
        self.validate()
        hash_length = len(self.dataHashed())*4
        maximum_hash_value_length = hash_length - difficulty * 4
        maximum_hash_value = pow(2,maximum_hash_value_length)
        hash_value = self.dataHashed(False)
        while hash_value > maximum_hash_value:
            self.nonce += 1
            hash_value = self.dataHashed(False)
        self.hash = self.dataHashed()

    @property
    def numberOfElements(self):
        return self.transactions.numberOfElements

if __name__ == '__main__':
    # IDENTITIES
    i = MyIdentity("me",1)
    ipub = i.get_public_key()
    j = MyIdentity("you",2)
    jpub = j.get_public_key()
    k = MyIdentity("him/her",3)
    kpub = j.get_public_key()
    
    # timestamp = 0
    timestamp = 1
    
    #TRANSACTIONS AND THEIR SIGNATURES
    t1 = MyTransaction(i,j,100, timestamp = timestamp)
    t1.sign()
    s = t1.signature # this is the transaction signed by me
    res = t1.validateSignature(s,ipub)
    assert res == True
    t2 = YourTransaction(ipub, jpub, t1.amount, t1.timestamp,t1._hash_function)
    res = t2.validateSignature (s)
    assert res == True
    t2.amount += 1
    res = t2.validateSignature (s)
    assert res == False
    t2.amount -= 1
    res = t2.validateSignature (s)
    assert res == True
    t2.timestamp += 1
    res = t2.validateSignature (s)
    assert res == False
    t2.timestamp -= 1
    res = t2.validateSignature (s)
    assert res == True
    t2.recipientId = i.DSA_object.ec.mul(jpub,2)
    res = t2.validateSignature (s)
    assert res == False
    t2.recipientId = jpub
    t2.senderId = i.DSA_object.ec.mul(ipub,2)
    res = t2.validateSignature (s)
    assert res == False
    t2.senderId = ipub
    res = t2.validateSignature (s)
    assert res == True
    
    #SERIALIZE TRANSACTIONS TO COPY FROM ONE TO THE OTHER
    d = t1.serialize()
    t3 = YourTransaction()
    t3.deserialize (d)
    res = t3.validateSignature ()
    assert res == True
    res = t3.validateSignature (s)
    assert res == True
    res = t3.validateSignature (t3.signature)
    assert res == True
    t3.signature = 1
    res = t3.validateSignature (s)
    assert res == True

    t4 = MyTransaction(j,i,15,timestamp = timestamp)
    t4.sign()
    assert t4.validateSignature()
    t5 = MyTransaction(j,k,25,timestamp = timestamp)
    t5.sign()
    assert t5.validateSignature()
    
    t6 = MyTransaction(k,i,9,timestamp = timestamp)
    t6.sign()
    assert t6.validateSignature()
    
    t7 = MyTransaction(k,j,1,timestamp = timestamp)
    t7.sign()
    assert t7.validateSignature()
    
    t8 = MyTransaction(k,j,1, timestamp = timestamp)
    t8.sign()
    assert t8.validateSignature()
    t8.amount = t8.amount + 1
    assert not t8.validateSignature()
    
    #BLOCKS OF TRANSACTIONS
    sumOfNonces = 0
    m = basic_merkle_tree.MerkleTree([t1,t4,t5])
    assert m.height == 2
    hashes = []
    b0 = Block(0,[t1,t4,t5], '0'*40,"genesis", "sha1",0,timestamp)
    h = b0.hash
    hashes.append(h)
    assert b0.transactions.height == 2
    b0.addTransactions([t6,t7])
    h = b0.hash
    assert b0.transactions.height == 3
    assert b0.nonce == 0
    assert h not in hashes
    hashes.append(h)
    b0.mine()
    assert b0.transactions.height == 3
    assert b0.nonce > 0
    h = b0.hash
    assert h not in hashes
    hashes.append(h)
    sumOfNonces += b0.nonce
    # print ("nonce = ", b0.nonce, " hash = ", b0.hash)
    b1 = Block(1,[t1,t4,t5], b0.hash,"participant/miner 1", "sha256",0,timestamp)
    assert b1.transactions.height == 2
    h = b1.hash
    assert h not in hashes
    hashes.append(h)
    b1.addTransactions([t6,t7])
    h = b1.hash
    assert h not in hashes
    hashes.append(h)
    assert b1.transactions.height == 3
    assert b1.nonce == 0
    b1.mine()
    assert b1.transactions.height == 3
    assert b1.nonce > 0
    h = b1.hash
    assert h not in hashes
    hashes.append(h)
    sumOfNonces += b1.nonce
    # print ("nonce = ", b1.nonce, " hash = ", b1.hash)
    b2 = Block(2,[t1,t4,t5], b1.hash,"participant/miner 2", "sha384",0,timestamp)
    assert b2.transactions.height == 2
    h = b2.hash
    assert h not in hashes
    hashes.append(h)
    b2.addTransactions([t6,t7])
    h = b2.hash
    assert h not in hashes
    hashes.append(h)
    assert b2.transactions.height == 3
    assert b2.nonce == 0
    b2.mine()
    assert b2.transactions.height == 3
    assert b2.nonce > 0
    h = b2.hash
    assert h not in hashes
    hashes.append(h)
    sumOfNonces += b2.nonce
    # print ("nonce = ", b2.nonce, " hash = ", b2.hash)
    b3 = Block(3,[t1,t4,t5], b2.hash,"participant/miner 3", "sha512",0,timestamp)
    assert b3.transactions.height == 2
    h = b3.hash
    assert h not in hashes
    hashes.append(h)
    b3.addTransactions([t6,t7, t8])
    h = b3.hash
    assert h not in hashes
    hashes.append(h)
    assert b3.transactions.height == 3
    assert b3.numberOfElements == 6
    assert b3.nonce == 0
    print ("t8 is an invalid transactions and this info should be printed during mining")
    print ("start of mining")
    b3.mine()
    print ("end of mining")
    assert b3.transactions.height == 3
    assert b3.numberOfElements == 5
    assert b3.nonce > 0
    h = b3.hash
    assert h not in hashes
    hashes.append(h)
    sumOfNonces += b3.nonce
    # print ("nonce = ", b3.nonce, " hash = ", b3.hash)
    # print ("average nonce = ", sumOfNonces // 4)
    c = Block(0,[t1,t2, t3,t4,t5], '0'*40,"genesis")
    s = c.serialize()
    d = Block()
    d.deserialize(s)
    assert c.hash == d.hash
    assert c.transactions.block_header == d.transactions.block_header
    assert c.transactions.numberOfElements == d.transactions.numberOfElements
