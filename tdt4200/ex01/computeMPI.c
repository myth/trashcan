#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <mpi.h>
#include <math.h>

/*
	A simple MPI example.
	
	1. Fill in the needed MPI code to make this run on any number of nodes.
	2. The answer must match the original serial version.
	3. Think of corner cases (valid but tricky values).

	Example input:
	./simple 2 10000

*/

// Define the master processor as rank 0
#define MASTER 0

bool DEBUG = false;

/*
 * Perform a summation of 1 / log(i) from start to stop
 */
double log_sum(int start, int stop) {
	// Perform the computation
	double sum = 0.0;
	for (int i = start; i < stop ; i++) {
		sum += 1.0 / log(i);
	}

    return sum;
}

/*
 * Determine the local start and stop counters for
 * a specific processor rank.
 */
void calc_local_range(int *loc_start, int *loc_stop, int start,
                       int stop, int rank, int num_processors) {

    // Compute the local range, so that all the elements are accounted for. 
    int remainder = (stop - start) % num_processors;
    int interval = (int) floor((stop - start) / num_processors);

    // Figure out where this processor should start and stop
    *loc_start = start;
    *loc_start = *loc_start + rank * interval;
    *loc_stop = *loc_start + interval;

    // For now, just let the processor with the shortest straw
    if (remainder != 0 && rank == num_processors - 1) {
        *loc_stop = stop;
    }
}

int main(int argc, char **argv) {
    double node_sum, sum;                       // We're storing the total sum here
    double start_time = 0.0;                    // Timestamp for start of invocation
    int NUM_PROCESSORS, RANK;                   // MPI Num of processors and proc. no of current processor

    // Check that correct amount of args are provided
	if (argc < 3) {
		printf("This program requires two parameters:\n \
the start and end specifying a range of positive integers in which \
start is 2 or greater, and end is greater than start.\n");
		exit(1);
	}

    // Fetch start and stop values from command line argument vector
	int start = atoi(argv[1]);
	int stop = atoi(argv[2]);
    int my_start, my_stop;
    
    // Perform some simple input valdation
	if (start < 2 || stop <= start) {
		printf("Start must be greater than 2 and the end must be larger than start.\n");
		exit(1);
	}

    // Set up MPI
    int mpi_init_status = MPI_Init(&argc, &argv);
    if (mpi_init_status != MPI_SUCCESS) {
        printf("Error starting MPI program. Terminating.\n");
        MPI_Abort(MPI_COMM_WORLD, mpi_init_status);
    }
    MPI_Comm_size(MPI_COMM_WORLD, &NUM_PROCESSORS);
    MPI_Comm_rank(MPI_COMM_WORLD, &RANK);
    
    // Set the start time
    if (RANK == MASTER) {
        start_time = MPI_Wtime();
    }

    // Determine local range bounds
    calc_local_range(&my_start, &my_stop, start, stop, RANK, NUM_PROCESSORS);
    
	// Debug prints if needed
    if (DEBUG) {
        printf("Process %d (Start: %d Stop: %d Work: %d)\n", RANK, my_start, my_stop, (my_stop - my_start));
    }

    // Perform calculations for all partials
    sum = log_sum(my_start, my_stop);
    
    // Communication between processors
    if (RANK == MASTER) {
        for (int i = 1; i < NUM_PROCESSORS; i++) {
            // Store result in node_sum and add to already calculated sum for master node
            MPI_Recv(&node_sum, 1, MPI_DOUBLE, i, 1337, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            sum += node_sum;
        }
        printf("The sum is: %f\n", sum);
        //printf("Calculations took: %f seconds.\n", MPI_Wtime() - start_time);
    }
    else {
        MPI_Send(&sum, 1, MPI_DOUBLE, MASTER, 1337, MPI_COMM_WORLD);
    }

    MPI_Finalize();
    return 0;
}

