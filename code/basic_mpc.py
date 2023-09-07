from cryptocourse import shamir
import random

def generateBeaverMultiple(n, m, primefield = shamir.field_size):
    a = random.randrange(2, primefield)
    b = random.randrange(2, primefield)
    c = a*b%primefield
    sharesa = shamir.generateShares(n, m, a, primefield, True)
    sharesb = shamir.generateShares(n, m, b, primefield, True)
    sharesc = shamir.generateShares(n, m, c, primefield, True)
    shares = []
    for i in range(len(sharesa)):
        shares.append([sharesa[i],sharesb[i], sharesc[i]])
    return shares

def checkBeaverMultiple(shares, t, primefield = shamir.field_size):
    sha = []
    shb = []
    shc = []
    for i in range(len(shares)):
        sha.append(shares[i][0])
        shb.append(shares[i][1])
        shc.append(shares[i][2])
    sha = random.sample(sha, t)
    shb = random.sample(shb, t)
    shc = random.sample(shc, t)
    a = shamir.reconstructSecret(sha,primefield)
    b = shamir.reconstructSecret(shb,primefield)
    c = shamir.reconstructSecret(shc,primefield)
    return a,b,c,c == a*b%primefield

def splitBeaver(beaver):
    sha = []
    shb = []
    shc = []
    for i in range(len(beaver)):
        sha.append(beaver[i][0])
        shb.append(beaver[i][1])
        shc.append(beaver[i][2])
    return sha, shb, shc

def multiplyShares (shares1, shares2, beaver, primefield = shamir.field_size):
    # SPDZ protocol
    shares3 = shamir.mulShares(shares1, shares2,primefield)
    sha, shb, shc = splitBeaver(beaver)
    alphashares = shamir.subtractShares(shares1,sha, primefield)
    betashares = shamir.subtractShares(shares2,shb, primefield)
    alpha = shamir.reconstructSecret(alphashares, primefield)
    beta = shamir.reconstructSecret(betashares, primefield)
    shares4 = shamir.linearCombinationOfShares ([shc, shb, sha],[1,alpha,beta],alpha*beta%primefield,primefield)
    return shares4

if __name__ == '__main__':
    s = generateBeaverMultiple(5,2,17)
    res = checkBeaverMultiple(s,2,17)
    assert res[3]
    s = generateBeaverMultiple(5,2)
    res = checkBeaverMultiple(s,2)
    assert res[3]
    s = generateBeaverMultiple(7,3)
    res = checkBeaverMultiple(s,3)
    assert res[3]
    
    t, n = 3,5
    secret1 = random.randrange(2,17)
    secret2 = random.randrange(2,17)
    secret3 = secret1*secret2%17
    beaver = generateBeaverMultiple(n,t,17)
    shares1 = shamir.generateShares(n,t,secret1,17,Shamir_style = True)
    shares2 = shamir.generateShares(n,t,secret2,17,Shamir_style = True)
    shares3 = multiplyShares(shares1, shares2, beaver,17)
    assert shamir.reconstructSecret(shares3, 17) == secret3
    
    t, n = 3,7
    secret1 = random.randrange(2,17)
    secret2 = random.randrange(2,17)
    secret3 = secret1*secret2%17
    beaver = generateBeaverMultiple(n,t,17)
    shares1 = shamir.generateShares(n,t,secret1,17,Shamir_style = True)
    shares2 = shamir.generateShares(n,t,secret2,17,Shamir_style = True)
    shares3 = multiplyShares(shares1, shares2, beaver,17)
    assert shamir.reconstructSecret(shares3, 17) == secret3

    t, n = 3,5
    secret1 = random.randrange(2,shamir.field_size)
    secret2 = random.randrange(2,shamir.field_size)
    secret3 = secret1*secret2%shamir.field_size
    beaver = generateBeaverMultiple(n,t)
    shares1 = shamir.generateShares(n,t,secret1,Shamir_style = True)
    shares2 = shamir.generateShares(n,t,secret2,Shamir_style = True)
    shares3 = multiplyShares(shares1, shares2, beaver)
    assert shamir.reconstructSecret(shares3) == secret3

    t, n = 3,7
    secret1 = random.randrange(2,shamir.field_size)
    secret2 = random.randrange(2,shamir.field_size)
    secret3 = secret1*secret2%shamir.field_size
    beaver = generateBeaverMultiple(n,t)
    shares1 = shamir.generateShares(n,t,secret1,Shamir_style = True)
    shares2 = shamir.generateShares(n,t,secret2,Shamir_style = True)
    shares3 = multiplyShares(shares1, shares2, beaver)
    assert shamir.reconstructSecret(shares3) == secret3

    t, n = 7,23
    secret1 = random.randrange(2,shamir.field_size)
    secret2 = random.randrange(2,shamir.field_size)
    secret3 = secret1*secret2%shamir.field_size
    beaver = generateBeaverMultiple(n,t)
    shares1 = shamir.generateShares(n,t,secret1,Shamir_style = True)
    shares2 = shamir.generateShares(n,t,secret2,Shamir_style = True)
    shares3 = multiplyShares(shares1, shares2, beaver)
    assert shamir.reconstructSecret(shares3) == secret3
