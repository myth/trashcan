.PHONY: clean all check run

all: newImageIdea

newImageIdea: newImageIdea.c ppm.c
	gcc -O2 --std=c99 -o $@ $^ -lm

checker: checker.c ppm.c
	gcc -O2 --std=c99 -o $@ $^

check: checker flower_tiny_correct.ppm flower_small_correct.ppm flower_medium_correct.ppm
	./checker

run: newImageIdea
	./newImageIdea 1

clean:
	rm -f newImageIdea checker
