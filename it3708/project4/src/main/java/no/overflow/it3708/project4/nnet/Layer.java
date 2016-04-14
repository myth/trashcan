package no.overflow.it3708.project4.nnet;

import no.overflow.it3708.project4.Tools;

import java.util.ArrayList;

/**
 * Created by Aleksander Skraastad (myth) on 4/11/16.
 * <p/>
 * project4 is licenced under the MIT licence.
 */
public class Layer {
    public ArrayList<Neuron> neurons;

    public Layer(int numberOfNeurons, int numberOfIncomingNeurons, Neuron.ActivationFunction af) {
        neurons = new ArrayList<>();
        for (int i = 0; i < numberOfNeurons; i++) {
            neurons.add(new Neuron(numberOfIncomingNeurons  + numberOfNeurons, af));
        }
    }

    public void updateOutputs(double[] incoming, double[] recurring) {
        double expSum = 0.0;

        // Calculate raw inputs
        for (Neuron n : neurons) {
            n.updateOutput(Tools.concat(incoming, recurring));
            expSum += Math.exp(n.output);
        }
        // Apply activation function
        for (Neuron n : neurons) {
            n.applyActivationFunction(expSum);
        }
    }

    public double[] getOutputArray() {
        double[] outputs = new double[neurons.size()];
        for (int i = 0; i < neurons.size(); i++) {
            outputs[i] = neurons.get(i).output;
        }
        return outputs;
    }

    public double[] getStateArray() {
        double[] outputs = new double[neurons.size()];
        for (int i = 0; i < neurons.size(); i++) {
            outputs[i] = neurons.get(i).state;
        }
        return outputs;
    }

    public void initializeRandomWeights() {
        neurons.forEach(Neuron::initializeRandomWeights);
    }

    public String toString() {
        String output = "Layer{" + neurons.size() + "}\n";;
        for (Neuron n : neurons) {
            output += n.toString() + "\n---\n";
        }
        return output;
    }
}
