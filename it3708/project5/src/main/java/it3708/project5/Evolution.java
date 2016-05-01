package it3708.project5;

import it3708.project5.population.Individual;
import it3708.project5.population.Population;
import it3708.project5.population.Selection;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;

/**
 * Created by Aleksander Skraastad (myth) on 4/21/16.
 * <p>
 * project5 is licenced under the MIT licence.
 */
public class Evolution {
    public static final int[][] cost = Utilities.ReadExcelFile("cost.xlsx");
    public static final int[][] distance = Utilities.ReadExcelFile("distance.xlsx");
    public static final double avgCost = Utilities.calculateAverageFromMatrix(cost);
    public static final double avgDistance = Utilities.calculateAverageFromMatrix(distance);

    private static Logger log = LoggerFactory.getLogger(Evolution.class);
    private Population population;

    /**
     * Construct an evolution loop
     */
    public Evolution() {
        population = new Population(Main.NUM_CHILDREN);
    }

    /**
     * Shut down any threaded services and perform other stop/deconstruct operations
     */
    public void deconstruct() {
        population.deconstruct();
    }

    /**
     * Run the evolution loop for N generations and return the best individual
     */
    public Individual run(int n) {
        log.info("Starting evolutionary loop ...");
        long startTime = System.currentTimeMillis();
        int generation = 0;

        // Assess the fitness ouf our random children
        population.calculateFitness();

        // Main evolutionary loop
        while (++generation <= n) {
            log.info(String.format("Generation %d", generation));

            population.unlock();
            population.performAdultSelection();
            population.performParentSelection();
            population.mutate();
            population.calculateFitness();

            log.info("Most fit: " + population.getMostFitIndividual());
        }

        // Halt the executor service threads in the population object
        population.deconstruct();

        long diff = System.currentTimeMillis() - startTime;
        log.info(
            String.format(
                "Complete! Evolved %d generations in %.1f seconds with total pool size %d",
                Main.NUM_GENERATIONS,
                (double) diff / 1000.0,
                population.getSize()
            )
        );

        return population.getMostFitIndividual();
    }
}
