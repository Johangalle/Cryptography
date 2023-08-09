# Asymmetric encryption (RSA)
Code snippets to learn cryptography without the need to use other libraries. DO NOT USE IN PRODUCTION.

RSA is the oldest asymmetric encryption (or public key) algorithm and is still used today. 

Prime numbers and factorisation into prime numbers is a major foundation of RSA. 

Factoring a number n = p*q (p and q being prime numbers) into the two factors p and q is a hard problem. 
Determining whether a given number is prime or not is easy (Miller-Rabin or other algorithms). Finding the least common multiple or the greatest common divisor of two numbers is also an easy problem (Euclidean algorithm).

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
>>> n1 = 93353879449
>>> n2 = 2104755767
>>> a = euclidean.gcd(n1,n2)
9511
>>> b = euclidean.lcm(n1,n2)
20658933460425353
>>> n1*n2/b
9511.0
```
