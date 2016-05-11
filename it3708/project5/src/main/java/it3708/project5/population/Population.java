package it3708.project5.population;

import it3708.project5.Main;
import org.slf4j.Logger;

import java.util.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * Created by Aleksander Skraastad (myth) on 4/21/16.
 * <p>
 * project5 is licenced under the MIT licence.
 */
public class Population {

    private Logger log;
    private ExecutorService es;
    public ArrayList<Individual> pool;
    public ArrayList<ArrayList<Individual>> fronts;
    private Random rng;

    /**
     * Construct a new population object with it's own executor pool
     */
    public Population(int initialPopulationSize) {
        log = org.slf4j.LoggerFactory.getLogger(Population.class);
        es = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());
        pool = new ArrayList<>();
        fronts = new ArrayList<>();
        rng = new Random();

        // Add random individuals to pool
        for (int i = 0; i < initialPopulationSize; i++) {
            pool.add(new Individual());
        }

        // Add initial front
        fronts.add(new ArrayList<>());
    }

    /**
     * Shuts down the executor service in this population
     */
    public void deconstruct() {
        es.shutdown();
    }

    /**
     * Retrieves the total size of this population, both children and adults.
     * @return Total population size as integer.
     */
    public int getSize() {
        return pool.size();
    }

    /**
     * Extends the current population pool with the argument group
     * @param group A list of Individuals
     */
    public void merge(List<Individual> group) {
        pool.addAll(group);
    }

    /**
     * Performs a reproduction session across the current population, performing crossover on new
     * individuals and returning a pool of new children.
     * @return An ArrayList of Individual objects with new genetic properties.
     */
    public ArrayList<Individual> reproduce() {
        long startTime = System.currentTimeMillis();
        ArrayList<Individual> children = new ArrayList<>();

        while (children.size() < Main.POPULATION_SIZE) {
            Individual p1 = Selection.tournamentSelection(this.pool);
            Individual p2 = Selection.tournamentSelection(this.pool);

            Individual c1 = new Individual(p1.genotype);
            Individual c2 = new Individual(p2.genotype);

            _crossover(c1, c2);

            c1.mutate(Main.MUTATION_STRENGTH);
            c2.mutate(Main.MUTATION_STRENGTH);

            c1.calculateObjectives();
            c2.calculateObjectives();

            children.add(c1);
            children.add(c2);
        }

        long diff = System.currentTimeMillis() - startTime;
        // LoggerFactory.getLogger(Population.class).debug(String.format("Reproduction completed in %d ms", diff));

        return children;
    }

    /**
     * Sorts this population given some sorting function
     */
    public void sort() {
        _fastNonDominatedSort();
    }

    /**
     * String representation of this population
     */
    public String toString() {
        return String.format("Population[Pool: %d] Fronts: %d, First-front-size: %d", pool.size(), fronts.size(), fronts.get(0).size());
    }

    /**
     * Static helper method that calculates and assigns crowding distance on a front
     */
    public static void crowdingDistanceAssignment(ArrayList<Individual> front) {
        // Break if front is empty
        if (front.size() == 0) return;

        int n = front.size();

        // Cost axis
        front.sort((a, b) -> Integer.compare(a.cost, b.cost));
        front.get(0).crowdingDistance = Integer.MAX_VALUE;
        front.get(n - 1).crowdingDistance = Integer.MAX_VALUE;

        int fmax_cost = front.get(n - 1).cost;
        int fmin_cost = front.get(0).cost;
        int fmax_dist = front.get(n - 1).distance;
        int fmin_dist = front.get(0).distance;

        for (Individual i : front) {
            if (i.distance > fmax_dist) fmax_dist = i.distance;
            else if (i.distance < fmin_dist) fmin_dist = i.distance;
        }

        for (int i = 1; i < n - 1; i++) {
            double divisor = (fmax_cost - fmin_cost);
            if (divisor == 0) divisor = 1.0d;
            front.get(i).crowdingDistance = (Math.abs(front.get(i + 1).cost - front.get(i - 1).cost) / divisor);

            divisor = (fmax_dist - fmin_dist);
            if (divisor == 0) divisor = 1.0d;
            front.get(i).crowdingDistance += (Math.abs(front.get(i + 1).distance - front.get(i - 1).distance) / divisor);
        }
    }

    /**
     * Performs crossover on a pair of individuals
     * @param a An Individual instance
     * @param b An Individual instance
     */
    public void _crossover(Individual a, Individual b) {
        int start = rng.nextInt(a.genotype.length);
        int end = rng.nextInt(a.genotype.length);

        for (int x = start; x < end; x++) {
            short prev_a = a.genotype[x];
            short prev_b = b.genotype[x];

            a.genotype[x] = prev_b;
            b.genotype[x] = prev_a;

            for (int i = 0; i < a.genotype.length; i++) {
                if (i != x) {
                    if (a.genotype[i] == prev_b) {
                        a.genotype[i] = prev_a;
                    }
                    if (b.genotype[i] == prev_a) {
                        b.genotype[i] = prev_b;
                    }
                }
            }
        }
    }

    /**
     * Private helper method that performs the fast non-dominated sorting algorithm on the current pool
     */
    private void _fastNonDominatedSort() {
        long startTime = System.currentTimeMillis();

        fronts = new ArrayList<>();
        fronts.add(new ArrayList<>());

        // For all individuals in the pool
        for (Individual a : pool) {
            a.dominated.set(0);
            a.dominates = new HashSet<>();

            // Cross check domination against all neighboring individuals
            for (Individual b : pool) {
                if (a.isDominatedBy(b)) {
                    a.dominated.incrementAndGet();
                } else if (b.isDominatedBy(a)) {
                    a.dominates.add(b);
                }
            }

            // If the current individual is a non-dominated solution, add it to the front
            if (a.dominated.get() == 0) {
                fronts.get(0).add(a);
                a.rank = 0;
            }
        }

        // Calculate ranks
        int front_index = 0;
        while (fronts.get(front_index).size() > 0) {
            ArrayList<Individual> tmp_front = new ArrayList<>();

            for (Individual a : fronts.get(front_index)) {
                for (Individual b : a.getDominatesSet()) {
                    if (b.decrementDominated() == 0) {
                        b.setRank(front_index + 1);
                        tmp_front.add(b);
                    }
                }
            }

            front_index++;
            fronts.add(tmp_front);
        }

        long diff = System.currentTimeMillis() - startTime;
        // log.debug(String.format("Fast non-dominated sorting completed in %d ms", diff));
    }
}