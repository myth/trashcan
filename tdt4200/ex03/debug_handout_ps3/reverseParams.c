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
	
	strcpy(mem, string);
	// Search for the first non null char
	for(i = 10; i >= 0; i--)
	{
		// Strings are terminated by null
		// Find the first character
		if(mem[i] != 0)
		{
			lastChar = i;
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
