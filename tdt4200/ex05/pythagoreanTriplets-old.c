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
int gcd(unsigned int u, unsigned int v);
bool is_coprime(unsigned int u, unsigned int v);

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
        if (stop[i] <= start[i]) {
            printf("%d\n", sum);
            continue;
        }
        
        // C is always on the form 4*n+1 with min of 5
        unsigned int c = 5;
        if (start[i] > 5) {
            c = start[i];
            while ((c - 1) % 4 != 0) c++;
        }

        // Outer loop incremented by 4, since we already know the form of C
        for (; c < stop[i]; c += 4) {
            for (unsigned int b = 4; b < c; b++) {   
                // If the pairs are not coprime, continue
                if (!is_coprime(b, c)) {
                    continue;
                }

                unsigned int a = 3;
                // If b is odd, then a must be even
                if (b % 2 == 1) {
                    a = 4;
                }
                
                for (; a < b; a += 2) {
                    if (pow(a, 2) + pow(b, 2) == pow(c, 2)) {
                        sum++;
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
int gcd(unsigned int u, unsigned int v) {
    while (v != 0) {
        unsigned int t = v;
        v = u % v;
        u = t;
    }
    return u;
}

// Find whether two integers are coprime
bool is_coprime(unsigned int u, unsigned int v) {
    return gcd(u, v) == 1;
}

