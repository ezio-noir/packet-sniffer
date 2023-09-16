Python Cheat Sheets - Modules
=============================

by Victor Payno
---------------

### struct ###

#### Format String ####

##### Optional 1st char #####

```
@ : native order, size & alignment (default)
= : native order, standard size & alignment
< : little-edian, standard size & alignment
> : big-edian, standard size & alignment
! : same as >
```

##### Remaining chars. #####

```
[optional preceding decimal indicates repetition]

x : pad byte -> no value
c : char -> string (len == 1)
b : signed char -> integer
B : unsigned char -> integer
? : _Bool -> bool (if C99 available, otherwise char)
h : short -> integer
H : unsigned short -> integer
i : int -> integer
I : unsigned int -> integer or long
l : long -> integer
L : unsigned long -> long
f : float -> float
d : double -> float

[preceding decimal indicates lenght]

s : char[] (C string) -> string
p : pascal array -> string (short variable-length string stored in a fixed number of bytes, first byte is the lenght of the string)

[Only available in native format.]

P : int/long type that holds a pointer (void *) -> long


[Not in native mode unless 'long long' in platform C.]

g : long long -> long
Q : unsigned long long -> long

```

#### Exceptions ####

```
struct.error
```

#### Functions ####

```
calcsize(format_string) - returns size of C struct

pack(format_string, v1, v2, ...) - returns string represented struct

pack_into(format_string, buffer, offset, v1, v2, ...) - same as pack but writes to buffer and accepts an offset

unpack(format_string, struct_string) - returns tuple representation of the struct, len(struct_string) == calcsize(format_string)

unpack_from(format_string, buffer[, offset=0]) - unpack buffer from offset
```

#### Examples ####

```
import struct

format_string = '2hl?Q10s'

raw_data = [1, 2, 3, True, 1234567890, "abcdefghi"]

packed_data = struct.pack(format_string, *raw_data)
# Out[163]: '\x01\x00\x02\x00\x03\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\xd2\x02\x96I\x00\x00\x00\x00abcdefghi\x00'

unpacked_data = struct.unpack(format_string, packed_data)

print "Raw Data:", raw_data
# Raw Data: [1, 2, 3, True, 1234567890, 'abcdefghi']

print "Packed Data:", packed_data
# Packed Data: ☺ ☻ ♥   ☺       ╥☻ûI    abcdefghi

print "Unpacked Data (tuple):", unpacked_data
# Unpacked Data: (1, 2, 3, True, 1234567890, 'abcdefghi\x00')

print "Unpacked Data (list):", list(unpacked_data)
# Unpacked Data: [1, 2, 3, True, 1234567890, 'abcdefghi\x00']

format_string = '>' + format_string
packed_data = struct.pack(format_string, *raw_data)
# Out[167]: '\x00\x01\x00\x02\x00\x00\x00\x03\x01\x00\x00\x00\x00I\x96\x02\xd2abcd
efghi\x00'

print "Packed Data:", packed_data
#  Packed Data:  ☺ ☻   ♥☺    Iû☻╥abcdefghi
```

