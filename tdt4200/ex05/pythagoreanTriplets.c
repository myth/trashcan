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
void calc_local_range(int *loc_start, int *loc_stop, int start, int stop, int rank, int num_processors);

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

	int tot_threads = 1, current_start, current_stop;
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

    int task_start = 0;
    int task_stop = amountOfRuns;
    for (int i = task_start; i < task_stop; i++) {
        int sum = 0;
        int begin, end, t;
        
        begin = start[i];
        end = stop[i];
        t = numThreads[i];

        // Do some bounds checks.
        if (end <= begin) {
            printf("%d\n", sum);
            continue;
        }

        #ifdef HAVE_OPENMP
        #pragma omp parallel num_threads(t) reduction(+:sum)
        {
            int loop_end = ceil(sqrt(end));
            int thread_sum = 0;
            int m;
            #pragma omp for private(m)
            for (m = 2; m < loop_end; m++) {
                int n;
                if (m % 2 == 0) { n = 1; }
                else { n = 2; }
                for (; n < m; n += 2) {
                    if ((m*m+n*n < end) && (m*m+n*n >= begin) && is_coprime(m, n)) {
                        thread_sum++;
                    }
                }
            }
            sum = thread_sum;
        }
        #else
        for (int m = 2; m*m < end; m++) {
            int n;
            if (m % 2 == 0) { n = 1; }
            else { n = 2; }
            for (; n < m; n += 2) {
                if ((m*m+n*n < end) && (m*m+n*n >= begin) && is_coprime(m, n)) {
                    sum++;
                }
            }
        }
        #endif

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

/*
 * Determine the local start and stop counters for
 * a specific processor rank.
 */
void calc_local_range(int *loc_start, int *loc_stop, int start,
                       int stop, int rank, int num_processors) {
    int num_runs = stop - start;
    int count = num_runs / num_processors;
    int remainder = num_runs % num_processors;

    if (rank < remainder) {
        *loc_start = rank * (count + 1);
        *loc_stop = *loc_start + count;
    }
    else {
        *loc_start = rank * (count + remainder);
        *loc_stop = *loc_start + count - 1;
    }
}

