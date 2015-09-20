.PHONY: clean all check run_reference run

all: newImageIdea newImageIdeaReference

newImageIdea: newImageIdea.c ppm.c
	gcc -O2 --std=c99 -o $@ $^ -lm


newImageIdeaReference: newImageIdeaReference.c ppm.c
	gcc -O2 --std=c99 -o $@ $^ -lm

checker: checker.c ppm.c
	gcc -O2 --std=c99 -o $@ $^

check: checker flower_tiny_correct.ppm flower_small_correct.ppm flower_medium_correct.ppm
	./checker

run_reference flower_tiny_correct.ppm flower_small_correct.ppm flower_medium_correct.ppm: newImageIdeaReference 
	./newImageIdeaReference

run: newImageIdea
	./newImageIdea 1

clean:
	rm -f newImageIdea newImageIdeaReference checker
