package it3708.project5.population;

import it3708.project5.Main;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * Created by Aleksander Skraastad (myth) on 4/21/16.
 * <p>
 * project5 is licenced under the MIT licence.
 */
public class Selection {
    private static Logger log = LoggerFactory.getLogger(Selection.class);
    private static Random rng = new Random();

    /**
     * Perform tournament selection on a group of individuals, using parameters K and E, for local tournament size
     * and change of selecting just a random individual.
     * @param group A list of Individual objects
     * @return A List of Individual objects that have been selected through tournament selection
     */
    public static List<Individual> tournamentSelection(List<Individual> group) {
        long startTime = System.currentTimeMillis();

        ArrayList<Individual> selected = new ArrayList<>();
        group.sort((a, b) -> a.compareTo(b));

        // Preemptively extract the number of elites that should have green-card for selection
        for (int n = 0; n < Main.NUM_ELITES; n++) {
            selected.add(group.get(0));
            group.get(0).lock();
        }

        // Perform selection until we have reached our child pool size
        while (selected.size() < Main.NUM_CHILDREN) {
            Individual[] pool = new Individual[Main.TOURNAMENT_SELECTION_K];
            Individual mostFit = null;

            // Select K random individuals for tournament
            for (int i = 0; i < pool.length; i++) {
                pool[i] = group.get(rng.nextInt(group.size()));
                // Store who is the most fit
                if (mostFit == null || mostFit.getFitness() > pool[i].getFitness()) {
                    mostFit = pool[i];
                }
            }
            // If we score less than E, just select a random individual from the local pool
            if (rng.nextDouble() < Main.TOURNAMENT_SELECTION_E) {
                selected.add(pool[rng.nextInt(pool.length)]);
            // Otherwise select the most fit from the local pool
            } else {
                selected.add(mostFit);
            }
        }

        long diff = System.currentTimeMillis() - startTime;
        log.info(String.format("Parent selection (TournamentSelection) completed in %d ms", diff));

        return selected;
    }

    /**
     * Perform adult selection using Generational Mixing.
     * @param children A List of Individuals that represent the children
     * @param adults A List of Individuals that represent the adults
     * @return A List of Individuals that have been selected for adulthood
     */
    public static List<Individual> generationalMixing(List<Individual> children, List<Individual> adults) {
        long startTime = System.currentTimeMillis();
        List<Individual> pool = new ArrayList<>();

        // We need to sort the lists
        adults.sort((a, b) -> a.compareTo(b));
        children.sort((a, b) -> a.compareTo(b));

        // Declare start offset indexes
        int ci = 0;
        int ai = 0;

        // Continue until we have the desired amount of adults
        while (pool.size() < Main.NUM_ADULTS) {
            // Check if we have an empty adult pool (which we will have during the first generation)
            if (adults.size() == 0) {
                pool.add(children.get(ci++));
                continue;
            }

            // Check if next child or next adult
            if (children.get(ci).getFitness() < adults.get(ai).getFitness()) pool.add(children.get(ci++));
            else pool.add(adults.get(ai++));
        }

        long diff = System.currentTimeMillis() - startTime;
        log.info(String.format("Adult selection (GenerationalMixing) completed in %d ms", diff));

        return pool;
    }
}
