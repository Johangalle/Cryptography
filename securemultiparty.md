# Secure Multiparty Computation
Code snippets to learn cryptography without the need to use other libraries. DO NOT USE IN PRODUCTION.

Secure multiparty computation allows multiple parties to start a protocol to perform a computation. 

The input of the computation are secrets shared among multiple parties. 

The output of the computation is again a secret shared among multiple parties. 

During the computation, none of the parties is able to deduce any other information than the final result.

We have shares1, a set of 3 shares [1,2], [2,5], [3,10] in a (3,3) secret sharing scheme. We have shares2, a set of 3 shares [1,6], [2,7], [3,8] in a (3,3) secret sharing scheme
Calculate a set of shares (resultShares) representing the product of the two secrets, by using the SPDZ protocol (based on beavers).

The formula behind this protocol works as follows. We want to multiply the secrets [x] and [y]. 

We have the beaver triple [a], [b], [c] and we know that c = a * b (this is the meaning of a beaver triple). The beaver values are secret-shared.

We calculate alpha = [x] – [a]; beta = [y] - [b]. We reconstruct the secrets alpha and beta, but this does not reveal any information about [x] and [y].
We then compute the linear function [z] = [c] + alpha*[b] + beta*[a] + alpha*beta. This results in [z] = [x] * [y].

## Perform the multiparty multiplication
```
>>> from cryptocourse import shamir, basic_mpc
>>> shares1 = [[1,2],[2,5],[3,10]]
>>> shares2 = [[1,6],[2,7],[3,8]]
>>> shamir.reconstructSecret(shares1)
1
>>> shamir.reconstructSecret(shares2)
5
>>> n,m = 3,3
>>> beaver = basic_mpc.generateBeaverMultiple(n,m)
>>> beaver
[[[1, 1350638100], [1, 193696820], [1, 2040608607]], [[2, 1342462740], [2, 300719459], [2, 1561463716]], [[3, 1588540574], [3, 612325379], [3, 570959117]]]
>>> sha, shb, shc = basic_mpc.splitBeaver(beaver)
>>> sha, shb, shc
([[1, 1350638100], [2, 1342462740], [3, 1588540574]], [[1, 193696820], [2, 300719459], [3, 612325379]], [[1, 2040608607], [2, 1561463716], [3, 570959117]])
>>> alphashares = shamir.subtractShares(shares1, sha)
>>> betashares = shamir.subtractShares(shares2, shb)
>>> 
>>> alpha = shamir.reconstructSecret(alphashares)
>>> beta = shamir.reconstructSecret(betashares)
>>> alpha, beta
(534416994, 1856226190)
>>> resultshares = shamir.linearCombinationOfShares([shc,shb,sha],[1,alpha,beta],alpha*beta)
>>> shamir.reconstructSecret(resultshares)
5
```
## Perform the multiparty multiplication using a given prime number for the modulo calculations
```
>>> from cryptocourse import shamir, basic_mpc
>>> n, m = 5,3
>>> shares1 = shamir.generateShares(n,m,25, 2969, True)
>>> shares1
[[1, 1708], [2, 2109], [3, 1228], [4, 2034], [5, 1558]]
>>> shares2 = shamir.generateShares(n,m,30, 2969, True)
>>> beaver = basic_mpc.generateBeaverMultiple(n,m,2969)
>>> sha, shb, shc = basic_mpc.splitBeaver(beaver)
>>> sha, shb, shc
([[1, 424], [2, 2789], [3, 112], [4, 1300], [5, 415]], [[1, 1061], [2, 1393], [3, 106], [4, 169], [5, 1582]], [[1, 865], [2, 2098], [3, 1483], [4, 1989], [5, 647]])
>>> alphashares = shamir.subtractShares(shares1, sha)
>>> betashares = shamir.subtractShares(shares2, shb)
>>> alphashares = shamir.subtractShares(shares1, sha, 2969)
>>> betashares = shamir.subtractShares(shares2, shb, 2969)
>>> alpha = shamir.reconstructSecret(alphashares,2969)
>>> beta = shamir.reconstructSecret(betashares,2969)
>>> alpha, beta
(1070, 920)
>>> resultshares = shamir.linearCombinationOfShares([shc,shb,sha],[1, alpha, beta],alpha*beta, 2969)
>>> shamir.reconstructSecret(resultshares, 2969)
750
>>> 25*30
750
```
