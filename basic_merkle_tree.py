#!/usr/bin/python3
#
# Largely based on merkle_tree implementation from Blockchain-for-Developers.
# See https://github.com/Blockchain-for-Developers/merkle-tree
#
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/
#
# This module supports the functions required to construct and check a merkle tree.
#
# No part of this module should be used for cryptography in production.
# This module is strictly for education purposes.
#
import hashlib
import sys
import json
import basic_bc

SECURE_HASH_FUNCTIONS = ['sha1', 'sha224', 'sha256', 'sha384', 'sha512']

def is_power_of_two(n):
    """Check whether `n` is an exponent of two

    >>> is_power_of_two(0)
    False
    >>> is_power_of_two(1)
    True
    >>> is_power_of_two(2)
    True
    >>> is_power_of_two(3)
    False
    >>> if_power_of_two(16)
    True
    """
    return n != 0 and ((n & (n - 1)) == 0)

def hash_data(data, digest = True, hash_function='sha256'):
    """One-way function, takes various standard algorithm names as
    `hash_function` input and uses it to hash string `data`. The default
    algorithm is 'sha256'. Even small changes in `data` input cause
    significant changes to the output

    >>> example = 'hello'
    >>> hash_data(example)
    '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
    >>> hash_data(example, 'sha1')
    'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d'
    >>> example = 'hello!'
    >>> hash_data(example)
    'ce06092fb948d9ffac7d1a376e404b26b7575bcc11ee05a4615fef4fec3a308b'
    """
    hash_function = getattr(hashlib, hash_function)
    data = data.encode('utf-8')
    if digest:
        return hash_function(data).hexdigest()
    else:
        return int.from_bytes(hash_function(data).digest(),'big')

def concat_and_hash_list(lst, hash_function='sha256'):
    """Helper function for quickly concatenate pairs of values and hash them.
    The process is repeated until one value is returned: the final hash.
    Assumes that the length of the `lst` is an exponent of two

    >>> concat_and_hash_list(['a', 'b'])
    'fb8e20fc2e4c3f248c60c39bd652f3c1347298bb977b8b4d5903b85055620603'
    """
    assert len(lst) >= 2, "No transactions to be hashed"
    while len(lst) > 1:
        a = lst.pop(0)
        b = lst.pop(0)
        lst.append(hash_data(a + b, True, hash_function))
    return lst[0]

def convertToStringOrSerialized(s):
    try:
        result = s.serialize()
    except:
        try:
            result = str(s)
        except:
            raise ValueError()
    return result

def convertToStringOrToBeHashed(s):
    try:
        result = s.dataToBeHashed()
    except:
        try:
            result = str(s)
        except:
            raise ValueError()
    return result

class HashLeaf(object):
    """Attach two pieces of string data and store the hash of the concatenated
    strings
    """
    def __init__(self, left=0, right=0, hash_function='sha256'):
        assert isinstance(hash_function, str), (
            "Hash function is not of type `String`")
        self._hash_function = hash_function
        self._left = left
        self._right = right
        self._data = self._evaluate()
        self._height = 1
        
    def _evaluate(self):
        return hash_data(self.dataToBeHashed(), True, self._hash_function)

    def dataToBeHashed(self):
        return convertToStringOrToBeHashed(self._left) + "$" + convertToStringOrToBeHashed(self._right) + "$"  + self._hash_function

    @property
    def data(self):
        """str: Allow the user to query the hashed data stored in the
        HashLeaf
        """
        return self._data

    @property
    def height(self):
        """int: Allow the user to query the height stored in the HashLeaf"""
        return self._height
        
    def serialize(self):
        d = {}
        d['left'] = convertToStringOrSerialized(self._left)
        d['right'] = convertToStringOrSerialized(self._right)
        d['_hash_function'] = self._hash_function
        d['_data'] = self._data
        return json.dumps(d)

    def deserialize(self, d):
        d = json.loads(d)
        self._hash_function = d['_hash_function']
        self._left = d['left']
        self._right = d['right']
        self._height = 1
        self._data = self._evaluate()
        if self._data != d['_data']:
            raise ValueError()

class HashNode(HashLeaf):
    """Attach two HashLeaf structures and store the hash of their concatenated
    data
    """
    def __init__(self, left, right, hash_function):
        super().__init__(left, right, hash_function)
        assert left._hash_function == hash_function, (
            "Hash functions incompatible")
        assert right._hash_function == hash_function, (
            "Hash functions incompatible")
        self._height = self._left.height + 1

    def _evaluate(self):
        """Ensure data is in the form of a HashLeaf data structures and has
        the correct height. Separate method from `HashLeaf` as there are
        different requirements
        """
        assert isinstance(self._left, HashLeaf), (
            "Data is not of type `HashLeaf`")
        assert isinstance(self._right, HashLeaf), (
            "Data is not of type `HashLeaf`")
        assert self._left.height == self._right.height, (
            "Left and right branch not balanced")
        return hash_data(self.dataToBeHashed(), True, self._hash_function)
 
    def dataToBeHashed(self):
        return self._left.data + "$" + self._right.data + "$"  + self._hash_function
 
    def serialize(self):
        d = {}
        d['left'] = self._left.serialize()
        d['right'] = self._right.serialize()
        d['_hash_function'] = self._hash_function
        d['_data'] = self._data
        return json.dumps(d)
        
class MerkleTree(object):
    """Merkle Tree implementation, default hash function is 'sha256'.
    Nodes are reconstructed upon every tx addition but the list of tx
    persistent
    """
    def __init__(self, tx_list = [0], hash_function='sha256'):
        hash_function = hash_function.lower()
        assert tx_list, "No transactions to be hashed"
        assert hash_function in SECURE_HASH_FUNCTIONS, (
            "{} is not a valid hash function".format(hash_function))
        self._hash_function = hash_function
        tx_list = list(tx_list)
        if type(tx_list[0]) == list:
            tx_list = tx_list[0]
        self._leaves = tx_list
        self._nodes = []
        self._root = self._evaluate()
        self._height = self._root.height
        self._block_header = self._root.data

    def add_tx(self, *tx):
        """Add an arbitrary amount of tx's to the tree. It needs to be
        reconstructed every time this happens and the block header
        changes as well
        """
        tx_in = list(tx)
        if type(tx_in[0]) == list:
            tx_in = tx_in[0]
        self._leaves += tx_in
        self._reevaluate()

    def reset_tree(self, hash_function='sha256'):
        """Clear the tree data"""
        self._hash_function = hash_function
        self._nodes = []
        self._height = 0
        self._block_header = None

    def _evaluate(self):
        """Used to construct the tree and arrive at the block header"""
        leaves = list(self._leaves)
        if not is_power_of_two(len(leaves)) or len(leaves) < 2:
            last_tx = leaves[-1]
            while not is_power_of_two(len(leaves)) or len(leaves) < 2:
                leaves.append(last_tx)
        for tx in range(0, len(leaves), 2):
            self._nodes.append(HashLeaf(leaves[tx], leaves[tx+1],
                self._hash_function))
        nodes = list(self._nodes)
        while len(nodes) > 2:
            left = nodes.pop(0)
            right = nodes.pop(0)
            node = HashNode(left, right, self._hash_function)
            nodes.append(node)
        if len(nodes) == 1:
            return nodes[0]
        return HashNode(nodes[0], nodes[1], self._hash_function)

    def _reevaluate(self):
        """Resets the tree and makes a call to `_evaluate(...)` to reconstruct
        the tree given its persistent list of tx's
        """
        self.reset_tree(self._hash_function)
        self._root = self._evaluate()
        self._height = self._root.height
        self._block_header = self._root.data

    def serialize(self):
        # Serializing in merkle_tree is only used for transfering data to another process
        # It is not used for hashing, as the hashing is only done inside the HahNode and HashLeaf objects
        # Therefore, the HashNode / HashLeaf serialize function is called with toHash parameter = False
        d = {}
        d['_root_hashes'] = self._root.serialize()
        leaves_list =[]
        for l in self._leaves:
            leaves_list.append(convertToStringOrSerialized(l))
        d['leaves'] = leaves_list
        d['_hash_function'] = self._hash_function
        d['height'] = self.height
        d['_block_header'] = self._block_header
        return json.dumps(d)
        
    def deserialize(self, d):
        d = json.loads(d)
        self._leaves = []
        for l in d['leaves']:
            t = basic_bc.YourTransaction()
            t.deserialize(l)
            self._leaves.append (t)
        self._hash_function = d['_hash_function']
        self._reevaluate()
        if self.block_header != d['_block_header']:
            raise ValueError
        
    @property
    def hash_function(self):
        """func: Allow the user to query the tree's hash function"""
        return self._hash_function

    # @hash_function.setter
    def hash_function(self, value):
        """Allows the user to change the tree's hash function. Requires that
        the tree be rebuilt to accomodate this change
        """
        value = value.lower()
        assert value in SECURE_HASH_FUNCTIONS, (
            "{} is not a valid hash function".format(value))
        self._hash_function = value

    @property
    def block_header(self):
        """str: Allow the user to query the tree's block header"""
        return self._block_header

    @property
    def height(self):
        """int: Allow the user to query the tree's height"""
        return self._height

    @property
    def leaves(self):
        """list: Allow the user to query the tree's list of tx's"""
        return self._leaves
    
    @property
    def numberOfElements(self):
        return len(self._leaves)

if __name__ == '__main__':
    hashes = []
    txt = 'a'
    m = MerkleTree(txt)
    assert m.height == 1
    m = MerkleTree(['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15'])
    h = m.block_header
    assert h not in hashes
    hashes.append(h)
    assert m.height == 4
    m.add_tx(['16'])
    h = m.block_header
    assert h not in hashes
    hashes.append(h)
    assert m.height == 4
    m.add_tx(['17','18','19'])
    h = m.block_header
    assert h not in hashes
    hashes.append(h)
    assert m.height == 5
    m.add_tx(['20','21','22','23','24','25','26','27','28','29','30','31','32'])
    h = m.block_header
    assert h not in hashes
    hashes.append(h)
    assert m.height == 5
    m.add_tx(['33'])
    h = m.block_header
    assert h not in hashes
    hashes.append(h)
    assert m.height == 6

    from basic_bc import *
    
    i = MyIdentity("me")
    j = MyIdentity("you")
    k = MyIdentity("him/her")
    t1 = MyTransaction(i,j,100)
    t1.sign()
    t2 = MyTransaction(i, k, 15)
    t2.sign()
    t3 = MyTransaction(j,k,20)
    t3.sign()
    t4 = MyTransaction(k,j,2)
    t4.sign()
    t5 = MyTransaction(k,i,3)
    t5.sign()
    m = MerkleTree([t1,t2, t3, t4, t5])
    s = m.serialize()

    n = MerkleTree()
    n.deserialize(s)
    
    assert n.block_header == m.block_header
