#define _GNU_SOURCE

#include <math.h> // for mathemetaical functions
#include <stdbool.h> // for bool
#include <stdio.h> // for stdin
#include <stdlib.h>
#include <unistd.h> // for ssize_t

#define MIN(a,b) (((a)<(b))?(a):(b))
#define MAX(a,b) (((a)>(b))?(a):(b))

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
        
        //#pragma omp parallel for
        for (int m = 2; m*m < stop[i]; m++) {
            int n;
            if (m % 2 == 0) { n = 1; }
            else { n = 2; }
            for (; n < m; n += 2) {
                if ((m*m+n*n <= stop[i]) && (m*m+n*n >= start[i]) && is_coprime(m, n)) {
                    sum++;
                    // printf("M: %d, N: %d,   a:%d, b:%d, c:%d\n", m, n, m*m - n*n, 2*m*n, m*m + n*n);
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

