#!/usr/bin/python3
#
# aes.py: implements AES - Advanced Encryption Standard
# based on octopius / slowaes: https://github.com/octopius/slowaes/blob/master/python/aes.py
#
# This is in turn based on:
# from the SlowAES project, http://code.google.com/p/slowaes/
#
# Copyright (c) 2008    Josh Davis ( http://www.josh-davis.org ),
#           Alex Martelli ( http://www.aleax.it )
#
# Ported from C code written by Laurent Haan ( http://www.progressive-coding.com )
#
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/
#
# The main addition done by this contribution is to both support byte strings and standard strings,
# as cleartext as well as ciphertext, and also adding CTR as a mode of operation.
# For the key and initialization vectors, both arrays of ints and byte strings are supported.
#
# This module uses the aes encryption algorithm and adds modes of operation.
# The modes of operation OFB, CFB, CBC and CTR are supported.
# No authenticated modes of encryption are supported.
# A pure block cipher suc as AES can only encrypt/decrypt the exact block size input, i.e. 128 bits.
# Modes of operation extend this encrypt/decrypt capability to arbitrary lengths.
# This means we can encrypt/decrypt inputs of less than and more than 128 bits.
#
# No part of this module should be used for cryptography in production.
# This module is strictly for education purposes.
#

import aes
import math

class AESModeOfOperation(object):

    aes = aes.AES()
    bytes_string = False

    # structure of supported modes of operation
    modeOfOperation = dict(OFB=0, CFB=1, CBC=2, CTR=3)

    # converts a 16 character string into a number array
    def convertString(self, string, start, end, mode):
        if end - start > 16: end = start + 16
        if mode == self.modeOfOperation["CBC"]: ar = [0] * 16
        else: ar = []

        i = start
        j = 0
        while len(ar) < end - start:
            ar.append(0)
        while i < end:
            if isinstance(string,bytes):
                ar[j] = string[i]
            else:
                ar[j] = ord(string[i])
            j += 1
            i += 1
        return ar

    def convertToList(self, ctr):
        """
        The ctr value is a (large) number; the return value should be a list of ints (bytes)
        """
        hexstr = hex(ctr)[2:]
        if len(hexstr) % 2 == 1:
            hexstr = '0' + hexstr
        return list(bytes.fromhex(hexstr))

    # Mode of Operation Encryption
    # stringIn - Input String
    # mode - mode of type modeOfOperation
    # hexKey - a hex key of the bit length size
    # size - the bit length of the key
    # hexIV - the 128 bit hex Initilization Vector
    def encrypt(self, stringIn, mode, key, size, IV):
        if isinstance(stringIn, bytes):
            bytes_string = True
        else:
            bytes_string = False
        if isinstance(key,bytes):
            key = list(key)
        if isinstance(IV, bytes):
            IV = list(IV)
        if len(key) % size:
            return None
        if len(IV) % 16:
            return None
        # the AES input/output
        plaintext = []
        iput = [0] * 16
        output = []
        ciphertext = [0] * 16
        # the output cipher string
        if bytes_string:
            cipherOut = b''
        else:
            cipherOut = []
        # char firstRound
        firstRound = True
        if stringIn != None:
            for j in range(int(math.ceil(float(len(stringIn))/16))):
                start = j*16
                end = j*16+16
                if  end > len(stringIn):
                    end = len(stringIn)
                plaintext = self.convertString(stringIn, start, end, mode)
                # print 'PT@%s:%s' % (j, plaintext)
                if mode == self.modeOfOperation["CFB"]:
                    if firstRound:
                        output = self.aes.encrypt(IV, key, size)
                        firstRound = False
                    else:
                        output = self.aes.encrypt(iput, key, size)
                    for i in range(16):
                        if len(plaintext)-1 < i:
                            ciphertext[i] = 0 ^ output[i]
                        elif len(output)-1 < i:
                            ciphertext[i] = plaintext[i] ^ 0
                        elif len(plaintext)-1 < i and len(output) < i:
                            ciphertext[i] = 0 ^ 0
                        else:
                            ciphertext[i] = plaintext[i] ^ output[i]
                    if bytes_string:
                        cipherOut += bytes(ciphertext)[:end-start]
                    else:
                        for k in range(end-start):
                            cipherOut.append(ciphertext[k])
                    iput = ciphertext
                elif mode == self.modeOfOperation["OFB"]:
                    if firstRound:
                        output = self.aes.encrypt(IV, key, size)
                        firstRound = False
                    else:
                        output = self.aes.encrypt(iput, key, size)
                    for i in range(16):
                        if len(plaintext)-1 < i:
                            ciphertext[i] = 0 ^ output[i]
                        elif len(output)-1 < i:
                            ciphertext[i] = plaintext[i] ^ 0
                        elif len(plaintext)-1 < i and len(output) < i:
                            ciphertext[i] = 0 ^ 0
                        else:
                            ciphertext[i] = plaintext[i] ^ output[i]
                    if bytes_string:
                        cipherOut += bytes(ciphertext)[:end-start]
                    else:
                        for k in range(end-start):
                            cipherOut.append(ciphertext[k])
                    iput = output
                elif mode == self.modeOfOperation["CBC"]:
                    for i in range(16):
                        if firstRound:
                            iput[i] =  plaintext[i] ^ IV[i]
                        else:
                            iput[i] =  plaintext[i] ^ ciphertext[i]
                    # print 'IP@%s:%s' % (j, iput)
                    firstRound = False
                    ciphertext = self.aes.encrypt(iput, key, size)
                    # always 16 bytes because of the padding for CBC
                    if bytes_string:
                        cipherOut += ciphertext
                    else:
                        for k in range(16):
                            cipherOut.append(ciphertext[k])
                elif mode == self.modeOfOperation["CTR"]:
                    if firstRound:
                        counter = int.from_bytes(bytes(IV[0:12] + [0,0,0,0]))
                        counterlist = self.convertToList(counter)
                        output = self.aes.encrypt(counterlist, key, size)
                        firstRound = False
                    else:
                        counter = counter + 1
                        counterlist = self.convertToList(counter)
                        output = self.aes.encrypt(counterlist, key, size)
                    for i in range(16):
                        if len(plaintext)-1 < i:
                            ciphertext[i] = 0 ^ output[i]
                        else:
                            ciphertext[i] = plaintext[i] ^ output[i]
                    if bytes_string:
                        cipherOut += bytes(ciphertext)[:end-start]
                    else:
                        for k in range(end-start):
                            cipherOut.append(ciphertext[k])
        return mode, len(stringIn), cipherOut

    # Mode of Operation Decryption
    # cipherIn - Encrypted String
    # originalsize - The unencrypted string length - required for CBC
    # mode - mode of type modeOfOperation
    # key - a number array of the bit length size
    # size - the bit length of the key
    # IV - the 128 bit number array Initilization Vector
    def decrypt(self, cipherIn, originalsize, mode, key, size, IV):
        # cipherIn = unescCtrlChars(cipherIn)
        if isinstance(cipherIn, bytes):
            bytes_string = True
        else:
            bytes_string = False
        if len(key) % size:
            return None
        if isinstance(key,bytes):
            key = list(key)
        if isinstance(IV, bytes):
            IV = list(IV)
        if len(IV) % 16:
            return None
        # the AES input/output
        ciphertext = []
        iput = []
        output = []
        plaintext = [0] * 16
        # the output plain text string
        if bytes_string:
            stringOut = b''
        else:
            stringOut = ''
        # char firstRound
        firstRound = True
        if cipherIn != None:
            for j in range(int(math.ceil(float(len(cipherIn))/16))):
                start = j*16
                end = j*16+16
                if j*16+16 > len(cipherIn):
                    end = len(cipherIn)
                ciphertext = cipherIn[start:end]
                if mode == self.modeOfOperation["CFB"]:
                    if firstRound:
                        output = self.aes.encrypt(IV, key, size)
                        firstRound = False
                    else:
                        output = self.aes.encrypt(iput, key, size)
                    for i in range(16):
                        if len(output)-1 < i:
                            plaintext[i] = 0 ^ ciphertext[i]
                        elif len(ciphertext)-1 < i:
                            plaintext[i] = output[i] ^ 0
                        elif len(output)-1 < i and len(ciphertext) < i:
                            plaintext[i] = 0 ^ 0
                        else:
                            plaintext[i] = output[i] ^ ciphertext[i]
                    if bytes_string:
                        stringOut += bytes(plaintext)[:end-start]
                    else:
                        for k in range(end-start):
                            stringOut += chr(plaintext[k])
                    iput = ciphertext
                elif mode == self.modeOfOperation["OFB"]:
                    if firstRound:
                        output = self.aes.encrypt(IV, key, size)
                        firstRound = False
                    else:
                        output = self.aes.encrypt(iput, key, size)
                    for i in range(16):
                        if len(output)-1 < i:
                            plaintext[i] = 0 ^ ciphertext[i]
                        elif len(ciphertext)-1 < i:
                            plaintext[i] = output[i] ^ 0
                        elif len(output)-1 < i and len(ciphertext) < i:
                            plaintext[i] = 0 ^ 0
                        else:
                            plaintext[i] = output[i] ^ ciphertext[i]
                    if bytes_string:
                        stringOut += bytes(plaintext)[:end-start]
                    else:
                        for k in range(end-start):
                            stringOut += chr(plaintext[k])
                    iput = output
                elif mode == self.modeOfOperation["CBC"]:
                    output = self.aes.decrypt(ciphertext, key, size)
                    for i in range(16):
                        if firstRound:
                            plaintext[i] = IV[i] ^ output[i]
                        else:
                            plaintext[i] = iput[i] ^ output[i]
                    firstRound = False
                    if originalsize is not None and originalsize < end:
                        if bytes_string:
                            stringOut += bytes(plaintext)[:originalsize-start]
                        else:
                            for k in range(originalsize-start):
                                stringOut += chr(plaintext[k])
                    else:
                        if bytes_string:
                            stringOut += bytes(plaintext)
                        else:
                            for k in range(end-start):
                                stringOut += chr(plaintext[k])
                    iput = ciphertext
                elif mode == self.modeOfOperation["CTR"]:
                    if firstRound:
                        counter = int.from_bytes(bytes(IV[0:12] + [0,0,0,0]))
                        counterlist = self.convertToList(counter)
                        output = self.aes.encrypt(counterlist, key, size)
                        firstRound = False
                    else:
                        counter = counter + 1
                        counterlist = self.convertToList(counter)
                        output = self.aes.encrypt(counterlist, key, size)
                    for i in range(16):
                        if len(ciphertext)-1 < i:
                            plaintext[i] = output[i] ^ 0
                        else:
                            plaintext[i] = output[i] ^ ciphertext[i]
                    if bytes_string:
                        stringOut += bytes(plaintext)[:end-start]
                    else:
                        for k in range(end-start):
                            stringOut += chr(plaintext[k])
                    iput = ciphertext
        return stringOut


def encryptData(key, data, mode=AESModeOfOperation.modeOfOperation["CBC"]):
    """encrypt `data` using `key`

    `key` should be a string of bytes.

    returned cipher is a string of bytes prepended with the initialization
    vector.

    """
    key = map(ord, key)
    if mode == AESModeOfOperation.modeOfOperation["CBC"]:
        data = append_PKCS7_padding(data)
    keysize = len(key)
    assert keysize in AES.keySize.values(), 'invalid key size: %s' % keysize
    # create a new iv using random data
    iv = [ord(i) for i in os.urandom(16)]
    moo = AESModeOfOperation()
    (mode, length, ciph) = moo.encrypt(data, mode, key, keysize, iv)
    # With padding, the original length does not need to be known. It's a bad
    # idea to store the original message length.
    # prepend the iv.
    return ''.join(map(chr, iv)) + ''.join(map(chr, ciph))

def decryptData(key, data, mode=AESModeOfOperation.modeOfOperation["CBC"]):
    """decrypt `data` using `key`

    `key` should be a string of bytes.

    `data` should have the initialization vector prepended as a string of
    ordinal values.

    """

    key = map(ord, key)
    keysize = len(key)
    assert keysize in AES.keySize.values(), 'invalid key size: %s' % keysize
    # iv is first 16 bytes
    iv = map(ord, data[:16])
    data = map(ord, data[16:])
    moo = AESModeOfOperation()
    decr = moo.decrypt(data, None, mode, key, keysize, iv)
    if mode == AESModeOfOperation.modeOfOperation["CBC"]:
        decr = strip_PKCS7_padding(decr)
    return decr

def generateRandomKey(keysize):
    """Generates a key from random data of length `keysize`.
    
    The returned key is a string of bytes.
    
    """
    if keysize not in (16, 24, 32):
        emsg = 'Invalid keysize, %s. Should be one of (16, 24, 32).'
        raise ValueError (emsg % keysize)
    return os.urandom(keysize)

if __name__ == "__main__":
    import secrets

    moo = AESModeOfOperation()
    cleartext = "This is a test! This is a test! This is a test!"
    cipherkey = [143,194,34,208,145,203,230,143,177,246,97,206,145,92,255,84]
    iv = [103,35,148,239,76,213,47,118,255,222,123,176,106,134,98,92]
    mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["CBC"],
            cipherkey, moo.aes.keySize["SIZE_128"], iv)
    decr = moo.decrypt(ciph, orig_len, mode, cipherkey,
            moo.aes.keySize["SIZE_128"], iv)
    assert decr == cleartext

    cleartext = "This is a test! This is a test! This is a test!"
    cipherkey = [143,194,34,208,145,203,230,143,177,246,97,206,145,92,255,84]
    iv = [103,35,148,239,76,213,47,118,255,222,123,176,106,134,98,92]
    mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["OFB"],
            cipherkey, moo.aes.keySize["SIZE_128"], iv)
    decr = moo.decrypt(ciph, orig_len, mode, cipherkey,
            moo.aes.keySize["SIZE_128"], iv)
    assert decr == cleartext

    cleartext = "This is a test! This is a test! This is a test!"
    cipherkey = [143,194,34,208,145,203,230,143,177,246,97,206,145,92,255,84]
    iv = [103,35,148,239,76,213,47,118,255,222,123,176,106,134,98,92]
    mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["CFB"],
            cipherkey, moo.aes.keySize["SIZE_128"], iv)
    decr = moo.decrypt(ciph, orig_len, mode, cipherkey,
            moo.aes.keySize["SIZE_128"], iv)
    assert decr == cleartext
    
    cleartext = "This is a test! This is a test! This is a test!"
    cipherkey = [143,194,34,208,145,203,230,143,177,246,97,206,145,92,255,84]
    iv = [103,35,148,239,76,213,47,118,255,222,123,176,106,134,98,92]
    mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["CTR"],
            cipherkey, moo.aes.keySize["SIZE_128"], iv)
    decr = moo.decrypt(ciph, orig_len, mode, cipherkey,
            moo.aes.keySize["SIZE_128"], iv)
    assert decr == cleartext

    moo = AESModeOfOperation()
    cleartext = b"This is a test! This is a test! This is a test!"
    cipherkey = secrets.token_bytes(16)
    iv = secrets.token_bytes(16)
    mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["CBC"], cipherkey, moo.aes.keySize["SIZE_128"], iv)
    decr = moo.decrypt(ciph, orig_len, mode, cipherkey, moo.aes.keySize["SIZE_128"], iv)
    assert decr == cleartext

    moo = AESModeOfOperation()
    cleartext = b"This is a test! "
    cipherkey = secrets.token_bytes(24)
    iv = secrets.token_bytes(16)
    mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["CBC"],
            cipherkey, moo.aes.keySize["SIZE_192"], iv)
    decr = moo.decrypt(ciph, orig_len, mode, cipherkey,
            moo.aes.keySize["SIZE_192"], iv)
    assert decr == cleartext

    moo = AESModeOfOperation()
    cleartext = b"This is a test!"
    cipherkey = secrets.token_bytes(32)
    iv = secrets.token_bytes(16)
    mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["CBC"],
            cipherkey, moo.aes.keySize["SIZE_256"], iv)
    decr = moo.decrypt(ciph, orig_len, mode, cipherkey,
            moo.aes.keySize["SIZE_256"], iv)
    assert decr == cleartext

    moo = AESModeOfOperation()
    cleartext = b"This is a test! This is a test! This is a test!"
    cipherkey = secrets.token_bytes(16)
    iv = secrets.token_bytes(16)
    mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["OFB"],
            cipherkey, moo.aes.keySize["SIZE_128"], iv)
    decr = moo.decrypt(ciph, orig_len, mode, cipherkey,
            moo.aes.keySize["SIZE_128"], iv)
    assert decr == cleartext

    moo = AESModeOfOperation()
    cleartext = b"This is a test! "
    cipherkey = secrets.token_bytes(24)
    iv = secrets.token_bytes(16)
    mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["OFB"],
            cipherkey, moo.aes.keySize["SIZE_192"], iv)
    decr = moo.decrypt(ciph, orig_len, mode, cipherkey,
            moo.aes.keySize["SIZE_192"], iv)
    assert decr == cleartext

    moo = AESModeOfOperation()
    cleartext = b"This is a test!"
    cipherkey = secrets.token_bytes(32)
    iv = secrets.token_bytes(16)
    mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["OFB"],
            cipherkey, moo.aes.keySize["SIZE_256"], iv)
    decr = moo.decrypt(ciph, orig_len, mode, cipherkey,
            moo.aes.keySize["SIZE_256"], iv)
    assert decr == cleartext

    moo = AESModeOfOperation()
    cleartext = b"This is a test! This is a test! This is a test!"
    cipherkey = secrets.token_bytes(16)
    iv = secrets.token_bytes(16)
    mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["CFB"],
            cipherkey, moo.aes.keySize["SIZE_128"], iv)
    decr = moo.decrypt(ciph, orig_len, mode, cipherkey,
            moo.aes.keySize["SIZE_128"], iv)
    assert decr == cleartext

    moo = AESModeOfOperation()
    cleartext = b"This is a test! "
    cipherkey = secrets.token_bytes(24)
    iv = secrets.token_bytes(16)
    mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["CFB"],
            cipherkey, moo.aes.keySize["SIZE_192"], iv)
    decr = moo.decrypt(ciph, orig_len, mode, cipherkey,
            moo.aes.keySize["SIZE_192"], iv)
    assert decr == cleartext

    moo = AESModeOfOperation()
    cleartext = b"This is a test!"
    cipherkey = secrets.token_bytes(32)
    iv = secrets.token_bytes(16)
    mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["CFB"],
            cipherkey, moo.aes.keySize["SIZE_256"], iv)
    decr = moo.decrypt(ciph, orig_len, mode, cipherkey,
            moo.aes.keySize["SIZE_256"], iv)
    assert decr == cleartext

    moo = AESModeOfOperation()
    cleartext = b"This is a test! This is a test! This is a test!"
    cipherkey = secrets.token_bytes(16)
    iv = secrets.token_bytes(16)
    mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["CTR"],
            cipherkey, moo.aes.keySize["SIZE_128"], iv)
    decr = moo.decrypt(ciph, orig_len, mode, cipherkey,
            moo.aes.keySize["SIZE_128"], iv)
    assert decr == cleartext

    moo = AESModeOfOperation()
    cleartext = b"This is a test! "
    cipherkey = secrets.token_bytes(24)
    iv = secrets.token_bytes(16)
    mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["CTR"],
            cipherkey, moo.aes.keySize["SIZE_192"], iv)
    decr = moo.decrypt(ciph, orig_len, mode, cipherkey,
            moo.aes.keySize["SIZE_192"], iv)
    assert decr == cleartext

    moo = AESModeOfOperation()
    cleartext = b"This is a test!"
    cipherkey = secrets.token_bytes(32)
    iv = secrets.token_bytes(16)
    mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["CTR"],
            cipherkey, moo.aes.keySize["SIZE_256"], iv)
    decr = moo.decrypt(ciph, orig_len, mode, cipherkey,
            moo.aes.keySize["SIZE_256"], iv)
    assert decr == cleartext

    moo = AESModeOfOperation()
    cleartext = secrets.token_bytes(10000)
    cipherkey = secrets.token_bytes(32)
    iv = secrets.token_bytes(16)
    mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["CTR"],
            cipherkey, moo.aes.keySize["SIZE_256"], iv)
    decr = moo.decrypt(ciph, orig_len, mode, cipherkey,
            moo.aes.keySize["SIZE_256"], iv)
    assert decr == cleartext
