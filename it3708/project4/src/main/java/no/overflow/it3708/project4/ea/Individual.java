package no.overflow.it3708.project4.ea;

import no.overflow.it3708.project4.Tools;
import no.overflow.it3708.project4.nnet.NeuralNetwork;
import no.overflow.it3708.project4.world.Board;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Created by Aleksander Skraastad (myth) on 4/11/16.
 * <p/>
 * project4 is licenced under the MIT licence.
 */
public class Individual {
    public double CAPTURED_W = 1.0;
    public double AVOIDED_W = 1.0;
    public double MISSED_W = 1.0;
    public double FAILED_W = 1.0;

    public static AtomicInteger _IdCounter = new AtomicInteger();
    public static Random rand = new Random();
    public boolean invulnerable = false;
    public boolean dirty = true;
    public int ID;
    public int[] genotype;
    public double fitness;

    public Individual() {
        ID = _IdCounter.incrementAndGet();
        genotype = new int[EvolutionaryLoop.GENOME_LENGTH];
        fitness = 0.0;
        initializeRandomGenotype();
    }

    public Individual(int[] genotype) {
        ID = _IdCounter.incrementAndGet();
        fitness = 0.0;
        this.genotype = genotype.clone();
    }

    public void initializeRandomGenotype() {
        for (int i = 0; i < genotype.length; i++) {
            genotype[i] = rand.nextInt(EvolutionaryLoop.GENOME_GRANULARITY + 1);
        }
    }

    /**
     * Perform basic genome mutation
     */
    public void mutate() {
        if (invulnerable) {
            invulnerable = false;
        } else {
            if (rand.nextDouble() < EvolutionaryLoop.MUTATION_RATE) {
                int mutationPoint = rand.nextInt(EvolutionaryLoop.GENOME_LENGTH);
                genotype[mutationPoint] = rand.nextInt(EvolutionaryLoop.GENOME_GRANULARITY + 1);
                dirty = true;
            }
            if (rand.nextDouble() < EvolutionaryLoop.COMPONENT_MUTATION_RATE) {
                int startMutation = rand.nextInt(EvolutionaryLoop.GENOME_LENGTH);
                int stopMutation = rand.nextInt(EvolutionaryLoop.GENOME_LENGTH);
                for (int x = Math.min(startMutation, stopMutation); x < Math.max(startMutation, stopMutation); x++) {
                    genotype[x] = rand.nextInt(EvolutionaryLoop.GENOME_GRANULARITY + 1);
                }
            }
        }
    }

    /**
     * Cross the genome of two indvididuals
     * @param first An Individual
     * @param second An Individual
     */
    public static void crossOver(Individual first, Individual second) {
        int crossoverPoint = rand.nextInt(EvolutionaryLoop.GENOME_LENGTH);
        for (int i = 0; i < crossoverPoint; i++) {
            int tmp = first.genotype[i];
            first.genotype[i] = second.genotype[i];
            second.genotype[i] = tmp;
            first.dirty = true;
            second.dirty = true;
        }
    }

    /**
     * Translate the genotype into a phenotype with appropriate values
     * @return An array of doubles containing values ready for NeuralNetwork reconfiguration
     */
    public List<Phenotype> translate() {
        ArrayList<Phenotype> phenotypes = new ArrayList<>();
        for (int i = 0; i < NeuralNetwork.HIDDEN_NODES; i++) {
            int offset = i * (3 + NeuralNetwork.HIDDEN_NODES + NeuralNetwork.INPUT_NODES);
            Phenotype p = new Phenotype(NeuralNetwork.HIDDEN_NODES, NeuralNetwork.INPUT_NODES);
            p.construct(genotype, offset);
            phenotypes.add(p);
        }
        for (int i = 0; i < NeuralNetwork.OUTPUT_NODES; i++) {
            int offset = (NeuralNetwork.HIDDEN_NODES  + i) * (3 + NeuralNetwork.OUTPUT_NODES + NeuralNetwork.HIDDEN_NODES);
            Phenotype p = new Phenotype(NeuralNetwork.OUTPUT_NODES, NeuralNetwork.HIDDEN_NODES);
            p.construct(genotype, offset);
            phenotypes.add(p);
        }

        return phenotypes;
    }

    /**
     * Create a NeuralNetwork and a Board, then run 600 iterations on the board before calculating total
     * fitness.
     */
    public Double calculateFitness() {
        // return if there is no change
        if (!dirty) return fitness;

        // Run through the network.
        NeuralNetwork nn = new NeuralNetwork();
        // Reconfigure network with current phenotype
        nn.reconfigure(this.translate());
        // Make a test world
        Board board = new Board();
        // Run 600 timesteps
        for (int step = 0; step < 600; step++) {
            double[] results = nn.fire(board.sense());
            int maxIndex = Tools.argMax(results);
            int steps = Tools.moveIntensity(results[0], results[1]);
            switch (maxIndex) {
                case 0:
                    board.left(steps);
                    break;
                case 1:
                    board.right(steps);
                    break;
                case 2:
                    board.pull();
                    break;
            }
            board.tick();
        }

        fitness = board.agent.numCaptured;
        fitness += board.agent.numAvoided;

        if (Board.WRAP && !Board.PULL) {
            fitness += board.agent.numCaptured;
            fitness /= 1 + (board.agent.numMissed + board.agent.numStruck * 2);
        } else if (!Board.WRAP) {
            FAILED_W = 3.5;
            MISSED_W = 2.0;
            fitness += board.agent.numCaptured * 5;
            fitness /= 1 + (board.agent.numMissed * MISSED_W + board.agent.numStruck * FAILED_W);
        } else if (Board.WRAP && Board.PULL) {
            MISSED_W = 2.0;
            FAILED_W = 42.0; // 36.0
            fitness += Math.pow(board.agent.numCaptured, 2);
            fitness /= 1 + (board.agent.numMissed * MISSED_W + board.agent.numStruck * FAILED_W);
        }

        // Reset the dirty flag
        dirty = false;

        return fitness;
    }

    public String toString() {
        return "Individual[" + ID + "] Fitness: " + fitness;
    }
}
