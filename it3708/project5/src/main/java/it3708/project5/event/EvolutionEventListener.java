package it3708.project5.event;

import it3708.project5.population.Population;

/**
 * Created by Aleksander Skraastad (myth) on 5/11/16.
 * <p>
 * project5 is licenced under the MIT licence.
 */
public interface EvolutionEventListener {
    void newGeneration(Population p, int generation);
}
