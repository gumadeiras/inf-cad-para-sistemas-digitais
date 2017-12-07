CC=gcc
.PHONY: all clean aigint

all: aigint aigpointer

aigint: aigint.c aigparser.o
	$(CC) -o $@ $^

aigpointer: aigpointer.c aigparser.o
	$(CC) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

clean:
	rm *.o aigint aigpointer
