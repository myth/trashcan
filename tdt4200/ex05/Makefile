.PHONY: all clean

CC=gcc
MPCC=mpicc
CFLAGS=-Wall -O3 -lm

all: serial

serial: pythagoreanTriplets.c
	$(CC) $(CFLAGS) -o program pythagoreanTriplets.c

openmp: pythagoreanTriplets.c
	$(CC) $(CFLAGS) -DHAVE_OPENMP -o omp_program pythagoreanTriplets.c

mpi: pythagoreanTriplets.c
	$(MPCC) $(CFLAGS) -DHAVE_MPI -o mpi_program pythagoreanTriplets.c

hybrid: pythagoreanTriplets
	$(MPCC) $(CFLAGS) -fopenmp -DHAVE_OPENMP -DHAVE_MPI -o hybrid_program pythagoreanTriplets.c

clean:
	rm -rf pythagoreanTriplets.o program omp_program mpi_program hybrid_program

