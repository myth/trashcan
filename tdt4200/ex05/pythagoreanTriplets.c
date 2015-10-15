#define _GNU_SOURCE

#include <math.h> // for mathemetaical functions
#include <stdbool.h> // for bool
#include <stdio.h> // for stdin
#include <stdlib.h>
#include <unistd.h> // for ssize_t

#ifdef HAVE_MPI
#include <mpi.h>
#endif

#ifdef HAVE_OPENMP
#include <omp.h>
#endif

/*
 *  Function declarations
 */
int gcd(int a, int b);
bool is_coprime(int a, int b);


/*
 *  Main method
 */
int main(int argc, char **argv) {
	char *inputLine = NULL; size_t lineLength = 0;
	int *start, *stop, *numThreads, amountOfRuns = 0;

	// Read in first line of input
	getline(&inputLine, &lineLength, stdin);
	sscanf(inputLine, "%d", &amountOfRuns);

	stop = (int*) calloc(amountOfRuns, sizeof(int));
	start = (int*) calloc(amountOfRuns, sizeof(int));
	numThreads = (int*) calloc(amountOfRuns, sizeof(int));

	int tot_threads, current_start, current_stop;
	for (int i = 0; i < amountOfRuns; ++i) {

		// Read in each line of input that follows after first line
		free(inputLine); lineLength = 0; inputLine = NULL;
		getline(&inputLine, &lineLength, stdin);

		// If there exists at least two matches (2x %d)...
		if (sscanf(inputLine, "%d %d %d", &current_start, &current_stop, &tot_threads) >= 2) {
			if(current_start < 0 || current_stop < 0) {
				current_start = 0, current_stop = 0;
			}
            start[i] = current_start;
            stop[i] = current_stop;
			numThreads[i] = tot_threads;
		}
	}

	/*
	*	Remember to only print 1 (one) sum per start/stop.
	*	In other words, a total of <amountOfRuns> sums/printfs.
	*/


    /*
     *  Sequential solution
     */
    for (int i = 0; i < amountOfRuns; i++) {
        int sum = 0;

        // Do some bounds checks
        if (start[i] <= stop[i]) {
            printf("%d\n", sum);
            continue;
        }

        // For each run, we sum up the primitive triplets
        for (int c = start[i]; c < stop[i]; c++) {
            for (int b = 4; b < c; b++) {
                for (int a = 3; a < b; a++) {
                    if (pow(a, 2) + pow(b, 2) == pow(c, 2)) {
                        if (is_coprime(a, b) && is_coprime(b, c) && is_coprime(a, c)) {
                            sum++;
                        }
                    }
                }
            }
        }
        printf("%d\n", sum);
    }

	return 0;
}

/*
 *  Helper functions
 */

// Find the greatest common divisor between two numbers
int gcd(int a, int b) {
    while (b != 0) {
        int t = b;
        b = a % b;
        a = t;
    }
    return a;
}

// Find whether two integers are coprime
bool is_coprime(int a, int b) {
    return gcd(a, b) == 1;
}
