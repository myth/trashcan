package no.overflow.it3708.project4.controller;

import javafx.scene.Scene;
import no.overflow.it3708.project4.nnet.NeuralNetwork;
import org.apache.log4j.Logger;

import java.util.Arrays;

/**
 * Created by Aleksander Skraastad (myth) on 4/11/16.
 * <p/>
 * project4 is licenced under the MIT licence.
 */
public class CoreController {
    private static Logger log = Logger.getLogger(CoreController.class);

    public WorldController world;
    public EAController ea;
    public NeuralNetwork nnet;

    public CoreController() {
        log.info("Initializing CoreController ...");
        ea = new EAController(this);
        nnet = new NeuralNetwork();
    }

    public void bindKeyListeners(Scene scene) {
        scene.setOnKeyPressed(e -> {
            switch (e.getCode()) {
                case LEFT:
                    world.board.left(1);
                    world.board.tick();
                    world.drawCanvas();
                    log.info("Sensing: " + Arrays.toString(world.board.sense()) + " " + world.board);
                    break;
                case RIGHT:
                    world.board.right(1);
                    world.board.tick();
                    world.drawCanvas();
                    log.info("Sensing: " + Arrays.toString(world.board.sense()) + " " + world.board);
                    break;
                case SPACE:
                    world.board.pull();
                    world.board.tick();
                    world.drawCanvas();
                    log.info("Sensing: " + Arrays.toString(world.board.sense()) + " " + world.board);
                    break;
            }
        });
    }
}
