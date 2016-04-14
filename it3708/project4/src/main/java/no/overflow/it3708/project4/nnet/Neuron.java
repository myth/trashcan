package no.overflow.it3708.project4.nnet;

import java.util.Arrays;

/**
 * Created by Aleksander Skraastad (myth) on 4/11/16.
 * <p/>
 * project4 is licenced under the MIT licence.
 */
public class Neuron {
    public double[] weights;
    public double output;
    public double state;
    public double bias;
    public double gain;
    public double time;
    public ActivationFunction activationFunction;

    public Neuron(int numberOfIncoming, ActivationFunction af) {
        weights = new double[numberOfIncoming];
        output = 0.0;
        bias = 0.0;
        gain = 1.0;
        time = 1.0;
        state = 0.0;
        activationFunction = af;
    }

    public void initializeRandomWeights() {
        for (int i = 0; i < weights.length; i++) {
            weights[i] = (Math.random() - 0.5) * 10.0;
        }
    }

    public void updateOutput(double[] incoming) {
        for (int i = 0; i < incoming.length; i++) {
            output += weights[i] * incoming[i];
        }
        output += bias;
        output = 1 / (1 + Math.exp(output));
        state += (1 / time) * (output - state);
    }

    public void applyActivationFunction(double layerExpSum) {
        switch (activationFunction) {
            case SIGMOID:
                output = 1 / (1 + Math.exp(-gain * state));
            case RELU:
                output = Math.max(gain * state, 0.0);
                break;
            case SOFTMAX:
                output = Math.exp(gain * state) / layerExpSum;
                break;
        }
    }

    public enum ActivationFunction {
        RELU,
        SOFTMAX,
        SIGMOID
    }

    public String toString() {
        return "Neuron{Output: " + output + ", Gain: " + gain + ", Bias: " + bias + ", Time: " + time +
            ", Weights: " + Arrays.toString(weights) + "}";
    }
}
