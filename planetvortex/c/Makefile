# The gravikernel — the C99 cross-language oracle
# (one command: `make -C c` builds and runs, the report lands on stdout)

CC ?= cc
CFLAGS ?= -O2 -std=c99 -Wall -Wextra
OUT := gravikernel

.PHONY: all run clean

all: $(OUT)

$(OUT): gravikernel.c
	$(CC) $(CFLAGS) -o $(OUT) gravikernel.c -lm

run: $(OUT)
	./$(OUT)

clean:
	rm -f $(OUT)
