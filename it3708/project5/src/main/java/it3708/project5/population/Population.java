package it3708.project5.population;

import it3708.project5.Main;
import org.apache.log4j.spi.LoggerFactory;
import org.slf4j.Logger;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Random;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

/**
 * Created by Aleksander Skraastad (myth) on 4/21/16.
 * <p>
 * project5 is licenced under the MIT licence.
 */
public class Population {

    private Logger log;
    private ExecutorService es;
    private ArrayList<Individual> children;
    private ArrayList<Individual> adults;
    private Random rng;

    /**
     * Construct a new population object with it's own executor pool
     */
    public Population(int initialPopulationSize) {
        log = org.slf4j.LoggerFactory.getLogger(Population.class);
        es = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());
        children = new ArrayList<>();
        adults = new ArrayList<>();
        rng = new Random();

        // Add random individuals to pool
        for (int i = 0; i < initialPopulationSize; i++) {
            children.add(new Individual());
        }
    }

    /**
     * Enqueues fitness calculation of each individual as calculation
     * jobs distributed among available processor cores. Will block until all jobs are done to prevent race conditions.
     */
    public void calculateFitness() {
        long startTime = System.currentTimeMillis();

        List<Callable<Double>> tasks = new ArrayList<>();
        children.forEach(i -> tasks.add(i::calculateFitness));
        adults.forEach(i -> tasks.add(i::calculateFitness));
        try {
            List<Future<Double>> results = es.invokeAll(tasks);
            for (Future f : results) {
                while (!f.isDone());
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        long diff = System.currentTimeMillis() - startTime;
        log.info(String.format("Fitness calculation completed in %d ms", diff));
    }

    /**
     * Shuts down the executor service in this population
     */
    public void deconstruct() {
        es.shutdown();
    }

    /**
     * Retrieve the most fit individual in this population
     * @return The individual with the highest fitness value in this population. null if there are no individuals.
     */
    public Individual getMostFitIndividual() {
        Individual mostFitChild = _getMostFitIndividualFromCollection(children);
        Individual mostFitAdult = _getMostFitIndividualFromCollection(adults);

        if (mostFitChild != null && mostFitAdult != null) {
            if (mostFitAdult.getFitness() < mostFitChild.getFitness()) {
                return mostFitAdult;
            }
            else {
                return mostFitChild;
            }
        } else if (mostFitChild != null) {
            return mostFitChild;
        }
        else {
            return mostFitAdult;
        }
    }

    /**
     * Retrieves the number of adults in this population.
     * @return The number of adults as an integer.
     */
    public int getAdultPoolSize() {
        return adults.size();
    }

    /**
     * Retrieves the number of children in this population.
     * @return The number of children as an integer.
     */
    public int getChildPoolSize() {
        return children.size();
    }

    /**
     * Retrieves the total size of this population, both children and adults.
     * @return Total population size as integer.
     */
    public int getSize() {
        return children.size() + adults.size();
    }

    /**
     * Performs mutation on all individuals in this population
     */
    public void mutate() {
        int mutations = mutateAdults() + mutateChildren();
        log.debug(String.format("Total number of mutations this generation: %d", mutations));
    }

    /**
     * Performs mutation on all adults in this population
     * @return The number of mutations that occurred
     */
    public int mutateAdults() {
        int mutations = 0;

        for (Individual i : adults) {
            i.mutate(rng.nextInt(24));
            if (i.isDirty()) mutations++;
        }

        return mutations;
    }

    /**
     * Performs mutation on all children in this population
     * @return The number of mutations that occurred
     */
    public int mutateChildren() {
        int mutations = 0;

        for (Individual i : children) {
            i.mutate(rng.nextInt(24));
            if (i.isDirty()) mutations++;
        }

        return mutations;
    }

    /**
     * Performs adult selection using Generational Mixing on this population
     */
    public void performAdultSelection() {
        List<Individual> newAdults = Selection.generationalMixing(children, adults);

        log.debug(String.format("Converted %d children to adults", newAdults.size()));

        adults.clear();
        adults.addAll(newAdults);
    }

    /**
     * Performs parent selection using Tournament Selection on this population
     */
    public void performParentSelection() {
        List<Individual> parents = Selection.tournamentSelection(adults);

        log.debug(String.format("Selected %d adults for parenthood", parents.size()));

        _reproduce(parents);
    }

    /**
     * Unlocks all individuals in this population
     */
    public void unlock() {
        adults.forEach(Individual::unlock);
        children.forEach(Individual::unlock);

        log.debug("All children and adults have been unlocked");
    }

    /**
     * String representation of this population
     */
    public String toString() {
        return String.format("Population[Children: %d, Adults: %d]", children.size(), adults.size());
    }

    /**
     * Private helper method that retrieves the most fit individual from a collection of individuals
     * @param c A Collection of Individual objects
     * @return The Individual with the highest fitness value in the collection. null if empty.
     */
    private Individual _getMostFitIndividualFromCollection(Collection<Individual> c) {
        return c.stream().min((a, b) -> a.compareTo(b)).orElse(null);
    }

    /**
     * Private helper method that performs reproduction (crossover) on the selected parents, and injects them into
     * the child pool.
     * @param group A List of Individuals representing parents
     */
    private void _reproduce(List<Individual> group) {
        long startTime = System.currentTimeMillis();
        children.clear();

        int offset = 0;

        while (children.size() < Main.NUM_CHILDREN) {
            Individual one = group.get(offset);
            // If we have an odd number of parents, just add the last one as a new child and break out of the loop
            if (offset + 1 >= group.size()) {
                children.add(one);
                break;
            }
            Individual two = group.get(offset + 1);

            Individual childOne = one.crossover(two);
            Individual childTwo = two.crossover(one);

            children.add(childOne);
            children.add(childTwo);

            offset += 2;
        }

        log.debug(String.format("Created %d children from %d parents", children.size(), group.size()));

        long diff = System.currentTimeMillis() - startTime;
        log.info(String.format("Reproduction completed in %d ms", diff));
    }
}
