package no.overflow.it3708.project4.ea;

import no.overflow.it3708.project4.world.Board;

import java.util.Arrays;

/**
 * Created by Aleksander Skraastad (myth) on 4/12/16.
 * <p/>
 * project4 is licenced under the MIT licence.
 */
public class Phenotype {

    public double[] weights;
    public double bias;
    public double time;
    public double gain;

    public Phenotype(int numberOfNeurons, int numberOfIncoming) {
        weights = new double[numberOfNeurons + numberOfIncoming];
        bias = 0.0;
        time = 0.0;
        gain = 0.0;
    }

    public void construct(int[] genotype, int offset) {
        bias = (((double) genotype[offset] / EvolutionaryLoop.GENOME_GRANULARITY) * 10.0) - 10.0;
        time = ((double) genotype[offset + 1] / EvolutionaryLoop.GENOME_GRANULARITY) + 1.0;
        gain = (((double) genotype[offset + 2] / EvolutionaryLoop.GENOME_GRANULARITY) * 4.0) + 1.0;

        if (!Board.WRAP) {
            time *= 1.5;
            gain *= 1.1;
        } else if (Board.WRAP && !Board.PULL) {
            gain *= 1.2;
        }

        offset = offset + 3;
        for (int i = 0; i < weights.length; i++) {
            weights[i] = (((double) genotype[offset + i] / EvolutionaryLoop.GENOME_GRANULARITY) - 0.5) * 10.0;
        }
    }

    public String toString() {
        return "Phenotype [NumWeights: " + weights.length + ", Bias: " + bias + ", Time: " + time + ", Gain: " + gain + ", Weights: " +
            Arrays.toString(weights);
    }
}
