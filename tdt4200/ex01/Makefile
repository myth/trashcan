.PHONY: clean all

DIR:=bin

ifndef START
START:=2
endif
ifndef STOP
STOP:=10000000
endif
ifndef PROCESSES
PROCESSES:=4
endif

all: serial parallel
	@echo "[i] Build complete."

parallel: dir computeMPI.c
	mpicc -g -Wall -lm -std=c99 -O2 -o $(DIR)/$@ computeMPI.c

serial: dir computeSerial.c
	gcc -Wall -o $(DIR)/$@ computeSerial.c -std=c99 -lm -O2

run_serial: serial
	bin/serial $(START) $(STOP)

run_parallel: parallel
	mpirun -np $(PROCESSES) bin/parallel $(START) $(STOP)

dir:
	test -d $(DIR) || mkdir $(DIR)

clean:
	rm -f bin/serial bin/parallel
	@echo "[i] Binaries removed."

