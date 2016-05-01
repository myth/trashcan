package it3708.project5;

import it3708.project5.population.Individual;

/**
 * Created by Aleksander Skraastad (myth) on 4/25/16.
 * <p>
 * project5 is licenced under the MIT licence.
 */
public class Test {
    public static void main(String[] args) {
        Individual i = new Individual();
        i.calculateFitness();
        System.out.println(i);
    }
}
