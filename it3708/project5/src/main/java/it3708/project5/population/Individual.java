package it3708.project5.population;

import it3708.project5.Evolution;
import it3708.project5.Main;
import it3708.project5.Utilities;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Random;
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Created by Aleksander Skraastad (myth) on 4/21/16.
 * <p>
 * project5 is licenced under the MIT licence.
 */
public class Individual {

    public static short[] cities = Individual._generateOrderedCitiesArray();
    private static AtomicInteger idGenerator = new AtomicInteger();

    private int _id;
    private boolean dirty = true;
    private boolean invulnerable = false;
    public double fitness;
    public int cost = Integer.MAX_VALUE;
    public int distance = Integer.MAX_VALUE;
    public AtomicInteger dominated;
    public HashSet<Individual> dominates;
    public double crowdingDistance = 0.0d;
    public int rank = Integer.MAX_VALUE;
    private Random rng = ThreadLocalRandom.current();

    public short[] genotype;

    /**
     * Construct an individual with a random genotype sequence
     */
    public Individual() {
        short[] randomGenotype = cities.clone();

        // Shuffle the order of elements
        Utilities.FisherYatesShuffle(randomGenotype);

        _init(randomGenotype);
    }

    /**
     * Construct an individual with the provided genotype, by cloning the array provided as an argument.
     * @param genotype An array of shorts
     */
    public Individual(short[] genotype) {
        _init(genotype.clone());
    }

    /**
     * Evaluate the objectives of this individual by assessing the objective functions on the phenotype.
     * Updates the cost and distance fields in this individual.
     */
    public void calculateObjectives() {
        // Shortcut if in a non-dirty state
        if (!dirty) return;

        _calculateCost();
        _calculateDistance();

        dirty = false;
    }

    /**
     * Empties the hashset containing solutions dominated by this individual
     */
    public void clearDominationSet() {
        dominates.clear();
    }

    /**
     * Dominate another individual by adding the to the dominated hash set.
     * This method is simplex, thus perform no increments on the individual argument.
     * @param i An individual instance.
     */
    public void dominate(Individual i) {
        dominates.add(i);
    }

    /**
     * Retrieve the number of times this individual has been dominated by another individual.
     * @return An integer.
     */
    public int getDominatedCount() {
        return this.dominated.get();
    }

    /**
     * Retrieve the set of solutions dominated by this individual.
     * @return A HashSet of dominated individuals.
     */
    public HashSet<Individual> getDominatesSet() {
        return dominates;
    }

    /**
     * Increments the dominated counter on this individual
     */
    public int incrementDominated() {
        return this.dominated.incrementAndGet();
    }

    /**
     * Decrements the dominated counter on this individual
     */
    public int decrementDominated() {
        return this.dominated.decrementAndGet();
    }

    /**
     * Check if this individual is marked as dirty
     * @return true if dirty, false otherwise
     */
    public boolean isDirty() {
        return dirty;
    }

    /**
     * Checks to see if this individual is dominated by the individual argument i.
     * Domination holds true iff:
     *
     * Individual i is no worse than this Individual in any of its objectives
     * Individual i is strictly better than this Individual in at least one of the objectives
     *
     * @param i An Individual instance
     * @return true if this individual is dominated by i
     */
    public boolean isDominatedBy(Individual i) {
        return cost >= i.cost && distance >= i.distance && (i.cost < cost || i.distance < distance);
    }

    /**
     * Check if this individual is invulnerable
     * @return true if invulnerable, false otherwise
     */
    public boolean isInvulnerable() {
        return invulnerable;
    }

    /**
     * Lock this individual, so it cannot have its genome altered
     */
    public void lock() {
        invulnerable = true;
    }

    /**
     * Unlock this individual, so it can have its genome altered
     */
    public void unlock() {
        invulnerable = false;
    }

    /**
     * Mutate this individual's genome by swapping n pairs of genotype indexes
     * @param n The number of random swaps to perform
     */
    void mutate(int n) {
        // If we hit below mutation threshold, swap genes N times
        if (rng.nextDouble() < Main.MUTATION_RATE) {
            int mutations = rng.nextInt(n);
            for (int i = 0; i < mutations; i++) {
                int from = rng.nextInt(Main.NUM_CITIES - 1);
                int to = rng.nextInt(Main.NUM_CITIES - 1);

                short tmp = genotype[to];
                genotype[to] = genotype[from];
                genotype[from] = tmp;
            }
        }
    }

    /**
     * Check if this individual has identical genome to another individual
     * @param other An Individual Instance
     * @return
     */
    public boolean hasEqualGenome(Individual other) {
        for (int i = 0; i < genotype.length; i++) {
            if (genotype[i] != other.genotype[i]) return false;
        }
        return true;
    }

    /**
     * Resets the dominated counter
     */
    public void resetDominatedCount() {
        this.dominated.set(0);
    }

    /**
     * Sets the rank of this individual.
     * @param i An integer representing the rank of this individual
     */
    public void setRank(int i) {
        rank = i;
    }

    /**
     * String representation of this Individual
     * @return A string representing this object containing its ID, and fitness value
     */
    public String toString() {
        return String.format("Individual[%d] C: %d, D: %d, CD: %.1f, Order: %s", _id, cost, distance, crowdingDistance, Arrays.toString(genotype));
    }

    /**
     * Calculates the cost value
     */
    private void _calculateCost() {
        cost = 0;
        for (int i = 0; i < this.genotype.length - 1; i++) {
            cost += Evolution.cost[genotype[i]][genotype[i + 1]];
        }
        cost += Evolution.cost[genotype[0]][genotype[genotype.length - 1]];
    }

    /**
     * Calculates the distance value
     */
    private void _calculateDistance() {
        distance = 0;
        for (int i = 0; i < this.genotype.length - 1; i++) {
            distance += Evolution.distance[genotype[i]][genotype[i + 1]];
        }
        distance += Evolution.distance[genotype[0]][genotype[genotype.length - 1]];
    }

    /**
     * Helper to initialize individual objects
     * @param genotype A short array containing unique short values between 0 and non-including NUM_CITIES;
     */
    private void _init(short[] genotype) {
        this.genotype = genotype;
        this._id = idGenerator.incrementAndGet();
        this.fitness = 0;
        this.dominates = new HashSet<>();
        this.dominated = new AtomicInteger();
    }

    /**
     * Helper method to create an ordered array of city IDs.
     * @return A short array of ordered unique city IDs.
     */
    private static short[] _generateOrderedCitiesArray() {
        short[] cities = new short[Main.NUM_CITIES];
        for (short i = 0; i < cities.length; i++) {
            cities[i] = i;
        }
        return cities;
    }
}
