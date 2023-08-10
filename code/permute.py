#!/usr/bin/python3
#
# This module groups two fundtions: permute and lfsr.
#
# permute can be used as part of a block cipher algorithm to perform permutation.
#
# lfsr is an implementation of a linear feedback shift register which can be part of a stream cipher.
#
# Written by Johan Galle
#
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/
#
# No part of this module should be used for cryptography in production.
# This module is strictly for education purposes.
#
def byte(number, i):
    return (number & (0xff << (i * 8))) >> (i * 8)
    
def permute(b,sequence):
    # example: b = 0x1234567890, s = [3,2,4,1,0]
    # this produces result = 0x5612347890
    # Position 0 is the rightmost position, position 1 is the position at the left, etc
    # So, the first byte (0x12) should come at position 3 which is the leftmost position but one
    # The second byte (0x34) should come at position 2, which is in the middle
    # The third byte (0x56) should come at positon 4 which is at the leftmost position
    # The fourth byte (0x78) should come at position 1, which is the rightmost position but one
    # The fifth byte (0x90) should come at position 0, which is the rightmost position
    if isinstance(b, bytes):
        bytes_string = True
        b = int.from_bytes(b)
    if int((len(hex(b).rstrip("L")) - 1)/2) > len(sequence):
        raise ValueError('byte length %s too big for sequence with length %s' %((len(hex(b)) - 1)/2, len(sequence)))
    else:
        result = 0
        index = 0
        s = list(sequence)
        s.reverse()
        for l in s:
            result = result + pow(2,l*8)*byte(b,index)
            index = index + 1
        if bytes_string:
            hexstr = hex(result)[2:]
            if len(hexstr)%2 == 1:
                hexstr = '0' + hexstr
            return bytes.fromhex(hexstr)
        else:
            return result


def lfsr(seed, mask,length,nbits = 0):
# seed = the initial value with the oldest bit being the most significant
# mask = the coefficients ci of the linear feedback shift register
#        the coefficients linked to the oldest values are the most significant bits
#
# example:
#   seed = 0b10110: the initial value of the register;
#          the result shall start with this number
#   mask = 0b11001
#          This represents the formula sn = s[n-5] + s[n-4] + s[n-1]
#          This corresponds with the connection polynomial X^5 + X^4 + X + 1
#   length: the number of bits we want to receive as output
#   returns: the full stream consisting of length number of bits
#            produced as output by the linear feedback shift register
# Performance of this function was never a goal;
# You should be able to use this function to produce streams of 1 million bits
# if the length of the mask does not correspond with the number of bits, you should
# provide it as a parameter
    if nbits == 0:
        nbits = mask.bit_length()
    result = seed
    all_ones = pow(2,nbits) - 1
    length_so_far = nbits
    while length_so_far < length:
        newbit = bin(mask&seed).count('1')%2
        seed = (seed<<1 & all_ones) + newbit
        result = (result<<1) + newbit
        length_so_far += 1
    hexresult = hex(result)[2:]
    if len(hexresult)%2 == 1:
        hexresult = '0' + hexresult
    return bytes.fromhex(hexresult)
