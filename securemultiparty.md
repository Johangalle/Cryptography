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

We calculate alpha = [x] – [a]; beta = [y] - [b]. We reconstruct the secrets alp[ha and beta, but this does not reveal any information about [x] and [y].
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
