#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Print the string in reverse, and swap lower case and capital letters.
// But only 10 chars max.
void reverse(char *string)
{
	// Make buffer
	unsigned char *mem = malloc(10);
	int i, lastChar;

    printf("[i] Analyzing content of mem before strcpy() ...\n");
    for (int x = 0; x < 16; x++) {
        if (mem[x] != 0) {
            printf("[%d] : %c\n", x, mem[x]);
        } else {
            printf("[%d] :  \n", x);
        }
    }
    printf("\n[i] Done!\n");

	printf("[i] Performing strcpy of %s into mem ...\n", string);

	strcpy(mem, string);

    printf("[i] Analyzing content of mem after strcpy() ...\n");
    for (int x = 0; x < 16; x++) {
        if (mem[x] != 0) {
            printf("[%d] : %c\n", x, mem[x]);
        } else {
            printf("[%d] :  \n", x);
        }
    }
    printf("\n[i] Done!\n");

	// Search for the first non null char
    printf("Locating null character ...\n", i);
	for(i = 10; i >= 0; i--)
	{
		
        // Strings are terminated by null
		// Find the first character
		if(mem[i] != 0)
		{
            lastChar = i;
            
            printf("Found the first character: %c at index %d\n", mem[i], lastChar);
			
            break;
		}
	}
	
	// Swap lower case <-> capital letters
	for(i = 0; i <= lastChar; i++)
	{
		// Handle lower case
		if(mem[i] >= 'a') {
			mem[i] -= 'a' - 'A';
		} else {
			// Handle upper case
			if(mem[i] >= 'A') {
				mem[i] += 'a' - 'A';
			}
		}
	}

    printf("[i] Status of lastChar is now: %d\n", lastChar);
	
	// Print starting with the last character.
	for(i = lastChar; i >= 0; i--)
		printf("%c", mem[i]);
	printf("\n");
	
	// Cleanup.
	free(mem);

}

int main(int argc, char *argv[])
{
	int i;
	// Iterate over the parameters in reverse.
	for(i = argc-1; i > 0; i--)
		reverse(argv[i]);
	return 0;
}

// This comment is potentially a bug.
