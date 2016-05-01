package it3708.project5;

import it3708.project5.population.Individual;
import org.apache.log4j.PropertyConfigurator;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Arrays;

/**
 * Created by Aleksander Skraastad (myth) on 4/21/16.
 * <p>
 * project5 is licenced under the MIT licence.
 */
public class Main {
    public static final int NUM_GENERATIONS = 250;
    public static final int NUM_CITIES = 48;
    public static final int NUM_ELITES = 10;
    public static final int NUM_ADULTS = 55000;
    public static final int NUM_CHILDREN = 65000;
    public static final double CROSSOVER_RATE = 0.7;
    public static final double MUTATION_RATE = 1.0;
    public static final int TOURNAMENT_SELECTION_K = 100;
    public static final double TOURNAMENT_SELECTION_E = 0.2;

    /**
     * Main program method
     * @param args Command line argument array
     */
    public static void main(String[] args) {
        // Set up logging
        PropertyConfigurator.configure(Main.class.getClassLoader().getResourceAsStream("config/log4j.properties"));
        Logger log = LoggerFactory.getLogger(Main.class);

        log.info("Initializing Multi-Objective Evolutionary Algorithm solver for MTSP ...");

        Evolution evolution = new Evolution();

        try {
            Individual mostFit = evolution.run(NUM_GENERATIONS);
            log.info(String.format("Most fit individual: %s", mostFit));
        } catch (Exception e) {
            e.printStackTrace();
            evolution.deconstruct();
        }
    }
}
