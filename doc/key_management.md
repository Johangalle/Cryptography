# Key management
Code snippets to learn cryptography without the need to use other libraries. DO NOT USE IN PRODUCTION.

Key management is not yet part of my library and needs to be taken from another library.

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
