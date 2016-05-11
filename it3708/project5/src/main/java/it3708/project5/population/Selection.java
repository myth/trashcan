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
    public static Individual tournamentSelection(List<Individual> group) {
        Individual[] pool = new Individual[Main.TOURNAMENT_SELECTION_K];
        Individual mostFit = null;

        // Select K random individuals for tournament
        for (int i = 0; i < pool.length; i++) {
            pool[i] = group.get(rng.nextInt(group.size()));
            // Store who is the most fit
            if (mostFit == null || crowdingOperator(pool[i], mostFit) == -1) {
                mostFit = pool[i];
            }
        }

        return mostFit;
    }

    /**
     * Crowding operator comparator
     * @param a Individual a
     * @param b Individual b
     * @return -1 if a is better than b, 1 if b is better than a, 0 if equal
     */
    public static int crowdingOperator(Individual a, Individual b) {
        if (a.rank < b.rank) {
            return -1;
        } else if (a.rank == b.rank) {
            if (a.crowdingDistance > b.crowdingDistance) return -1;
            if (a.crowdingDistance == b.crowdingDistance) return 0;
        }
        return 1;
    }
}
