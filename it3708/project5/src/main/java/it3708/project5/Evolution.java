package it3708.project5;

import it3708.project5.event.EvolutionEventListener;
import it3708.project5.population.Individual;
import it3708.project5.population.Population;
import it3708.project5.population.Selection;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.swing.*;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by Aleksander Skraastad (myth) on 4/21/16.
 * <p>
 * project5 is licenced under the MIT licence.
 */
public class Evolution extends SwingWorker<Population, Population> {
    public static final int[][] cost = Utilities.ReadExcelFile("cost.xlsx");
    public static final int[][] distance = Utilities.ReadExcelFile("distance.xlsx");

    private static Logger log = LoggerFactory.getLogger(Evolution.class);
    private Population population;
    private ArrayList<EvolutionEventListener> listeners;
    public Main main;
    public int generation = 0;

    /**
     * Construct an evolution loop
     */
    public Evolution() {
        listeners = new ArrayList<>();
        this.population = new Population(Main.POPULATION_SIZE);
    }

    /**
     * Shut down any threaded services and perform other stop/deconstruct operations
     */
    public void deconstruct() {
        population.deconstruct();
    }

    public void setMain(Main m) {
        main = m;
    }

    /**
     * Register an object as an event listener for generational events
     * @param e An object implementing the EvolutionEventListener interface
     */
    public void registerListener(EvolutionEventListener e) {
        if (!listeners.contains(e)) listeners.add(e);
    }

    /**
     * Register an object as an event listener for generational events
     * @param e An object implementing the EvolutionEventListener interface
     */
    public void unregisterListener(EvolutionEventListener e) {
        if (listeners.contains(e)) listeners.remove(e);
    }

    /**
     * Run the evolution loop for N generations and return the best individual
     */
    @Override
    public Population doInBackground() {
        log.info("Starting evolutionary loop ...");
        long startTime = System.currentTimeMillis();
        this.generation = 0;
        ArrayList<Individual> pareto = new ArrayList<>();

        this.population.sort();
        this.population.fronts.forEach(Population::crowdingDistanceAssignment);

        List<Individual> children = this.population.reproduce();

        // Main evolutionary loop
        while (++generation <= Main.NUM_GENERATIONS) {
            log.info(String.format("Generation %d", generation));

            this.population.merge(children);

            // Sort dat shit
            this.population.sort();

            log.info("Current population: " + this.population);

            // Establish base next generation
            Population next = new Population(0);
            int i = 0;

            while (next.getSize() + this.population.fronts.get(i).size() <= Main.POPULATION_SIZE) {
                Population.crowdingDistanceAssignment(this.population.fronts.get(i));
                next.merge(this.population.fronts.get(i));
                i++;
            }

            // Add remaining crowding distance sorted individuals from last rank
            Population.crowdingDistanceAssignment(this.population.fronts.get(i));
            this.population.fronts.get(i).sort(Selection::crowdingOperator);
            for (int x = 0; x < Main.POPULATION_SIZE - next.getSize(); x++) {
                next.pool.add(this.population.fronts.get(i).get(x));
            }

            // Publish latest population
            if (generation % Main.GUI_GENERATION_UPDATE == 0) publish(this.population);

            // Advance to next population and make them babies
            pareto = this.population.fronts.get(0);
            this.population = next;
            children = this.population.reproduce();
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

        // Print the front
        pareto.sort((a, b) -> Integer.compare(a.cost, b.cost));
        for (Individual i : pareto) {
            System.out.println(i);
        }

        return population;
    }

    @Override
    protected void process(List<Population> chunks) {
        main.newGeneration(chunks.get(chunks.size() - 1), this.generation);
    }
}
