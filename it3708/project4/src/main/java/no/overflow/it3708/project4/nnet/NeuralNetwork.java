package no.overflow.it3708.project4.nnet;

import no.overflow.it3708.project4.ea.Phenotype;

import java.util.Arrays;
import java.util.List;

/**
 * Created by Aleksander Skraastad (myth) on 4/11/16.
 * <p/>
 * project4 is licenced under the MIT licence.
 */
public class NeuralNetwork {
    public static int INPUT_NODES = 5;
    public static int HIDDEN_NODES = 3;
    public static int OUTPUT_NODES = 2;
    Layer hidden, output;

    public NeuralNetwork() {
        hidden = new Layer(HIDDEN_NODES, INPUT_NODES, Neuron.ActivationFunction.SIGMOID);
        output = new Layer(OUTPUT_NODES, HIDDEN_NODES, Neuron.ActivationFunction.SIGMOID);
    }

    public void initializeRandomWeights() {
        hidden.initializeRandomWeights();
        output.initializeRandomWeights();
    }

    public double[] fire(double[] inputs) {
        hidden.updateOutputs(inputs, hidden.getOutputArray());
        output.updateOutputs(hidden.getOutputArray(), output.getOutputArray());

        return output.getOutputArray();
    }

    public void reconfigure(List<Phenotype> neurons) {
        for (int i = 0; i < hidden.neurons.size(); i++) {
            Phenotype p = neurons.get(0);
            neurons.remove(0);
            Neuron n = hidden.neurons.get(i);
            n.bias = p.bias;
            n.gain = p.gain;
            n.time = p.time;
            n.weights = p.weights.clone();
        }
        for (int i = 0; i < output.neurons.size(); i++) {
            Phenotype p = neurons.get(0);
            neurons.remove(0);
            Neuron n = output.neurons.get(i);
            n.bias = p.bias;
            n.gain = p.gain;
            n.time = p.time;
            n.weights = p.weights.clone();
        }
    }

    public String toString() {
        return "Hidden:\n" + hidden.toString() + "Output:\n" + output.toString() + "\n";
    }
}
