#!/usr/bin/python3
#
# Miller_rabin based on Dendi Suhubdy's RSA Implementation Running on Python 3.6
# See https://gist.github.com/dendisuhubdy/e2e67d796605dbf4860aa6e94201690a
#
# and on William Stallings Cryptography and Network Security book.
#
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/
#
# This module supports the miller_rabin function to check whether a given number is prime or not.
# This module also supports the random generation of primes
# as well as the random generation of safe primes.
# The function largest_prime_factor should be used with caution, i.e. use it with small numbers only.
#
# This is a pure Python implementation, not even using any of the Python standard built-in libraries.
#
# No part of this module should be used for cryptography in production.
# This module is strictly for education purposes.
#
import secrets
secretsGenerator = secrets.SystemRandom()

def largest_prime_factor(n):
    # We try all possible divisors starting with 2 
    # and continuing to 3, 5, 7, ... until sqrt(n)
    # Each time when we find a divisor i, 
    # we replace n by n / i
    i = 2
    step = 1
    teller3 = -1
    teller5 = -2
    while i * i <= n:
        if n % i != 0:
            i = i + step
            teller3 = teller3 + 1
            teller5 = teller5 + 1
            if teller3 != 2 and teller5 != 4:
                step = 2
            else:
                if teller3 != 1 and teller5 != 3:
                    step = 4
                    teller3 = (teller3 + 1)%3
                    teller5 = (teller5 + 1)%5
                else:
                    step = 6
                    teller3 = (teller3 + 2)%3
                    teller5 = (teller5 + 2)%5                
        else:
            n = n // i
    return n

def power(x, m, n):
    # Calculate x^m modulo n using O(log(m)) operations
    # We calculate all the powers x, x^2, x^4, x^8, ...
    # and decide whether we need this particular power
    # for x^m.
    # Example: x^11 = x * x^2 * x^8
    #
    # This is really just for the educational purpose as this is equivalent
    # with the built in function pow(x,m,n)
    #
    a = 1
    while m > 0:
        if m % 2 == 1:
            a = (a * x) % n
        x = (x * x) % n
        m = m // 2
    return a

def miller_rabin(n, ctr=10):
    if n <= 2:
        return True

    def check(a, k, q, n):
        # n = 2^k * q
        # For this value of a, we check whether
        # a^q == 1
        # OR
        # one of the values a^q, a^2q, a^4q, a^8q, ..., a^(k-1)q == n - 1
        # If one of these conditions is True, we return True
        # True means that n may be a prime
        x = pow(a, q, n)
        if x == 1:
            return True
        for i in range(k - 1):
            if x == n - 1:
                return True
            x = pow(x, 2, n)
        return x == n - 1

    # find k, d so that n = 2^k * d 
    # and d is odd
    k = 0
    d = n - 1
    while d % 2 == 0:
        d = d // 2
        k = k + 1

    # We check the miller-rabin condition
    # for a number of random values of a
    # If one of these checks returns False, the end result is False
    # If all of these checks return True, the end result is True
    for i in range(ctr):
        a = secretsGenerator.randrange(2, n - 1)
        if not check(a, k, d, n):
            return False
    return True

SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

def checkSmallPrimeFactors(p):
    # Checks whether this candidate prime number p could be a prime
    # We check whether p has divisors in the first list of primes
    for i in SMALL_PRIMES:
        if p%i == 0 and i*i <= p:
            return False
    return True

def findAPrime(a, b):
    # Return a pseudo prime number roughly between a and b,
    # (could be larger than b). Raise ValueError if cannot find a
    # pseudo prime after 10 * ln(x) + 3 tries. 
    #
    # The distribution of primes tells us that we should on average find 
    # a new prime after ln(x) non-primes
    # To be very sure, we do not give up after ln(x) non-primes 
    # but only after 8*ln(x) tries
    # Because we only check the odd numbers, we need to try only 4*ln(x)
    #
    # This should never happen
    # 
    # Say that the bit length of x = n
    # So, x <= 2^nrOfBits
    # 4*ln(x) = 4*ln(2^nrOfBits) = 4*nrOfBits*ln(2) = 4*nrOfBits*0.69 < 3*nrOfBits
    #
    x = secretsGenerator.randint(a, b)
    if x%2 == 0:
        x = x + 1
    nrOfBits = x.bit_length()
    for i in range(0, 3*nrOfBits):
        if miller_rabin(x,50):
            return x
        else:
            x = x + 2 #increase x with 2 and try again
    raise ValueError

def findASafePrime(a,b):
    # Safe primes are of the form q = 2*p + 1
    # Safe primes are special in the sense that 
    # and q - 1 = 2*p is guaranteed to have a large 
    # prime factor
    # The average distribution for safe primes is [ln(n)]^2
    # For 1024 bits (and only odd numbers), we need to
    # test on average 1024*0.69/2 = 353.
    # So, one chance in 353 to find a prime.
    # But one chance in 353^2 = 125000 to find a safe prime !
    # So, this function may take a while to complete
    # Because miller_rabin takes quite some time, we want a
    # sequence of quick to less quick to slow test to perform
    # the tests on both p and q before we spend too much time 
    # proving that e.g. p is a prime if we could easily
    # have found out quickly that q is not a prime
    #
    # It is also known that for all safe primes q > 7,
    # q = 11 (mod 12)
    if b <= a:
        b = a*4
    p = secretsGenerator.randint(a, b)
    if p % 2 == 0:
        p = p + 1
    q = 2*p + 1
    while True:
        # print "checking p = ", p, "q = ", q
        if q%12 == 11:
            if checkSmallPrimeFactors(p) and checkSmallPrimeFactors(q):
                if miller_rabin(p,2) and miller_rabin(q,2):
                    if miller_rabin(p,4) and miller_rabin(q,4):
                        if miller_rabin(p,8) and miller_rabin(q,8):
                            if miller_rabin(p,10) and miller_rabin(q,10):
                                return q
        p = p + 2 #increase x with 2 and try again
        q = 2*p + 1
        
def findASafePrime2(a,b):
    # Safe primes are of the form q = 2*p + 1
    # Safe primes are special in the sense that 
    # p - 1 and q - 1 = 2*p is guaranteed to have a large
    # prime factor
    while True:
        p = findAPrime(a, b)
        q = 2*p + 1
        if miller_rabin(q,20):
            return q 


if __name__ == '__main__':       
    n1 = largest_prime_factor(143)
    assert n1 == 13
    
    n1 = largest_prime_factor(1541)
    assert n1 == 67
    
    n1 = largest_prime_factor(24465482849)
    assert n1 == 198811

    p1 = findAPrime (1000000, 2000000)
    p2 = findAPrime (p1+1, 2000000)
    nr = 2*3*p1*p2
    n1 = largest_prime_factor(nr)
    assert n1 == p2
    
    p1 = findASafePrime(10000000,20000000)
    q1 = p1 // 2
    assert miller_rabin(p1) and miller_rabin(q1)
    
    print ("This may take a while")
    p1 = findAPrime (pow(2,2023), pow(2,2024))
    assert miller_rabin(p1)
    print ("end")
