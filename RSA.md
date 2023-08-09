# Asymmetric encryption (RSA)
Code snippets to learn cryptography without the need to use other libraries. DO NOT USE IN PRODUCTION.

RSA is the oldest asymmetric encryption (or public key) algorithm and is still used today. 

Prime numbers and factorisation into prime numbers is a major foundation of RSA. 

Factoring a number n = p*q (p and q being prime numbers) into the two factors p and q is a hard problem. 
Determining whether a given number is prime or not is easy (Miller-Rabin or other algorithms). Finding the least common multiple or the greatest common divisor of two numbers is also an easy problem (Euclidean algorithm).

The extended euclidean algorithm is used to calculate the multiplicative inverse. 

## Determining whether a given number is prime or not
```
>>> import primes
>>> p = 2453
>>> primes.miller_rabin(p)
False
>>> p = 2457
>>> primes.miller_rabin(p)
False
>>> p = 2459
>>> primes.miller_rabin(p)
True
```
## Using the euclidean algorithm to find the greatest common divisor and the lowest common multiple
```
>>> import euclidean
>>> n1 = 93353879449
>>> n2 = 2104755767
>>> a = euclidean.gcd(n1,n2)
>>> a
9511
>>> b = euclidean.lcm(n1,n2)
>>> b
20658933460425353
>>> n1*n2/b
9511.0
```
## Using the extended euclidean algorithm to find the multiplicative inverse
```
>>> import euclidean
>>> euclidean.mulinv(5,17)  # What do we need to multiply 5 with in order to obtain 1 in modulo 17?
7
>>> 5*7%17    # % = remainder or modulo
1
```
## Determining suitable parameters for RSA (small number example)
```
>>> import euclidean
>>> import primes
>>> p = primes.findAPrime(30,100)
>>> q = primes.findAPrime(30,100)
>>> n = p*q
>>> p, q, n
(31, 79, 2449)
>>> totient_n = (p-1)*(q-1)
>>> e = 3
>>> d = euclidean.mulinv(e, totient_n)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/johangalle/Public/Sources/cryptocourse2/euclidean.py", line 67, in mulinv
    raise ValueError('multiplicative inverse is not possible if values are not relatively prime ')
ValueError: multiplicative inverse is not possible if values are not relatively prime 
>>> e = 5
>>> d = euclidean.mulinv(e, totient_n)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/johangalle/Public/Sources/cryptocourse2/euclidean.py", line 67, in mulinv
    raise ValueError('multiplicative inverse is not possible if values are not relatively prime ')
ValueError: multiplicative inverse is not possible if values are not relatively prime 
>>> e = 7
>>> d = euclidean.mulinv(e, totient_n)
>>> plain = 1234    # should be smaller than n
>>> cipher = pow(plain,e,n)
>>> cipher
2288
>>> decrypt = pow(cipher,d,n)
>>> decrypt
1234
>>> public = (n,e)
>>> private = (n,d)
>>> 
>>> totient_n/3
780.0
>>> totient_n/5
468.0
>>> totient_n/7
334.2857142857143
```
## Determining suitable parameters for RSA (large number example)
```
>>> import primes
>>> import euclidean
>>> p = primes.findAPrime(pow(2,2000), pow(2,2100))
>>> q = primes.findAPrime(pow(2,2000), pow(2,2100))
>>> n = p*q
>>> n.bit_length(), p.bit_length(), q.bit_length()
(4190, 2098, 2092)
>>> totient_n = (p-1)*(q-1)
>>> e = 65537      # This is a convention
>>> bin(e)
'0b10000000000000001'     # The exponentiation function is more efficient with fewer 1's
>>> d = euclidean.mulinv(e, totient_n)
>>> plain = 1234567890987654321    # should be smaller than n
>>> cipher = pow(plain,e,n)
>>> decrypt = pow(cipher,d,n)
>>> decrypt
1234567890987654321
>>> 
>>> reduced_totient = euclidean.lcm(p-1, q-1)
>>> d = euclidean.mulinv(e, reduced_totient)
>>> plain = 1234567890987654321 
>>> cipher = pow(plain,e,n)
>>> decrypt = pow(cipher,d,n)
>>> decrypt
1234567890987654321
```
