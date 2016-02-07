package no.overflow.it3708.controller;

import javafx.animation.Animation;
import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.control.Button;
import javafx.scene.control.Slider;
import javafx.scene.paint.Color;
import javafx.scene.shape.FillRule;
import javafx.scene.shape.Line;
import javafx.util.Duration;
import no.overflow.it3708.Main;
import no.overflow.it3708.model.Boid;
import no.overflow.it3708.model.Obstruction;
import no.overflow.it3708.model.Predator;
import org.apache.log4j.Logger;

import java.util.ArrayList;

/**
 * Created by Aleksander Skraastad (myth) on 1/26/16.
 * <p/>
 * project1 is licenced under the MIT licence.
 */
public class BoidController {

    private Logger log = Logger.getLogger(BoidController.class);
    private @FXML Canvas canvas;
    public @FXML Slider alignment;
    public @FXML Slider cohesion;
    public @FXML Slider separation;
    public @FXML Slider velocity;
    public @FXML Slider fear;
    private @FXML Button startButton;
    private @FXML Button stopButton;
    private GraphicsContext gc;
    private ArrayList<Boid> flock;
    private ArrayList<Obstruction> obstructions;
    private ArrayList<Predator> predators;
    private Timeline timeline;

    public void initialize() {
        log.info("Initializing BoidController...");

        flock = new ArrayList<>();
        obstructions = new ArrayList<>();
        predators = new ArrayList<>();

        gc = canvas.getGraphicsContext2D();
        gc.setFill(Color.WHITE);
        gc.fillRect(0., 0., Main.CANVAS_WIDTH, Main.CANVAS_HEIGHT);

        // Initialize all boids
        for (int i = 0; i < Main.NUM_BOIDS; i++) {
            Boid b = new Boid(flock, this);
            drawBoid(b);
        }

        // Add some stuff
        addObstaclesAndPredators();

        // Set up our animation timeline
        timeline = new Timeline(new KeyFrame(
            Duration.millis(Main.GUI_FRAME_INTERVAL),
            event -> tick()
        ));
        timeline.setCycleCount(Animation.INDEFINITE);

        log.info("Initialized " + Main.NUM_BOIDS + " boids.");
    }

    public void addObstaclesAndPredators() {
        // Initialize obstructions
        Obstruction obsOne = new Obstruction(this);
        Obstruction obsTwo = new Obstruction(this);
        obsOne.setPosition(150, 150);
        obsTwo.setPosition(500, 400);
        drawObstruction(obsOne);
        drawObstruction(obsTwo);

        Predator predOne = new Predator(this);
        Predator predTwo = new Predator(this);
        drawPredator(predOne);
        drawPredator(predTwo);
    }

    public void clearCanvas() {
        gc.clearRect(-2, -2, Main.CANVAS_WIDTH + 2, Main.CANVAS_HEIGHT + 2);
        gc.setFill(Color.WHITE);
        gc.fillRect(0., 0., Main.CANVAS_WIDTH, Main.CANVAS_HEIGHT);
    }

    public void drawBoid(Boid b) {
        gc.setFill(Color.RED);
        gc.fillOval(
            b.position.get(0) - b.radius,
            b.position.get(1) - b.radius,
            b.radius * 2,
            b.radius * 2
        );
        gc.setLineWidth(1);
        gc.setStroke(Color.BLACK);
        gc.strokeLine(
            b.position.get(0),
            b.position.get(1),
            b.position.get(0) + b.velocity.get(0) * 3,
            b.position.get(1) + b.velocity.get(1) * 3
        );
    }

    /**
     * Draws an obstruction on the canvas
     * @param o An Obstruction object
     */
    public void drawObstruction(Obstruction o) {
        gc.setFill(Color.BLUE);
        gc.setLineWidth(2);
        gc.fillOval(
            o.position.get(0) - o.radius,
            o.position.get(1) - o.radius,
            o.radius * 2,
            o.radius * 2
        );
        gc.setStroke(Color.BLACK);
        gc.strokeOval(
            o.position.get(0) - o.radius,
            o.position.get(1) - o.radius,
            o.radius * 2,
            o.radius * 2
        );
    }

    public void drawPredator(Predator b) {
        gc.setFill(Color.YELLOW);
        gc.fillOval(
            b.position.get(0) - b.radius,
            b.position.get(1) - b.radius,
            b.radius * 2,
            b.radius * 2
        );
        gc.setLineWidth(1);
        gc.setStroke(Color.BLACK);
        gc.strokeLine(
            b.position.get(0),
            b.position.get(1),
            b.position.get(0) + b.velocity.get(0) * 5,
            b.position.get(1) + b.velocity.get(1) * 5
        );
        gc.strokeOval(
            b.position.get(0) - Main.NEIGHBOR_RADIUS,
            b.position.get(1) - Main.NEIGHBOR_RADIUS,
            Main.NEIGHBOR_RADIUS * 2,
            Main.NEIGHBOR_RADIUS * 2
        );
    }

    public void tick() {
        clearCanvas();
        flock.forEach(f -> {
            f.applyForce();
            drawBoid(f);
        });
        obstructions.forEach(this::drawObstruction);
        predators.forEach(p -> {
            p.applyForce();
            drawPredator(p);
        });
    }

    public ArrayList<Obstruction> getObstructions() {
        return obstructions;
    }
    public ArrayList<Predator> getPredators() {
        return predators;
    }
    public ArrayList<Boid> getFlock() { return flock; }

    @FXML
    public void handleStartButtonClicked(ActionEvent e) {
        if (!timeline.getStatus().equals(Animation.Status.RUNNING)) {
            log.info("Starting Flocking simulation!");
            timeline.play();
        }
    }

    @FXML
    public void handleStopButtonClicked(ActionEvent e) {
        if (timeline.getStatus().equals(Animation.Status.RUNNING)) {
            log.info("Stopping Flocking simulation!");
            timeline.stop();
        }
    }
}
