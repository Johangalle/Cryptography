#!/usr/bin/python3
#
# Basics of Elliptic Curve Cryptography implementation on Python
# Largely based on https://gist.github.com/bellbind/1414867, https://asecuritysite.com/encryption/ecc_points2 and https://safecurves.cr.yp.to/base.html
#
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/
#
# This module supports most functions required for elliptical curve (EC) cryptography:
# - calculations (addition of EC points and multiplication of a scalar and an EC point)
# - a number of standard elliptical curves and base points
# - ElGamal encryption/decryption based on elliptical curve cryptography
# - Diffie-Hellman based on elliptical curve cryptography
# - ECDSA (Elliptical Curve Digital Signature Algorithm)
#
# No part of this module should be used for cryptography in production.
# This module is strictly for education purposes.
#

import collections
from cryptocourse import euclidean
import math
import sys
import os
import binascii
import time
import secrets
import sys

def inv(n, q):
    """div on PN modulo a/b mod q as a * inv(b, q) mod q
    >>> assert n * inv(n, q) % q == 1
    """
    return euclidean.mulinv(n, q)

def sqrt(n, q):
    """sqrt on PN modulo: returns two numbers or exception if not exist
    >>> assert (sqrt(n, q)[0] ** 2) % q == n
    >>> assert (sqrt(n, q)[1] ** 2) % q == n
    """
    n = n%q
    i = modular_sqrt(n,q)
    if i*i%q != n:
        raise Exception("not found")
    else:
        return (i, (q - i)%q)
    """
    if n == 0:
        return 0,0
    assert n < q
    for i in range(1, q):
        if i * i % q == n:
            return (i, q - i)
        pass
    raise Exception("not found")
    """

def modular_sqrt(a, p):
    """ Find a quadratic residue (mod p) of 'a'. p
        must be an odd prime.

        Solve the congruence of the form:
            x^2 = a (mod p)
        And returns x. Note that p - x is also a root.

        0 is returned is no square root exists for
        these a and p.

        The Tonelli-Shanks algorithm is used (except
        for some simple cases in which the solution
        is known from an identity). This algorithm
        runs in polynomial time (unless the
        generalized Riemann hypothesis is false).
    """
    # Simple cases
    #
    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return p
    elif p % 4 == 3:
        return pow(int(a), int((p + 1) // 4), int(p))

    # Partition p-1 to s * 2^e for an odd s (i.e.
    # reduce all the powers of 2 from p-1)
    #
    s = p - 1
    e = 0
    while s % 2 == 0:
        s /= 2
        e += 1

    # Find some 'n' with a legendre symbol n|p = -1.
    # Shouldn't take long.
    #
    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1

    # Here be dragons!
    # Read the paper "Square roots from 1; 24, 51,
    # 10 to Dan Shanks" by Ezra Brown for more
    # information
    #

    # x is a guess of the square root that gets better
    # with each iteration.
    # b is the "fudge factor" - by how much we're off
    # with the guess. The invariant x^2 = ab (mod p)
    # is maintained throughout the loop.
    # g is used for successive powers of n to update
    # both a and b
    # r is the exponent - decreases with each update
    #
    x = pow(a, (s + 1) / 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e

    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, p)

        if m == 0:
            return x

        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m


def legendre_symbol(a, p):
    """ Compute the Legendre symbol a|p using
        Euler's criterion. p is a prime, a is
        relatively prime to p (if p divides
        a, then a|p = 0)

        Returns 1 if a has a square root modulo
        p, -1 otherwise.
    """
    ls = pow(int(a), int((p - 1) // 2), int(p))
    return -1 if ls == p - 1 else ls

Coord = collections.namedtuple("Coord", ["x", "y"])

class EC(object):
    """System of Elliptic Curve"""
    def __init__(self, a, b, q, order=0):
        """elliptic curve as: (y**2 = x**3 + a * x + b) mod q
        - a, b: params of curve formula
        - q: prime number
        """
        a = a%q
        b = b%q
        assert 0 <= a and a < q and 0 <= b and b < q and q > 2
        assert (4 * (a ** 3) + 27 * (b ** 2))  % q != 0
        self.a = a
        self.b = b
        self.q = q
        self._order = order
        # just as unique ZERO value representation for "add": (not on curve)
        self.zero = Coord(0, 0)
        pass

    def is_valid(self, p):
        if p == self.zero: return True
        l = (p.y ** 2) % self.q
        r = ((p.x ** 3) + self.a * p.x + self.b) % self.q
        return l == r

    def at(self, x):
        """find points on curve at x
        - x: int < q
        - returns: ((x, y), (x,-y)) or not found exception
        >>> a, ma = ec.at(x)
        >>> assert a.x == ma.x and a.x == x
        >>> assert a.x == ma.x and a.x == x
        >>> assert ec.neg(a) == ma
        >>> assert ec.is_valid(a) and ec.is_valid(ma)
        """
        assert x < self.q
        ysq = (x ** 3 + self.a * x + self.b) % self.q
        y, my = sqrt(ysq, self.q)
        return Coord(x, y), Coord(x, my)

    def elements (self,max=100):
        result = set()
        count = 0
        for i in range (0,self.q):
            try:
                g, h = self.at(i)
                result.add(g)
                result.add(h)
                count += 2
                if count > max:
                    break
            except:
                pass
        return sorted(result)

    def mul_elements (self, g, max=100):
        result = set()
        count = 0
        for i in range (0, self.q):
            result.add(self.mul(g,i))
            count += 1
            if count > max:
                break
        return sorted(result)

    def neg(self, p):
        """negate p
        >>> assert ec.is_valid(ec.neg(p))
        """
        return Coord(p.x, -p.y % self.q)

    def add(self, p1, p2):
        """<add> of elliptic curve: negate of 3rd cross point of (p1,p2) line
        >>> d = ec.add(a, b)
        >>> assert ec.is_valid(d)
        >>> assert ec.add(d, ec.neg(b)) == a
        >>> assert ec.add(a, ec.neg(a)) == ec.zero
        >>> assert ec.add(a, b) == ec.add(b, a)
        >>> assert ec.add(a, ec.add(b, c)) == ec.add(ec.add(a, b), c)
        """
        if p1 == self.zero: return p2
        if p2 == self.zero: return p1
        if p1.x == p2.x and (p1.y != p2.y or p1.y == 0):
            # p1 + -p1 == 0
            return self.zero
        if p1.x == p2.x:
            # p1 + p1: use tangent line of p1 as (p1,p1) line
            l = (3 * p1.x * p1.x + self.a) * inv(2 * p1.y, self.q) % self.q
            pass
        else:
            l = (p2.y - p1.y) * inv(p2.x - p1.x, self.q) % self.q
            pass
        x = (l * l - p1.x - p2.x) % self.q
        y = (l * (p1.x - x) - p1.y) % self.q
        return Coord(x, y)

    def mul(self, p, n):
        """n times <mul> of elliptic curve
        >>> m = ec.mul(p, n)
        >>> assert ec.is_valid(m)
        >>> assert ec.mul(p, 0) == ec.zero
        """
        r = self.zero
        m2 = p
        # O(log2(n)) add
        while 0 < n:
            if n & 1 == 1:
                r = self.add(r, m2)
                pass
            n, m2 = n >> 1, self.add(m2, m2)
            pass
        # [ref] O(n) add
        #for i in range(n):
        #    r = self.add(r, p)
        #    pass
        return r

    def order(self, g, max = 100):
        """order of point g
        >>> o = ec.order(g)
        >>> assert ec.is_valid(a) and ec.mul(a, o) == ec.zero
        >>> assert o <= ec.q
        """
        assert self.is_valid(g) and g != self.zero
        if self._order == 0:
            for i in range(1, 2*self.q + 1):
                if self.mul(g, i) == self.zero:
                    return i
                pass
            raise Exception("Invalid order")
        else:
            return self._order
    pass

StandardECS = {
    "Anomalous": EC(15347898055371580590890576721314318823207531963035637503096292, 7444386449934505970367865204569124728350661870959593404279615, 0xb0000000000000000000000953000000000000000000001f9d7, 0xb0000000000000000000000953000000000000000000001f9d7),
    "P-192": EC(-3,2455155546008943817740293915197451784769108058161191238065, 2**192-2**64-1,  6277101735386680763835789423176059013767194773182842284081),
    "P-224": EC(-3,18958286285566608000408668544493926415504680968679321075787234672564, 2**224 - 2**96 + 1, 0xffffffffffffffffffffffffffff16a2e0b8f03e13dd29455c5c2a3d),
    "P-256": EC(-3,41058363725152142129326129780047268409114441015993725554835256314039467401291, 2**256 - 2**224 + 2**192 + 2**96 - 1, 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551),
    "P-384": EC(-3, 27580193559959705877849011840389048093056905856361568521428707301988689241309860865136260764883745107765439761230575, 2**384 - 2**128 - 2**96 + 2**32 - 1, 0xffffffffffffffffffffffffffffffffffffffffffffffffc7634d81f4372ddf581a0db248b0a77aecec196accc52973),
    "secp256k1": EC(0, 7,2**256 - 2**32 - 977, 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141),
    "BN(2,254)": EC(0, 2, 16798108731015832284940804142231733909889187121439069848933715426072753864723, 0x2523648240000001ba344d8000000007ff9f800000000010a10000000000000d),
    "brainpoolP256t1": EC(-3, 46214326585032579593829631435610129746736367449296220983687490401182983727876, 0xa9fb57dba1eea9bc3e660a909d838d726e3bf623d52620282013481d1f6e5377, 0xa9fb57dba1eea9bc3e660a909d838d718c397aa3b561a6f7901e0e82974856a7),
    "FRP256v1": EC(-3, 107744541122042688792155207242782455150382764043089114141096634497567301547839, 0xf1fd178c0b3ad58f10126de8ce42435b3961adbcabc8ca6de8fcf353d86e9c03, 0xf1fd178c0b3ad58f10126de8ce42435b53dc67e140d2bf941ffdd459c6d655e1),
    "brainpoolP384t1": EC(-3, 19596161053329239268181228455226581162286252326261019516900162717091837027531392576647644262320816848087868142547438, 0x8cb91e82a3386d280f5d6f7e50e641df152f7109ed5456b412b1da197fb71123acd3a729901d1a71874700133107ec53, 0x8cb91e82a3386d280f5d6f7e50e641df152f7109ed5456b31f166e6cac0425a7cf3ab6af6b7fc3103b883202e9046565),
    }
StandardBasePoints = {
    "Anomalous": Coord(0x101efb35fd1963c4871a2d17edaafa7e249807f58f8705126c6, 0x22389a3954375834304ba1d509a97de6c07148ea7f5951b20e7),
    "P-192": Coord(0x188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012, 0x07192b95ffc8da78631011ed6b24cdd573f977a11e794811),
    "P-224": Coord(0xb70e0cbd6bb4bf7f321390b94a03c1d356c21122343280d6115c1d21, 0xbd376388b5f723fb4c22dfe6cd4375a05a07476444d5819985007e34),
    "P-256": Coord(0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296, 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5),
    "P-384": Coord(0xaa87ca22be8b05378eb1c71ef320ad746e1d3b628ba79b9859f741e082542a385502f25dbf55296c3a545e3872760ab7, 0x3617de4a96262c6f5d9e98bf9292dc29f8f41dbd289a147ce9da3113b5f0b8c00a60b1ce1d7e819d7a431d7c90ea0e5f),
    "secp256k1": Coord(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8),
    "BN(2,254)": Coord(-1,1),
    "brainpoolP256t1": Coord(0xa3e8eb3cc1cfe7b7732213b23a656149afa142c47aafbc2b79a191562e1305f4, 0x2d996c823439c56d7f7b22e14644417e69bcb6de39d027001dabe8f35b25c9be),
    "FRP256v1": Coord(0xb6b3d4c356c139eb31183d4749d423958c27d2dcaf98b70164c97a2dd98f5cff, 0x6142e0f7c8b204911f9271f0f3ecef8c2701c307e8e4c9e183115a1554062cfb),
    "brainpoolP384t1": Coord(0x18de98b02db9a306f2afcd7235f72a819b80ab12ebd653172476fecd462aabffc4ff191b946a5f54d8d0aa2f418808cc, 0x25ab056962d30651a114afd2755ad336747f93475b7a1fca3b88f2b6a208ccfe469408584dc2b2912675bf5b9e582928),
    }
class ElGamal(object):
    """ElGamal Encryption
    pub key encryption as replacing (mulmod, powmod) to (ec.add, ec.mul)
    - ec: elliptic curve
    - g: (random) a point on ec
    """
    def __init__(self, ec, g):
        assert ec.is_valid(g)
        self.ec = ec
        self.g = g
        # self.n = ec.order(g)
        pass

    def gen_private_key(self):
        self.priv = int.from_bytes(secrets.token_bytes(math.ceil(self.ec.q.bit_length() / 8)),sys.byteorder)%(self.ec.q)
        # self.priv = int(binascii.hexlify(os.urandom(100)), base=16)%(self.ec.q)

    def set_private_key(self, priv):
        self.priv = priv

    def gen_public_key(self):
        """generate pub key
        - priv: priv key as (random) int < ec.q
        - returns: pub key as points on ec
        """
        return self.ec.mul(self.g, self.priv)

    def enc(self, plain, pub, r=0):
        """encrypt
        - plain: data as a point on ec
        - pub: pub key as points on ec
        - r: randam int < ec.q
        - returns: (cipher1, ciper2) as points on ec
        """
        if r == 0:
            r = int.from_bytes(secrets.token_bytes(math.ceil(self.ec.q.bit_length() / 8)),sys.byteorder)%(self.ec.q)
            # r = int(binascii.hexlify(os.urandom(100)), base=16)%(self.ec.q)
        assert self.ec.is_valid(plain)
        assert self.ec.is_valid(pub)
        return (self.ec.mul(self.g, r), self.ec.add(plain, self.ec.mul(pub, r)))

    def dec(self, cipher):
        """decrypt
        - chiper: (chiper1, chiper2) as points on ec
        - priv: private key as int < ec.q
        - returns: plain as a point on ec
        """
        c1, c2 = cipher
        assert self.ec.is_valid(c1) and self.ec.is_valid(c2)
        return self.ec.add(c2, self.ec.neg(self.ec.mul(c1, self.priv)))
    pass
    

class DiffieHellman(object):
    """Elliptic Curve Diffie Hellman (Key Agreement)
    - ec: elliptic curve
    - g: a point on ec
    """
    def __init__(self, ec, g):
        self.ec = ec
        self.g = g
        # self.n = ec.order(g)
        self.priv = int.from_bytes(secrets.token_bytes(math.ceil(self.ec.q.bit_length() / 8)),sys.byteorder)%(self.ec.q)
        # self.priv = int(binascii.hexlify(os.urandom(100)), base=16)%(ec.q)
        pass
        
    def get_private_key(self):
        """ Return the private key (a) """
        return self.priv

    def set_private_key(self,a):
        """ Sets the private key (a) """
        self.priv = a

    def gen_public_key(self):
        """generate pub key"""
        return self.ec.mul(self.g, self.priv)

    def gen_shared_key(self, other_contribution):
        """calc shared secret key for the pair
        - priv: my private key
        - other contribution: partner pub key as a point on ec
        - returns: shared secret as a point on ec
        """
        assert self.ec.is_valid(other_contribution)
        return self.ec.mul(other_contribution, self.priv)
    pass


class DSA(object):
    """ECDSA
    - ec: elliptic curve
    - g: a point on ec
    """
    def __init__(self, ec, g, randomized=0):
        self.ec = ec
        self.g = g
        self.n = ec.order(g)
        if randomized == 0:
            self.priv = int.from_bytes(secrets.token_bytes(math.ceil(self.ec.q.bit_length() / 8)),sys.byteorder)%(self.ec.q)
        else:
            self.priv = randomized
        # self.priv = int(binascii.hexlify(os.urandom(100)), base=16)%(ec.q)
        pass
        
    def get_private_key(self):
        """ Return the private key (a) """
        return self.priv

    def set_private_key(self,a):
        """ Sets the private key (a) """
        self.priv = a

    def gen_public_key(self):
        """generate pub key"""
        return self.ec.mul(self.g, self.priv)

    def sign(self, hashval, r = 0):
        """generate signature
        - hashval: hash value of message as int
        - priv: priv key as int
        - r: random int
        - returns: signature as (int, int)
        """
        if isinstance(hashval,str):
            hashval = int(hashval,16)
        hashval = int(hashval)
        if r == 0:
            inverse = 0
        else:
            inverse = 0
            try:
                inverse = inv(r, self.n)
                sig1 = inverse * (hashval + m.x * self.priv) % self.n
                inverse = inv(sig1, self.n)
            except:
                r = 0
        while r == 0:
            r = int.from_bytes(secrets.token_bytes(math.ceil(self.ec.q.bit_length() / 8)),sys.byteorder)%(self.ec.q)
            # r = int(binascii.hexlify(os.urandom(100)), base=16)%(self.ec.q)
            try:
                inverse = inv(r, self.n)
            except:
                r = 0
            if r != 0:
                m = self.ec.mul(self.g, r)
                sig0 = m.x
                sig1 = inv(r, self.n) * (hashval + m.x * self.priv) % self.n
                try:
                    inverse = inv(sig1, self.n)
                except:
                    r = 0
        m = self.ec.mul(self.g, r)
        return (m.x, inv(r, self.n) * (hashval + m.x * self.priv) % self.n)

    def validate(self, hashval, sig, pub):
        """validate signature
        - hashval: hash value of message as int
        - sig: signature as (int, int)
        - pub: pub key as a point on ec
        """
        if isinstance(hashval,str):
            hashval = int(hashval,16)
        assert self.ec.is_valid(pub)
        assert self.ec.mul(pub, self.n) == self.ec.zero
        w = inv(sig[1], self.n)
        u1, u2 = hashval * w % self.n, sig[0] * w % self.n
        p = self.ec.add(self.ec.mul(self.g, u1), self.ec.mul(pub, u2))
        return p.x % self.n == sig[0]
    pass


if __name__ == "__main__":
    # shared elliptic curve system of examples
    ec = EC(1, 18, 19)
    g, _ = ec.at(7)
    
    # ElGamal enc/dec usage
    eg_receiver = ElGamal(ec, g)
    # mapping value to ec point
    # "masking": value k to point ec.mul(g, k)
    # ("imbedding" on proper n:use a point of x as 0 <= n*v <= x < n*(v+1) < q)
    mapping = ec.elements()
    plain = mapping[7]
    
    eg_receiver.gen_private_key()
    pub = eg_receiver.gen_public_key()
    
    eg_sender = ElGamal(ec, g)
    cipher = eg_sender.enc(plain, pub, 15)
    decoded = eg_receiver.dec(cipher)
    assert decoded == plain
    assert cipher != pub
    
    # ECDH usage
    adh = DiffieHellman(ec, g)
    apub = adh.gen_public_key()
    time.sleep(0.5)
    
    bdh = DiffieHellman(ec, g)
    bpub = bdh.gen_public_key()
    time.sleep(0.5)

    cdh = DiffieHellman(ec, g)
    cpub = cdh.gen_public_key()
    
    # same secret on each pair
    assert adh.gen_shared_key (bpub) == bdh.gen_shared_key(apub)
    assert adh.gen_shared_key (cpub) == cdh.gen_shared_key(apub)
    assert bdh.gen_shared_key (cpub) == cdh.gen_shared_key(bpub)
        
    # not same secret on other pair, but due to the small values in this example, these assertions sometyimes fail
    # assert adh.gen_shared_key (bpub) != bdh.gen_shared_key(cpub)
    # assert adh.gen_shared_key (cpub) != bdh.gen_shared_key(apub)
    # assert bdh.gen_shared_key (cpub) != adh.gen_shared_key(bpub)

    
    # ECDSA usage
    dsa = DSA(ec, g)
    
    pub = dsa.gen_public_key()
    hashval = 128
    r = 7
    
    sig = dsa.sign(hashval, r)
    assert dsa.validate(hashval, sig, pub)

    # shared elliptic curve system of examples
    ec = StandardECS["secp256k1"]
    g = StandardBasePoints["secp256k1"]
    
    # ElGamal enc/dec usage
    eg_receiver = ElGamal(ec, g)
    # mapping value to ec point
    # "masking": value k to point ec.mul(g, k)
    # ("imbedding" on proper n:use a point of x as 0 <= n*v <= x < n*(v+1) < q)
    
    eg_receiver.gen_private_key()
    pub = eg_receiver.gen_public_key()
    
    eg_sender = ElGamal(ec, g)
    plain,_ = ec.at(123) # I know that 123 is a correct x value for this elliptical curve
    cipher = eg_sender.enc(plain, pub, 15)
    decoded = eg_receiver.dec(cipher)
    assert decoded == plain
    assert cipher != pub
    
    # ECDH usage
    adh = DiffieHellman(ec, g)
    apub = adh.gen_public_key()
    
    bdh = DiffieHellman(ec, g)
    bpub = bdh.gen_public_key()

    cdh = DiffieHellman(ec, g)
    cpub = cdh.gen_public_key()
    
    # same secret on each pair
    assert adh.gen_shared_key (bpub) == bdh.gen_shared_key(apub)
    assert adh.gen_shared_key (cpub) == cdh.gen_shared_key(apub)
    assert bdh.gen_shared_key (cpub) == cdh.gen_shared_key(bpub)
        
    # not same secret on other pair
    assert adh.gen_shared_key (bpub) != bdh.gen_shared_key(cpub)
    assert adh.gen_shared_key (cpub) != bdh.gen_shared_key(apub)
    assert bdh.gen_shared_key (cpub) != adh.gen_shared_key(bpub)
    
    # ECDSA usage
    dsa = DSA(ec, g)
    
    pub = dsa.gen_public_key()
    hashval = 128
    r = 7
    
    sig = dsa.sign(hashval, r)
    assert dsa.validate(hashval, sig, pub)

    # Diffie Hellman using a standard EC curve
    ec = StandardECS["secp256k1"]
    g = StandardBasePoints["secp256k1"]
    
    a = DiffieHellman(ec,g)
    b = DiffieHellman(ec,g)
    
    puba = a.gen_public_key()
    pubb = b.gen_public_key()
    
    secretab = a.gen_shared_key(pubb)
    secretba = b.gen_shared_key(puba)
    assert secretab == secretba

    # ECDSA using a standard EC curve
    ec = StandardECS["secp256k1"]
    g = StandardBasePoints["secp256k1"]

    d_sender = DSA(ec, g)
    public = d_sender.gen_public_key()
    signature = d_sender.sign(127,7)
    
    d_receiver = DSA(ec,g)
    assert d_receiver.validate(127,signature,public)
    assert d_receiver.validate(128,signature,public) == False
