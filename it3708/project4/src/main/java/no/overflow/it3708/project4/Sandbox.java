package no.overflow.it3708.project4;

import no.overflow.it3708.project4.ea.EvolutionaryLoop;
import no.overflow.it3708.project4.ea.Individual;
import no.overflow.it3708.project4.nnet.NeuralNetwork;
import no.overflow.it3708.project4.world.Board;
import org.apache.log4j.PropertyConfigurator;

import java.util.Arrays;
import java.util.List;

/**
 * Created by Aleksander Skraastad (myth) on 4/12/16.
 * <p/>
 * project4 is licenced under the MIT licence.
 */
public class Sandbox {
    public static void main(String[] args) {
        PropertyConfigurator.configure(Sandbox.class.getClassLoader().getResource("config/log4j.properties"));

        long startTime = System.currentTimeMillis();

        NeuralNetwork.INPUT_NODES = 7;
        NeuralNetwork.OUTPUT_NODES = 2;
        Board.WRAP = true;
        Board.PULL = false;

        NeuralNetwork nn = new NeuralNetwork();
        Board b = new Board();
        Individual i = new Individual();
        i.initializeRandomGenotype();
        System.out.println(nn);
        System.out.println(i.translate());
        nn.reconfigure(i.translate());

        double[] results = nn.fire(b.sense());
        System.out.println(Arrays.toString(results));
        System.out.println(Tools.moveIntensity(results[0], results[1]));
        for (int x = 0; x < 20; x++) {
            b.right(4);
            results = nn.fire(b.sense());
            System.out.println(Arrays.toString(results));
            System.out.println(Tools.moveIntensity(results[0], results[1]));
        }

        long elapsedTime = System.currentTimeMillis() - startTime;
        System.out.println("Elapsed time: " + elapsedTime + " ms");
    }
}
