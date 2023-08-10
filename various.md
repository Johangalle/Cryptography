# Various Python examples
## Convert between int, bytes and hex-string
```
>>> b = b"this is a byte string"
>>> i = int.from_bytes(b)
>>> i
170130276577738348141904353322542212591924105801319
>>> i_bytes = i.to_bytes((i.bit_length()+7)//8,"big")
>>> i_bytes
b'this is a byte string'
>>> hs1 = hex(i)
>>> hs1
'0x746869732069732061206279746520737472696e67'
>>> hs2 = b.hex()
>>> hs2
'746869732069732061206279746520737472696e67'  # Note it does not start with 0x
>>> i_fromh = int(hs1[2:],16)    # Note that we remove the 0x by starting at index 2
>>> i_fromh
170130276577738348141904353322542212591924105801319
>>> i_fromh = int(hs2,16)
>>> j = 0x746869732069732061206279746520737472696e67 # you can also just create an int using the hex representation
>>> b = bytes.fromhex(hs2)   # Make sure that the hex string contains an even number of hex symbols, otherwise, add a 0 in front of it.
>>>
>>> st = "This is a string"
>>> bst = st.encode()
>>> bst
b'This is a string'
>>> cst = bst.decode()   # from a character string to a byte string to a character string works like this
>>> cst
'This is a string'       
>>> cst == st
True
>>>
>>> i = 982345082347082347023946    # just a random number
>>> b = i.to_bytes((i.bit_length()+7)//8,"big")
>>> b
b'\xd0\x05\x08\x9b[\\\xbf\x19\x8eJ'
>>> b.hex()
'd005089b5b5cbf198e4a'
>>> list(b)
[208, 5, 8, 155, 91, 92, 191, 25, 142, 74]
>>> 0xd0, 0x05, 0x08, 0x9b, 0x5b, 0x5c, 0xbf, 0x19, 0x8e, 0x4a
(208, 5, 8, 155, 91, 92, 191, 25, 142, 74)
>>> cst = b.decode()     # from a random bytes string to a character string does not work most of the time
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xd0 in position 0: invalid continuation byte
```
## Converting binary to base64 and back
```
>>> import base64
>>> import secrets
>>> b = secrets.token_bytes(64)
>>> b
b'e\xf3\xdaP\x1fMh\x91ip(N3\x9eg\xa8G|\xca\xcb\xc8\x99\x81r\x9d/m+\xac\xd5\t\xaa\xa3\xef8\\~\x8d\x12\x16\xc7\x05F\x8d\x10l\xe6\xfaQc\xa3\x7f\xa6G"cy\xf2c\xae\xa3\xf2\x14\xff'
>>> b.hex()
'65f3da501f4d68916970284e339e67a8477ccacbc89981729d2f6d2bacd509aaa3ef385c7e8d1216c705468d106ce6fa5163a37fa647226379f263aea3f214ff'
>>> base64_b = base64.b64encode(b)
>>> base64_b
b'ZfPaUB9NaJFpcChOM55nqEd8ysvImYFynS9tK6zVCaqj7zhcfo0SFscFRo0QbOb6UWOjf6ZHImN58mOuo/IU/w=='
>>> b2 = base64.b64decode(base64_b)
>>> b2
b'e\xf3\xdaP\x1fMh\x91ip(N3\x9eg\xa8G|\xca\xcb\xc8\x99\x81r\x9d/m+\xac\xd5\t\xaa\xa3\xef8\\~\x8d\x12\x16\xc7\x05F\x8d\x10l\xe6\xfaQc\xa3\x7f\xa6G"cy\xf2c\xae\xa3\xf2\x14\xff'
>>> b2 == b
True
```
## Reading and writing binary files:
```
>>> with open('some_file_name.ext', 'rb') as file:
...     binary_data = file.read()  # The result is a bytes object that can be used as input to the other functions
>>> with open("new_file.ext", "wb") as file:
...     file.write(binary_data)
```
