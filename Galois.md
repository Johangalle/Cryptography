# Galois multiplication
Code snippets to learn cryptography without the need to use other libraries. DO NOT USE IN PRODUCTION

Galois multiplication is the core of finite filed arithmetic and is the core of modern encryption algorithms such as AES.
I expect you to be able to calculate Galois multiplications by hand, but this module offers the implementation anyway.

The coefficients of the polynomials are always modulo some number. Most of the time, this modulo is 2.

## Adding polynomials (including unary negation)
```
>>> import galois
>>> p = galois.Polynomial(5,1,2,3,4)
>>> q = galois.Polynomial(5,1,2,0,0)
>>> p
Polynomial (modulo 5) : 1*x^3+2*x^2+3*x+4
>>> q
Polynomial (modulo 5) : 1*x^3+2*x^2+0
>>> p+q
Polynomial (modulo 5) : 2*x^3+4*x^2+3*x+4
>>> p+(-q)
Polynomial (modulo 5) : 3*x+4
>>> 
>>> p = galois.Polynomial(2,1,2,3,4)
>>> 
>>> 
>>> p = galois.Polynomial(2,1,1,1,1)
>>> q = galois.Polynomial(2,1,0,1)
>>> p
Polynomial (modulo 2) : 1*x^3+1*x^2+1*x+1
>>> q
Polynomial (modulo 2) : 1*x^2+1
>>> p+q
Polynomial (modulo 2) : 1*x^3+1*x+0
>>> p+(-q)
Polynomial (modulo 2) : 1*x^3+1*x+0
```
## Multiplying polynomials
```
>>> p = galois.Polynomial(2,1,0,0,1,0,1,0,1)   
>>> q = galois.Polynomial(2,1,0,0,0,1,0,1,0)
>>> p
Polynomial (modulo 2) : 1*x^7+1*x^4+1*x^2+1
>>> q
Polynomial (modulo 2) : 1*x^7+1*x^3+1*x+0
>>> irred8 = galois.Polynomial(2,1,0,0,0,1,1,0,1,1)
>>> p.set_irreducible_polynomial(irred8)
>>> q.set_irreducible_polynomial(irred8)
>>> res = p * q
>>> res
Polynomial (modulo 2) : 1
>>> q = galois.Polynomial(2,1,0,1,0)
>>> q
Polynomial (modulo 2) : 1*x^3+1*x+0
>>> q.set_irreducible_polynomial(irred8)
>>> res = p * q
>>> res
Polynomial (modulo 2) : 1*x^7+1*x^6+1*x^5+1*x^4+1*x^2+1
```
## Converting polynomials and numbers
```
>>> poly = galois.poly_from_int(3)
>>> poly
Polynomial (modulo 2) : 1*x+1
>>> poly.to_int()
3
```
## Galois multiplication of numbers
```
>>> irred8 = galois.Polynomial(2,1,0,0,0,1,1,0,1,1)
>>> res = galois.galois_multiply(0x95,0x8a,irred8)
>>> res
1
>>> res = galois.galois_multiply(245,255,irred8)
>>> res
79
```
## Galois multiplicative inverse
```
>>> i = galois.galois_inverse(228, irred8)
>>> i
198
>>> res = galois.galois_multiply(i,228,irred8)
>>> galois.galois_multiply(i,228,irred8)
1
```
## Example irreducible polynomials
Irreducible polynomials cannot be divided by any other smaller degree polynomial.

Determining irreducible polynomials is considered out of scope of the course. For meaningful multiplication, you always need an irreducible polynomial. Such a polynomial shall always be supplied if required.

```
x+1
x^2 + x + 1
x^3 + x + 1
x^3 + x^2 + 1
x^4 + x + 1
x^4 + x^3 + 1
x^5 + x^2 + 1
x^5 + x^3 + 1
x^5 + x^3 + x^2 + x + 1
x^5 + x^4 + x^2 + x + 1
x^5 + x^4 + x^3 + x + 1
x^5 + x^4 + x^3 + x^2 + 1
x^6 + x + 1
x^6 + x^4 + x^3 + x + 1
x^6 + x^5 + 1
x^6 + x^5 + x^2 + x + 1
x^6 + x^5 + x^3 + x^2 + 1
x^6 + x^5 + x^4 + x + 1
x^7 + x + 1
x^7 + x^3 + 1
x^7 + x^3 + x^2 + x + 1
x^7 + x^4 + 1
x^7 + x^4 + x^3 + x^2 + 1
x^7 + x^5 + x^2 + x + 1
x^7 + x^5 + x^3 x + 1
x^7 + x^5 + x^4 + x^3 + 1
x^7 + x^5 + x^4 + x^3 + x^2 + x + 1
x^7 + x^6 + 1
x^7 + x^6 + x^3 + x + 1
x^7 + x^6 + x^4 + x + 1
x^7 + x^6 + x^4 + x^2 + 1
x^7 + x^6 + x^5 + x^2 + 1
x^7 + x^6 + x^5 + x^3 + x^2 + x + 1
x^7 + x^6 + x^5 + x^4 + 1
x^7 + x^6 + x^5 + x^4 + x^2 + x + 1
x^7 + x^6 + x^5 + x^4 + x^3 + x^2 + 1
x^8 + x^4 + x^3 + x + 1
x^8 + x^4 + x^3 + x^2 + 1
x^8 + x^5 + x^3 + x + 1
x^8 + x^5 + x^3 + x^2 + 1
x^8 + x^6 + x^3 + x^2 + 1
x^8 + x^6 + x^4 + x^3 + x^2 + x + 1
x^8 + x^6 + x^5 + x + 1
x^8 + x^6 + x^5 + x^2 + 1
x^8 + x^6 + x^5 + x^3 + 1
x^8 + x^6 + x^5 + x^4 + 1
x^8 + x^7 + x^2 + x + 1
x^8 + x7 + x3 + x2 + 1
x^8 + x7 + x5 + x3 + 1
x^8 + x7 + x6 + x + 1
x^8 + x^7 + x^6 + x^3 + x^2 + x + 1
x^8 + x^7 + x^6 + x^5 + x^2 + x + 1
x^8 + x^7 + x^6 + x^5 + x^4 + x^2 + 1
```
