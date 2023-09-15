# Key management
Code snippets to learn cryptography without the need to use other libraries. DO NOT USE IN PRODUCTION.

Key management is not yet part of my library and needs to be taken from another library.

## Create the public / private key pair, csr and self-signed certificate
```
$ openssl genrsa -out ./mytestserver.key 2048                 
Generating RSA private key, 2048 bit long modulus
................+++++
......................+++++
e is 65537 (0x10001)
$ openssl req -new -sha256 -key mytestserver.key -out mytestserver.csr
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) []:be
State or Province Name (full name) []:
Locality Name (eg, city) []:
Organization Name (eg, company) []:howest
Organizational Unit Name (eg, section) []:
Common Name (eg, fully qualified host name) []:howest
Email Address []:

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
$ cat mytestserver.key                                                
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA5naF7zSixD6a+18XSdDrpUCuc4oWf0dOL7oBhhZ6fYNsg7Ms
wjdEFLl9Zi7eQeBCg4iYdRpN2/bvxthywadnIHpKucRNQOqdKqJmX/4+dtcGrMW7
h7j8v2NMvmL2qTpEQoM2YOfe+mlI84VBLCFit/aDOtWoGFdBHLqyEvAXI8XiHm7E
gKdlPjJwNFHANisi1NsyO+j2NKacgkQZ/JT3efWjeRUHJLz2TqzBw7qxN5BTjjan
+bU4ok+WqWQgwNc5e41nzajzUzILy8pKO2Z2/I5qvE9yzZBLXMYMqsNaEQ8U8IdD
NxkPiv7zgAcIXgvKg3GJslKr5GoEiAkKAxlK4QIDAQABAoIBAH61K24YwmSjBxKt
dWBgPS7eIQvlH/laeuJCohPWyAG6AC9ok3M0b3n1gbxsiEYvxmIK98dqbuRBIBNz
baSLJWf11J/ODatjUoXeQ+sDHdS45DKZhEFas5uGPOtv/a2NG3p2Ka+dzDphKHq7
CNn6gQwjvILcdU7sqh/hhYZj+lTvq/BFZYujJ8Js8LS+55ErHhwv80qVOdBfihnO
+Os6kjSmiPslyGn8GcDr+x3wt8zCR7MNPVCI6zRJ7vqObk0HnQpitPQn/6DfsuNu
NuEiDxt/CWZoM5QvlblXrzpZKlTEnzzwU8QtRJu+delA8Fjm5BbHzOFJ5L5JM5nS
kNa5fwECgYEA+dKufPthLX2q5QuKmZmOt6YufFMpsDaxfPxBIATd3sU17RXSoQ+d
FqFzU0QyTjQyRq6R9wmb1njl/n9FmRHekBJSan4RTSkNfpFvOq0qg8Wdc7iO0CYR
0fdLSEHqMs6TItuRZAT3aqdIu37dFe4x/Ct3BNTOJE0hHdHST0z+I7MCgYEA7ClM
LJJmIwXz2vLIxLxOyFhoZQKa3ZjVGwYPkz69BqMRHy+LlM4ofJJbG6vIWJKkYm8u
lBRucaRCsZihpmiQPCdMuk56Lg8XrfHSdjXYBsjNPFGcEv4X3gzxnLjRKaleeZLN
vSyq5zZyV41HUjJM3kZjTY3IPPX9+Y+FFy2e3RsCgYAOInl04NQyurV8mBaTcji8
804WAq6NJcsNA0i8Awp6nDXc4Cs2qad9rEzWHTmraxCdJytjCswialy49YJ+kqBB
DohTNibMctIsoxXkAAAzzG6IKZ0K8dx4QMGlqPUTQtTYWAv12MIW6rgWw6rGnt99
IQhu4Yt4SlThVwnLKtQGOQKBgQCS9fQYPJZgryCcHL+BZimklReJ3EAhLC1ZXsEs
gTtCORG7lWvIEy6wrqcRpinLrJ2tP8D9l2VPRMfYGsJleuZe+JnPymxP40Z6EWVF
+KXROv40zhhQ3Vxe6zEjtQM8aNCI2Sk80uIbdg9bmmhKp1CcdbLwHQ4BmZcNyRkq
XlJhBwKBgBX46Q1v3IUzu/8BYhC+m8AJunNu6SwLd9r0z7ToYgZw+NBvznYF3oij
IVTH6PGGczByrKSbrgFmqLRPGK0SEKpqtgG30+JiHw2VWcS9g3aIaCwITxAGQWfw
RT0FKxUJARToBBdb/BTAGg6d34yAfJNnkRJrY/cnKu/WZPsorCYp
-----END RSA PRIVATE KEY-----
$ cat mytestserver.csr                                                
-----BEGIN CERTIFICATE REQUEST-----
MIICdDCCAVwCAQAwLzELMAkGA1UEBhMCYmUxDzANBgNVBAoMBmhvd2VzdDEPMA0G
A1UEAwwGaG93ZXN0MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA5naF
7zSixD6a+18XSdDrpUCuc4oWf0dOL7oBhhZ6fYNsg7MswjdEFLl9Zi7eQeBCg4iY
dRpN2/bvxthywadnIHpKucRNQOqdKqJmX/4+dtcGrMW7h7j8v2NMvmL2qTpEQoM2
YOfe+mlI84VBLCFit/aDOtWoGFdBHLqyEvAXI8XiHm7EgKdlPjJwNFHANisi1Nsy
O+j2NKacgkQZ/JT3efWjeRUHJLz2TqzBw7qxN5BTjjan+bU4ok+WqWQgwNc5e41n
zajzUzILy8pKO2Z2/I5qvE9yzZBLXMYMqsNaEQ8U8IdDNxkPiv7zgAcIXgvKg3GJ
slKr5GoEiAkKAxlK4QIDAQABoAAwDQYJKoZIhvcNAQELBQADggEBAF8glvWTZXaf
kDmxkJE2UZbkNj46aVo/nn7n3GAYRD1fF6Sw7Abb7/tL58GvwRFh9I1JFm9IBQP7
68GpjBbOzn+zRumrrZ0nz+yOEu0wpkO1ELMvqTbe9/khljb6n9uutX+lFFLBw5QF
AN/8Q1meYT0vHhkONKaJjA0Lc4sO5UZILD5dcxC2mx9MtaOBlDnmFL72ckW4PuNd
Sr2Fj0oegRcLGb3mpeL59fo5tZaKdiDMVFxvHEIG9ZprabG7Pf/fPu+Yv4H4c7JH
UM5DvUvr+GD3ehIg9vFR6CoFoGo6TTghdtnjEmufFrAil0hg521z91DvYplT4o8M
Hta6bAfJcB0=
-----END CERTIFICATE REQUEST-----
$ openssl x509 -req -days 365 -in mytestserver.csr -signkey mytestserver.key -out mytestservercert.pem
Signature ok
subject=/C=be/O=howest/CN=howest
Getting Private key
$ cat mytestservercert.pem 
-----BEGIN CERTIFICATE-----
MIIC2jCCAcICCQCjymQywEYpijANBgkqhkiG9w0BAQsFADAvMQswCQYDVQQGEwJi
ZTEPMA0GA1UECgwGaG93ZXN0MQ8wDQYDVQQDDAZob3dlc3QwHhcNMjMwOTE1MTYw
MzE3WhcNMjQwOTE0MTYwMzE3WjAvMQswCQYDVQQGEwJiZTEPMA0GA1UECgwGaG93
ZXN0MQ8wDQYDVQQDDAZob3dlc3QwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEK
AoIBAQDmdoXvNKLEPpr7XxdJ0OulQK5zihZ/R04vugGGFnp9g2yDsyzCN0QUuX1m
Lt5B4EKDiJh1Gk3b9u/G2HLBp2cgekq5xE1A6p0qomZf/j521wasxbuHuPy/Y0y+
YvapOkRCgzZg5976aUjzhUEsIWK39oM61agYV0EcurIS8BcjxeIebsSAp2U+MnA0
UcA2KyLU2zI76PY0ppyCRBn8lPd59aN5FQckvPZOrMHDurE3kFOONqf5tTiiT5ap
ZCDA1zl7jWfNqPNTMgvLyko7Znb8jmq8T3LNkEtcxgyqw1oRDxTwh0M3GQ+K/vOA
BwheC8qDcYmyUqvkagSICQoDGUrhAgMBAAEwDQYJKoZIhvcNAQELBQADggEBAEq6
WruLfCNH1Gw++4BD9L7N55JBHk/yeYB83utFER8TKM4mUYpdt7RR7dXgbcC837sP
fj0UE368upxw/H454kgR8az386u3X/62+l03R9yn88uajq3FclxTEGqfrJtnL5dG
dfon5gdCyk3VseF5QxN4zQy+l96RBM+dS6lu7ekhZZCPWg1/ZDdNSswEyY+mBhwp
kifmpJ4M+YNla1Zw92nkIeClPABNiGx5ZOtYzhN4shbCM6TGRrIsVx1xA/dfVF0q
KAVnbfIKb/2YBlY53UZkbzvmJ2W660uCIZ2+LNez9T3hVEsP5/wiPnOChxdlg6gQ
OZDtqwKfhM+9fvvKfqs=
-----END CERTIFICATE-----
johangalle@Johans-MacBook-Air ~ % 
```
## Create the public / private key pair
Install the pycryptodome library for this purpose. You may need to install pip (or pip3) first, or upgrade pip. 

We create an RSA key pair and store the public key in the file "receiver.pem" and the private key in "private.pem".
```
$ pip3 install pycryptodome
$ python3
>>> from Crypto.PublicKey import RSA
>>> key = RSA.generate(2048)
>>> private_key = key.export_key()
>>> file_out = open("private.pem", "wb")
>>> file_out.write(private_key)
>>> file_out.close()
>>> public_key = key.publickey().export_key()
>>> file_out2 = open("receiver.pem", "wb")
>>> file_out2.write(public_key)
>>> file_out2.close()
>>> private_key
b'-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEAx89zN9qfzeR4geyljutm9ARV06pceZQx/lq8PisXbF7mRvSc\ni6Gwrrpyr1z+5fxUFcwiDODL74eFenI65PSFdDMUEuZebvPkU4Cj1Mo9obi7oUz5\nqZZims38j0o71OILU8JqYASSOyN2QdKckrvf1d9PPO91BocTW6svFDDbyFeuyjgs\nf2P1o32NaXhLjB4rHjmLA96tkiwvgsMBJz5CU5rQb/UWXZtc7voV0EBNxvN2Oqfj\nyt3nqiGWcXYa+GOyz4A+JLQLwEr9FD+6JtgXlHG25W6QdovOfLzv+22mzBfayV7S\nnug+PSZSgfEFLBakapofzbtb0Z+H0hHVxJ54hwIDAQABAoIBAAzMrwUBJHZSnQTQ\n1wFi9p/9D+gH1495cDZqzSvVim7Ij+UA66JNako9hI+gdaFGWuos8gvaWDxw283h\nnjPNrvR005b39Bnhb8GI0dxIurTIZuSVtllbWj4WbrsmUAZ6fUVEhMuMn2pAaRi2\nvo1VXnWOrfHDJfKUGcGOiezq/R+sbERrZcZVMmyKjttsYUK+Fc0M83ySW7lwYxiY\nUu6XY1tuGdMk5T2OGIjX364kaNZG/0ZPAdIIeI8778rTCc1aBK+zGCauRxR81SGC\nPNGvoMKuMvKD70wRk8nyZi8eJ7rmbu4sHCsh4zgOD64KawcHXMgGYrKcp+Uewe6q\nbpXRqPkCgYEAyGqwKh1icBdk0SMl1/q/Gl8uncCiot1nAPtfUbTSxDMJCsFbVxlA\n7ZlZe5r8Wl67v1qh1RSMqDDwDE8jCJiQPwlm1+V73CqP1nV0B2KO7e6BBTNlAFk4\n0qDxFZK/e+4sjmhEw9AqUAlrRr+EEJFfmErmqX5EzrZudA+big75GrsCgYEA/zm1\nXY/pjCxciA3H0VholN3BH0tLDILiDY2Cqrhd+6TwI6KOW3drqXaBp4M6InDNI5fk\nrqHJU8j40NW+7c/teb4We0YbuTcrwK4ULoiMYe/cX9fWyp37+eZSaZ2so9tot5RF\nwjdK0XXWspQKFK0bVP5yAzUfimA3V7NRNJuX2qUCgYEApupkKc8rStvQ9XVmcUi+\nnIIlWvEzAp2OyfyRWIVW/Fzc7P44yoOX1crgAdgE0GcRyr77BXIF65ZGdpn6PZCC\nol18L9dKnwU7ootTxUrKa1M2VVSGjBHDB3lPEH6Vx+uHZFtm2ganFt2hYNzkasAI\nc9f936/wMpEx0KunCQaLZT0CgYAzSfOKc8spIhkONka7aRrLH60ZjtXsE7k9o/xo\nNlico06mupoFA4CdM3VmplZeaXCwAGwyM8zzi2WFAg82VxyP5IU8DKCxncarF9By\ncXpUjBErKYK+gPUMCR7ynn79BrCKg79pAheE9DtK87j64ralY+ShhGFsO12jwCNH\ngSUJCQKBgHJIDA24j3bnnZ2W0iG98l73reu4pwkrxffplr9Pv/F5DFqgZhdx2Icn\nku2w/MhZQBxbaMBjIKUD2BofDjo+/VTZnKMiVwUdwFFX8ho1mkMLOiHdtH6vHDBr\ncbZw8v+CzVE4v+moUPyMBCZPJ9JvDw13XtGeW1nZJOrCrPTOpHV2\n-----END RSA PRIVATE KEY-----'
>>> public_key
b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAx89zN9qfzeR4geyljutm\n9ARV06pceZQx/lq8PisXbF7mRvSci6Gwrrpyr1z+5fxUFcwiDODL74eFenI65PSF\ndDMUEuZebvPkU4Cj1Mo9obi7oUz5qZZims38j0o71OILU8JqYASSOyN2QdKckrvf\n1d9PPO91BocTW6svFDDbyFeuyjgsf2P1o32NaXhLjB4rHjmLA96tkiwvgsMBJz5C\nU5rQb/UWXZtc7voV0EBNxvN2Oqfjyt3nqiGWcXYa+GOyz4A+JLQLwEr9FD+6JtgX\nlHG25W6QdovOfLzv+22mzBfayV7Snug+PSZSgfEFLBakapofzbtb0Z+H0hHVxJ54\nhwIDAQAB\n-----END PUBLIC KEY-----'
```
## The sender encrypts
The sender encrypts the secret message using AES and a random 128 bits AES symmetric key. The sender also encrypts this random symmetric key using public key cryptography and using the public key "receiver.pem".
```
>>> data = "I met aliens in UFO. Here is the map.".encode("utf-8")
>>> recipient_key = RSA.import_key(open("receiver.pem").read())
>>> import secrets
>>> symmetric_key128 = secrets.token_bytes(16)
>>> len(symmetric_key128)
16
>>> from Crypto.Cipher import AES, PKCS1_OAEP
>>> cipher_rsa = PKCS1_OAEP.new(recipient_key)
>>> enc_symmetric_key128 = cipher_rsa.encrypt(symmetric_key128)
>>> cipher_aes = AES.new(symmetric_key128, AES.MODE_EAX)
>>> ciphertext, tag = cipher_aes.encrypt_and_digest(data)
>>> file_out = open("encrypted_data.bin", "wb")
>>> [ file_out.write(x) for x in (enc_symmetric_key128, cipher_aes.nonce, tag, ciphertext) ]
>>> file_out.close()
```
## The receiver decrypts
The receiver decrypts the ciphertext. This inludes taking the encrypted symmetric key, decrypting it using his private key "private.pem", then using this decrypted symmetric key to decrypt the actual ciphertext.
```
>>> from Crypto.PublicKey import RSA
>>> from Crypto.Cipher import AES, PKCS1_OAEP
>>> file_in = open("encrypted_data.bin", "rb")
>>> private_key = RSA.import_key(open("private.pem").read())
>>> enc_symmetric_key, nonce, tag, ciphertext = [ file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]
>>> file_in.close()
>>> cipher_rsa = PKCS1_OAEP.new(private_key)
>>> symmetric_key = cipher_rsa.decrypt(enc_symmetric_key)
>>> len(symmetric_key)
16
>>> cipher_aes = AES.new(symmetric_key, AES.MODE_EAX, nonce)
>>> data = cipher_aes.decrypt_and_verify(ciphertext, tag)
>>> data
b'I met aliens in UFO. Here is the map.'
>>> data.decode("utf-8")
'I met aliens in UFO. Here is the map.'
```
