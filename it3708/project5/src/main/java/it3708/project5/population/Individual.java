package it3708.project5.population;

import it3708.project5.Evolution;
import it3708.project5.Main;
import it3708.project5.Utilities;

import java.util.Arrays;
import java.util.Random;
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Created by Aleksander Skraastad (myth) on 4/21/16.
 * <p>
 * project5 is licenced under the MIT licence.
 */
public class Individual implements Comparable<Individual> {

    private static short[] cities = Individual._generateOrderedCitiesArray();
    private static AtomicInteger idGenerator = new AtomicInteger();

    private int _id;
    private boolean dirty = true;
    private boolean invulnerable = false;
    private double fitness;
    private Random rng = ThreadLocalRandom.current();

    private short[] genotype;

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
     * Evaluate the fitness of this individual by assessing the objective functions on the phenotype.
     * Updates the fitness field on this individual as well as return the value.
     *
     * This will simply return the fitness field if the "dirty" field is set to false.
     * @return The fitness value of this individual as an integer.
     */
    public double calculateFitness() {
        // Shortcut if in a non-dirty state
        if (!dirty) return fitness;

        int cost_sum = 0;
        int distance_sum = 0;
        for (int i = 0; i < this.genotype.length - 1; i++) {
            cost_sum += Evolution.cost[genotype[i]][genotype[i + 1]];
            distance_sum += Evolution.distance[genotype[i]][genotype[i + 1]];
        }

        cost_sum += Evolution.cost[genotype[0]][genotype[genotype.length - 1]];
        distance_sum += Evolution.distance[genotype[0]][genotype[genotype.length - 1]];

        // Update fitness and clear dirty flag.
        fitness = ((double) cost_sum / Evolution.avgCost + (double) distance_sum / Evolution.avgDistance);
        dirty = false;

        return fitness;
    }

    /**
     * Compares this individual to another individual, and ranks according to current fitness value.
     * @param other An Individual object
     * @return 1 if this individual is better than the other, -1 if opposite, or 0 if even.
     */
    @Override
    public int compareTo(Individual other) {
        if (this.getFitness() < other.getFitness()) return -1;
        else if (this.getFitness() > other.getFitness()) return 1;
        return 0;
    }

    /**
     * Perform crossover on this individual, producing a new individual whose genome is a crossover between
     * the two parts, if the dice roll is below the threshold value. Otherwise it will return itself.
     * Will return itself if this individual is currently invulnerable.
     * @param other An Individual object
     * @return A new Individual object if crossover has been performed, this individual otherwise.
     */
    public Individual crossover(Individual other) {
        if (!invulnerable && Math.random() < Main.CROSSOVER_RATE) {
            // TODO: Figure out how to perform crossover and do the necessary operations
            return new Individual(this.genotype);
        } else {
            return new Individual(this.genotype);
        }
    }

    /**
     * Retrieve the fitness value for this individual. If the dirty flag is true, the fitness will first have to
     * be re-calculated before being returned.
     * @return The fitness value of this individual
     */
    public double getFitness() {
        if (dirty) calculateFitness();
        return fitness;
    }

    /**
     * Check if this individual is marked as dirty
     * @return true if dirty, false otherwise
     */
    public boolean isDirty() {
        return dirty;
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
        // Abort if we are invulnerable
        if (invulnerable) return;

        // If we hit below mutation threshold, swap genes N times
        if (rng.nextDouble() < Main.MUTATION_RATE) {
            for (int i = 0; i < n; i++) {
                int from = rng.nextInt(Main.NUM_CITIES - 1);
                int to = rng.nextInt(Main.NUM_CITIES - 1);

                short tmp = genotype[to];
                genotype[to] = genotype[from];
                genotype[from] = tmp;
            }

            dirty = true;
        }
    }

    /**
     * String representation of this Individual
     * @return A string representing this object containing its ID, and fitness value
     */
    public String toString() {
        return String.format("Individual[%d] F: %.2f, C: %d, D: %d, Order: %s", _id, fitness, _calculateCost(), _calculateDistance(), Arrays.toString(genotype));
    }

    /**
     * Calculates the cost fitness
     * @return The total cost
     */
    private int _calculateCost() {
        int cost_sum = 0;
        for (int i = 0; i < this.genotype.length - 1; i++) {
            cost_sum += Evolution.cost[genotype[i]][genotype[i + 1]];
        }
        cost_sum += Evolution.cost[genotype[0]][genotype[genotype.length - 1]];

        return cost_sum;
    }

    /**
     * Calculates the distance fitness
     * @return The total distance
     */
    private int _calculateDistance() {
        int distance_sum = 0;
        for (int i = 0; i < this.genotype.length - 1; i++) {
            distance_sum += Evolution.distance[genotype[i]][genotype[i + 1]];
        }
        distance_sum += Evolution.distance[genotype[0]][genotype[genotype.length - 1]];

        return distance_sum;
    }

    /**
     * Helper to initialize individual objects
     * @param genotype A short array containing unique short values between 0 and non-including NUM_CITIES;
     */
    private void _init(short[] genotype) {
        this.genotype = genotype;
        this._id = idGenerator.incrementAndGet();
        this.fitness = 0;
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
