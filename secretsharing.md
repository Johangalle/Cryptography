# Secret sharing
Code snippets to learn cryptography without the need to use other libraries. DO NOT USE IN PRODUCTION.

Secret sharing allows to split a secret into a number of shares in a (t,n) scheme. Given at least t shares, we can reconstruct the secret.

## Secret sharing with default parameters
```
>>> import shamir
>>> t,n = 3,7
>>> secret = 1234
>>> shares = shamir.generateShares(n,t,secret)    # all calculations are done using a default prime as modulo
>>> shares     # Note that these shares have random x values
[[1022756980, 1970664245], [885629270, 960624785], [657345916, 626113163], [1204024348, 991024408], [955576390, 2027332549], [2035145887, 738636443], [1368596146, 2066603660]]
>>> import random
>>> pool = random.sample(shares, t)
>>> pool
[[955576390, 2027332549], [1204024348, 991024408], [885629270, 960624785]]
>>> 
>>> reconstructed_secret = shamir.reconstructSecret(pool)
>>> reconstructed_secret
1234
>>> reconstructed_secret == secret
True
```
## Secret sharing with a chosen prime as modulo
```
>>> import shamir
>>> t,n = 3,7
>>> secret = 12
>>> p = 113
>>> shares = shamir.generateShares(n,t,secret, p)
>>> shares
[[48, 50], [97, 72], [43, 21], [55, 36], [45, 93], [16, 26], [109, 13]]
>>> import random
>>> pool = random.sample(shares, t)
>>> pool
[[109, 13], [97, 72], [48, 50]]
>>> reconstructed_secret = shamir.reconstructSecret(pool)
>>> reconstructed_secret
1988703110
>>> reconstructed_secret = shamir.reconstructSecret(pool, p)
>>> reconstructed_secret
12
>>> reconstructed_secret == secret
True
```
## Secret sharing, Shamir style
```
>>> import shamir
>>> t,n = 3,7
>>> secret = 12
>>> p = 113
>>> shares = shamir.generateShares(n,t,secret, p, Shamir_style = True)
>>> shares
[[1, 28], [2, 5], [3, 56], [4, 68], [5, 41], [6, 88], [7, 96]]
>>> import random
>>> pool = random.sample(shares, t)
>>> pool
[[2, 5], [7, 96], [4, 68]]
>>> reconstructed_secret = shamir.reconstructSecret(pool, p)
>>> reconstructed_secret
12
>>> reconstructed_secret == secret
True
```
## Adding shares, Shamir style
```
>>> import shamir
>>> t,n = 3,7
>>> p = 113
>>> secret1 = 12
>>> shares1 = shamir.generateShares(n,t,secret1,p,Shamir_style = True)
>>> secret2 = 13
>>> shares2 = shamir.generateShares(n,t,secret2,p,Shamir_style = True)
>>> shares1
[[1, 72], [2, 85], [3, 51], [4, 83], [5, 68], [6, 6], [7, 10]]
>>> shares2
[[1, 19], [2, 35], [3, 61], [4, 97], [5, 30], [6, 86], [7, 39]]
>>> shares3 = shamir.addShares(shares1, shares2, primefield = p)
>>> shares3
[[1, 91], [2, 7], [3, 112], [4, 67], [5, 98], [6, 92], [7, 49]]
>>> shamir.reconstructSecret(shares3, p)
25
```
## Multiplying shares, Shamir style
```
>>> import shamir
>>> t,n = 4,7
>>> p = 113
>>> secret1 = 4
>>> shares1 = shamir.generateShares(n,t,secret1, p, Shamir_style = True)
>>> shares1
[[1, 39], [2, 80], [3, 84], [4, 8], [5, 35], [6, 9], [7, 0]]
>>> secret2 = 12
>>> shares2 = shamir.generateShares(n,t,secret2,p, Shamir_style = True)
>>> shares2
[[1, 21], [2, 55], [3, 77], [4, 50], [5, 50], [6, 40], [7, 96]]
>>> shares3 = shamir.mulShares(shares1, shares2, primefield = p)
>>> shares3
[[1, 28], [2, 106], [3, 27], [4, 61], [5, 55], [6, 21], [7, 0]]
>>> shamir.reconstructSecret(shares3, p)      # This result is correct because t = 4 implies a 3rd degree polynomial
                                              # Multiplying 2 3rd degree polynomials results in a 6th degree polynomial
                                              # n = 7 points and thsi is enough to uniquely identify a 6th degree polynomial
48
>>> 
>>> import shamir
>>> t,n = 5,7
>>> p = 113
>>> secret1 = 4
>>> shares1 = shamir.generateShares(n,t,secret1, p, Shamir_style = True)
>>> shares1
[[1, 52], [2, 107], [3, 59], [4, 63], [5, 87], [6, 25], [7, 36]]
>>> secret2 = 12
>>> shares2 = shamir.generateShares(n,t,secret2,p, Shamir_style = True)
>>> shares2
[[1, 58], [2, 31], [3, 82], [4, 60], [5, 77], [6, 56], [7, 70]]
>>> shares3 = shamir.mulShares(shares1, shares2, primefield = p)
>>> shares3
[[1, 78], [2, 40], [3, 92], [4, 51], [5, 32], [6, 44], [7, 34]]
>>> shamir.reconstructSecret(shares3, p)      # These are 2 4th egree polynomials (t = 5).
                                              # Multiplying these results in a 8th degree polynomial
                                              # We would need 9 points to uniquely identify such polynomial but we only have 7 points
                                              # So, the result is completely random
70

```
