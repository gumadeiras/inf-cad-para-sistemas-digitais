## Compile

To compile use simple command, it's necessary have a GNU C compiler installed and some of standard c library:

```
$ make
```

## Execute

After compile step, it's generate two binaries:
* aigint
* aigpointer

To execute this file is necessary specify input file with the description of the
AIG. So, for example *aigint [input file]*:

```
$ aigint aig.txt
```

## File input format

First line must content the header, with the bellow information and format:

aig [Maximum variable index] [number of inputs] [number of latches NOT SUPPORTED] [number of outputs] [number of AND gates]

Followed by inputs, like:
[input number]
And outputs, like:
[input number]
And for the last, the AND gates:
[node] [input1] [input2]

**ODD numbers are interpreted as logic inverter gate**
