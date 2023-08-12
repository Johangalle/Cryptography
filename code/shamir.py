#!/usr/bin/python3
#
#Implementation of Shamir Secret Sharing Scheme
# code partly copied from https://www.geeksforgeeks.org/implementing-shamirs-secret-sharing-scheme-in-python/
# The code ran on Python2 and Python3, but has not been tested on Python2.7 for a while.
#
# Written by Johan Galle
#
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/
#
# No part of this module should be used for cryptography in production.
# This module is strictly for education purposes.
#

import random
from cryptocourse import euclidean

random.seed(None)
#  Of course, this is not truly random, so not acceptable from a security point of view
      
global field_size
# This is a prime number to avoid the problem that the multiplicative inverse would not exist
# For that purpose, I generated some prime numbers of the form pow(2,i) - 1
# You can take any prime number
# No secrets larger than this number can be used
# field_size = 31
# field_size = 127
# field_size = 8191
# field_size = 524287
field_size = 2147483647
# field_size = 2305843009213693951
# field_size = 170141183460469231731687303715884105727
# field_size = 6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057151
# field_size = 285542542228279613901563566102164008326164238644702889199247456602284400390600653875954571505539843239754513915896150297878399377056071435169747221107988791198200988477531339214282772016059009904586686254989084815735422480409022344297588352526004383890632616124076317387416881148592486188361873904175783145696016919574390765598280188599035578448591077683677175520434074287726578006266759615970759521327828555662781678385691581844436444812511562428136742490459363212810180276096088111401003377570363545725120924073646921576797146199387619296560302680261790118132925012323046444438622308877924609373773012481681672424493674474488537770155783006880852648161513067144814790288366664062257274665275787127374649231096375001170901890786263324619578795731425693805073056119677580338084333381987500902968831935913095269821311141322393356490178488728982288156282600813831296143663845945431144043753821542871277745606447858564159213328443580206422714694913091762716447041689678070096773590429808909616750452927258000843500344831628297089902728649981994387647234574276263729694848304750917174186181130688518792748622612293341368928056634384466646326572476167275660839105650528975713899320211121495795311427946254553305387067821067601768750977866100460014602138408448021225053689054793742003095722096732954750721718115531871310231057902608580607
   
def reconstructSecret(shares, primefield = field_size):
      
    # Combines shares using
    # Lagranges interpolation.
    # Shares is an array of shares
    # being combined
    sums = 0
      
    for j in range(len(shares)):
        xj, yj = shares[j][0],shares[j][1]
        numerator = yj
        denominator = 1
        prod = 1
          
        for i in range(len(shares)):
            xi = shares[i][0]
            if i != j:
                numerator *= -xi
                denominator *= (xj-xi)
                numerator = numerator%primefield
                denominator = denominator%primefield
        inverse_denominator = euclidean.mulinv(denominator,primefield)
        prod *= numerator*inverse_denominator%primefield
        # print (numerator, denominator, inverse_denominator)
        sums += prod
          
    return sums%primefield
   
def polynom(x,coeff, primefield = field_size):
      
    # Evaluates a polynomial in x
    # with coeff being the coefficient
    # list
    return sum([x**(len(coeff)-i-1) * coeff[i] for i in range(len(coeff))])%primefield
   
def coeff(t,secret, primefield = field_size):
      
    # Randomly generate a coefficient
    # array for a polynomial with
    # degree t-1 whose constant = secret
    # the coefficients are allowed to be zero, but the coefficient for the highest degree should not be 0
    # coeff is a list with the leftmost element corresponding to the highest degree (t-1), and
    # the rightmost element corresponding to the lowest degree (0)
    # It is a list of t elements with the rightmost element being equal to secret
    # The coefficients are integers between 0 and primefield - 1
    coeff = [random.randrange(0, primefield) for _ in range(t-1)]
    if coeff[0] == 0:
        coeff[0] = random.randrange(1, primefield)
    coeff.append(secret)
      
    return coeff
   
def generateShares(n,m,secret, primefield=field_size, Shamir_style = False):
      
    # Split secret using SSS into
    # n shares with threshold m
    # Shamir style implies that the n values chosen are 1, 2, ..., n; otherwise, they can be chosen randomly
    cfs = coeff(m,secret, primefield)
    shares = []
      
    for i in range(1,n+1):
        if Shamir_style:
            r = i
        else:
            r = random.randrange(1, primefield)
        shares.append([r, polynom(r,cfs, primefield)])
      
    return shares
  
def lagrangeInterpolate (x,xyvalues, primefield = field_size):
    sums = 0
    for j in range(len(xyvalues)):
        xj, yj = xyvalues[j][0],xyvalues[j][1]
        numerator = yj
        denominator = 1
        prod = 1
        # print (j, numerator)
          
        for i in range(len(xyvalues)):
            xi = xyvalues[i][0]
            if i != j:
                numerator *= (x - xi)
                denominator *= (xi-xj)
                numerator = numerator%primefield
                denominator = denominator%primefield
                
        inverse_denominator = euclidean.mulinv(denominator,primefield)
        prod *= numerator*inverse_denominator%primefield
        # print (numerator, denominator, inverse_denominator)
        sums += prod
          
    return sums%primefield
  
def addShares (shares1, shares2, primefield = field_size):
    shares3 = []
    if len(shares1) != len(shares2):
        raise ValueError("incompatible lengths")
    else:
        for j in range(len(shares1)):
            xj = shares1[j][0]
            yj = shares1[j][1]
            found = False
            for i in range(len(shares2)):
                xi = shares2[i][0]
                if xi == xj:
                    yi = shares2[i][1]
                    valuePair = [xi, (yi+yj)%primefield]
                    found = True
            if found:
                shares3.append(valuePair)
            else:
                raise ValueError("x-value " + str(xi) + " not found")
        return shares3

def subtractShares (shares1, shares2, primefield = field_size):
    shares3 = []
    if len(shares1) != len(shares2):
        raise ValueError("incompatible lengths")
    else:
        for j in range(len(shares1)):
            xj = shares1[j][0]
            yj = shares1[j][1]
            found = False
            for i in range(len(shares2)):
                xi = shares2[i][0]
                if xi == xj:
                    yi = shares2[i][1]
                    valuePair = [xi, (yj-yi)%primefield]
                    found = True
            if found:
                shares3.append(valuePair)
            else:
                raise ValueError("x-value " + str(xi) + " not found")
        return shares3


def mulShares (shares1, shares2, primefield = field_size):
    shares3 = []
    if len(shares1) != len(shares2):
        raise ValueError("incompatible lengths")
    else:
        for j in range(len(shares1)):
            xj = shares1[j][0]
            yj = shares1[j][1]
            found = False
            for i in range(len(shares2)):
                xi = shares2[i][0]
                if xi == xj:
                    yi = shares2[i][1]
                    valuePair = [xi, (yi*yj)%primefield]
                    found = True
            if found:
                shares3.append(valuePair)
            else:
                raise ValueError("x-value " + str(xi) + " not found")
        return shares3

def linearCombinationOfShares(listOfShares, listOfCoefficients, fixedTerm, primefield = field_size):
    sharesResult = []
    for j in range(len(listOfShares[0])):
        sharesResult.append([j+1,fixedTerm])
    if len(listOfShares) != len(listOfCoefficients):
        raise ValueError("incompatible lengths")
    else:
        for i in range(len(listOfShares)):
            for j in range(len(listOfShares[0])):
                sharesResult [j][1] = (sharesResult [j][1] + listOfShares[i][j][1]*listOfCoefficients[i])%primefield
    return sharesResult
  
# Driver code
if __name__ == '__main__':
      
    # (3,5) sharing scheme
    t,n = 3, 5
    secret = 123456789
    # Python 3
    print('Original Secret:', secret)
    # Python 2
    # print 'Original Secret:', secret
   
    # Phase I: Generation of shares
    shares = generateShares(n, t, secret)
    # Python 3
    print('\nShares:', *shares)
    # Python 2
    # print '\nShares:', shares
   
    # Phase II: Secret Reconstruction
    # Picking t shares randomly for
    # reconstruction
    pool = random.sample(shares, t)
    
    # Python 3
    print('\nCombining shares:', *pool)
    # Python 2
    # print '\nCombining shares:', pool
    
    # Python 3
    print('Reconstructed secret:', reconstructSecret(pool))
    # Python 2
    # print 'Reconstructed secret:', reconstructSecret(pool)
