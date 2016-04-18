package no.overflow.it3708.project4.ea;

import no.overflow.it3708.project4.nnet.NeuralNetwork;
import org.apache.log4j.Logger;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Random;
import java.util.concurrent.*;

/**
 * Created by Aleksander Skraastad (myth) on 4/12/16.
 * <p/>
 * project4 is licenced under the MIT licence.
 */
public class EvolutionaryLoop {
    public static final int NUMBER_OF_GENERATIONS = 800;
    public static final int GENOME_LENGTH = calculateGenomeLength();
    public static final int GENOME_GRANULARITY = 2048;
    public static final int CHILD_POOL_SIZE = 200;
    public static final int ADULT_POOL_SIZE = 150;
    public static final int ELITISM = 20;
    public static final double MUTATION_RATE = 0.95; // 0.8
    public static final double COMPONENT_MUTATION_RATE = 0.25;
    public static final double CROSSOVER_RATE = 0.9;
    public static final int TOURNAMENT_SELECTION_K = 10;
    public static final double TOURNAMENT_SELECTION_EPSILON = 0.25;
    private static final Logger log = Logger.getLogger(EvolutionaryLoop.class);

    private static Random rand = new Random();
    private boolean _running = false;
    private int _generation = 0;
    private ExecutorService es;
    private List<Individual> children;
    private List<Individual> adults;
    private Individual mostFit = new Individual();

    public EvolutionaryLoop() {
        adults = new ArrayList<>();
        children = new ArrayList<>();
        es = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());
        for (int i = 0; i < CHILD_POOL_SIZE; i++) {
            children.add(new Individual());
        }
    }

    public Individual loop() {
        log.info("Starting evolutionary loop ...");

        // Schedule fitness update and await...
        updateFitness(children);

        _running = true;
        while (_running) {
            _generation++;

            performAdultSelection();

            performParentSelection();

            performMutations();

            // Schedule fitness update and await...
            updateFitness(children);
            updateFitness(adults);

            Individual bestChallenger = getMostFit();
            if (bestChallenger.fitness > mostFit.fitness) mostFit = getMostFit();
            log.info("[" + _generation + "] Most fit: " + mostFit);

            if (_generation == NUMBER_OF_GENERATIONS) stop();
        }

        // Return the most fit
        return mostFit;
    }

    public void stop() {
        log.info("Stopping evolutionary loop ...");
        _running = false;
        es.shutdown();
    }

    /**
     * Perform adult selection
     */
    private void performAdultSelection() {
        ArrayList<Individual> pool = new ArrayList<>();
        pool.addAll(children);
        pool.addAll(adults);
        pool.sort((a, b) -> {
            if (a.fitness > b.fitness) return -1;
            else if (a.fitness < b.fitness) return 1;
            return 0;
        });
        children.clear();
        adults.clear();

        adults = pool.subList(0, ADULT_POOL_SIZE);
    }

    /**
     * Update fitness and update Most fit individual
     * @param pool A List of Individuals
     */
    private void updateFitness(List<Individual> pool) {
        List<Callable<Double>> tasks = new ArrayList<>();
        for (Individual i : pool) {
            tasks.add(i::calculateFitness);
        }
        try {
            List<Future<Double>> results = es.invokeAll(tasks);
            for (Future f : results) {
                while (!f.isDone());
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    /**
     * Perform parent selection and reproduction
     */
    private void performParentSelection() {
        ArrayList<Individual> pool = new ArrayList<>();

        // Sort by fitness
        adults.sort((a, b) -> {
            if (a.fitness > b.fitness) return -1;
            else if (a.fitness < b.fitness) return 1;
            return 0;
        });

        // Add elites
        for (int i = 0; i < ELITISM; i++) {
            Individual elite = adults.get(i);
            elite.invulnerable = true;
            pool.add(elite);
        }

        // Fill the pool with parents
        while (pool.size() < CHILD_POOL_SIZE) {
            ArrayList<Individual> local_group = new ArrayList<>();
            for (int i = 0; i < TOURNAMENT_SELECTION_K; i++) {
                int x = rand.nextInt(adults.size());
                local_group.add(adults.get(x));

                // If we are choosing the best
                if (rand.nextDouble() > TOURNAMENT_SELECTION_EPSILON) {
                    // Determine which individual of the random group has maximum fitness
                    double max = Double.NEGATIVE_INFINITY;
                    int maxIndex = 0;
                    for (int j = 0; j < local_group.size(); j++) {
                        if (local_group.get(i).fitness > max) {
                            maxIndex = i;
                            max = local_group.get(i).fitness;
                        }
                    }
                    pool.add(local_group.get(maxIndex));
                } else {
                    // Just add a random dude from the local group
                    pool.add(local_group.get(rand.nextInt(local_group.size())));
                }
            }
        }

        // Reproduction stage
        while (!pool.isEmpty()) {
            Individual parentOne = pool.get(0);
            Individual parentTwo = pool.get(1);

            // Check if we had an odd number of parents in pool
            if (pool.size() == 1) {
                children.add(new Individual(parentOne.genotype));
                return;
            }

            pool.remove(0);
            pool.remove(0);

            Individual childOne = new Individual(parentOne.genotype);
            Individual childTwo = new Individual(parentTwo.genotype);

            if (rand.nextDouble() < CROSSOVER_RATE) Individual.crossOver(childOne, childTwo);

            children.add(childOne);
            children.add(childTwo);
        }
    }

    /**
     * Perform mutations
     */
    private void performMutations() {
        adults.forEach(Individual::mutate);
        children.forEach(Individual::mutate);
    }

    /**
     * Retrieves the most fit individual in the pools
     * @return An Individual with the highest fitness in the pools
     */
    private Individual getMostFit() {
        Comparator<Individual> desc = (a, b) -> {
            if (a.fitness > b.fitness) return -1;
            else if (a.fitness < b.fitness) return 1;
            return 0;
        };
        children.sort(desc);
        adults.sort(desc);

        if (children.get(0).fitness > adults.get(0).fitness) return children.get(0);
        return adults.get(0);
    }

    public static int calculateGenomeLength() {
        int length = 0;

        length += (NeuralNetwork.INPUT_NODES + NeuralNetwork.HIDDEN_NODES + 3) * NeuralNetwork.HIDDEN_NODES;
        length += (NeuralNetwork.HIDDEN_NODES + NeuralNetwork.OUTPUT_NODES + 3) * NeuralNetwork.OUTPUT_NODES;

        return length;
    }
}
