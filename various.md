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
>>> i_fromh = int(hs1[2:],16)
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
>>> cst = b.decode()     # from a random bytes string to a character string does not work most of the time
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xd0 in position 0: invalid continuation byte
```
## Reading and writing binary files:
```
>>> with open('some_file_name.ext', 'rb') as file:
...     binary_data = file.read()  # The result is a bytes object that can be used as input to the other functions
>>> with open("new_file.ext", "wb") as file:
...     file.write(binary_data)
```
