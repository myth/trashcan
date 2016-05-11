package it3708.project5;

import it3708.project5.population.Individual;
import it3708.project5.population.Population;

/**
 * Created by Aleksander Skraastad (myth) on 4/25/16.
 * <p>
 * project5 is licenced under the MIT licence.
 */
public class Test {
    public static void main(String[] args) {
        Population p = new Population(0);

        Individual a = new Individual();
        Individual b = new Individual();

        System.out.println(a);
        System.out.println(b);

        p._crossover(a, b);

        System.out.println(a);
        System.out.println(b);
    }
}
