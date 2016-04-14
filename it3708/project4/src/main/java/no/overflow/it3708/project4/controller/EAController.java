package no.overflow.it3708.project4.controller;

import no.overflow.it3708.project4.ea.EvolutionaryLoop;
import no.overflow.it3708.project4.ea.Individual;
import org.apache.log4j.Logger;

/**
 * Created by Aleksander Skraastad (myth) on 4/11/16.
 * <p/>
 * project4 is licenced under the MIT licence.
 */
public class EAController {
    private static Logger log = Logger.getLogger(EAController.class);
    private CoreController core;
    private EvolutionaryLoop el;

    public EAController(CoreController c) {
        log.info("Initializing EAController ...");
        core = c;
    }

    public Individual evolveNeuralNetwork() {
        el = new EvolutionaryLoop();
        return el.loop();
    }

    public EvolutionaryLoop getEvolutionaryLoop() {
        return el;
    }
}
