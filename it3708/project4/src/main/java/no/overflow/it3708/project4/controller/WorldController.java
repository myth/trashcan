package no.overflow.it3708.project4.controller;

import javafx.animation.Animation;
import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.application.Platform;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.control.Button;
import javafx.scene.control.CheckBox;
import javafx.scene.control.Slider;
import javafx.scene.input.MouseEvent;
import javafx.scene.paint.Color;
import javafx.util.Duration;
import no.overflow.it3708.project4.Main;
import no.overflow.it3708.project4.Sandbox;
import no.overflow.it3708.project4.Tools;
import no.overflow.it3708.project4.ea.EvolutionaryLoop;
import no.overflow.it3708.project4.nnet.NeuralNetwork;
import no.overflow.it3708.project4.world.Board;
import org.apache.log4j.Logger;

import java.util.Arrays;

/**
 * Created by Aleksander Skraastad (myth) on 4/11/16.
 * <p/>
 * project4 is licenced under the MIT licence.
 */
public class WorldController {
    private Logger log = Logger.getLogger(WorldController.class);
    private @FXML Canvas canvas;
    public @FXML Slider timeScaling;
    public @FXML Button startButton;
    public @FXML Button stopButton;
    public @FXML CheckBox isWrapping;
    public @FXML CheckBox isPulling;
    public @FXML Button trainButton;
    private GraphicsContext gc;
    private Timeline timeline;
    public CoreController core;
    public Board board;

    private static KeyFrame updateFrame;
    private static int cellSize = Main.CANVAS_WIDTH / Board.BOARD_WIDTH;

    public void initialize() {
        log.info("Initializing WorldController ...");

        gc = canvas.getGraphicsContext2D();
        gc.setFill(Color.WHITESMOKE);
        gc.fillRect(0., 0., Main.CANVAS_WIDTH, Main.CANVAS_HEIGHT);

        // Set up our animation timeline
        updateFrame = new KeyFrame(
            Duration.millis(30 + 300 * timeScaling.getValue()),
            event -> tick()
        );
        timeline = new Timeline(updateFrame);
        timeline.setCycleCount(600);

        board = new Board();
        isWrapping.setSelected(true);
        isPulling.setSelected(false);
        Board.WRAP = isWrapping.isSelected();
        Board.PULL = isPulling.isSelected();
        isPulling.setFocusTraversable(false);
        isWrapping.setFocusTraversable(false);
        timeScaling.setFocusTraversable(false);
        startButton.setFocusTraversable(false);
        stopButton.setFocusTraversable(false);
        trainButton.setFocusTraversable(false);
        canvas.setFocusTraversable(true);
        canvas.addEventFilter(MouseEvent.ANY, (e) -> canvas.requestFocus());

        drawGrid();
        drawAgent();
        drawBlock();

        log.info("Sensing: " + Arrays.toString(board.sense()) + " " + board);

        // Listen for changes on the slider, and refresh the keyframe list with new interval
        timeScaling.setOnMouseReleased(e -> {
            // Update tick delay
            boolean restart = timeline.getStatus().equals(Animation.Status.RUNNING);
            log.info("TimeScaling changed to " + timeScaling.getValue());
            timeline.stop();
            timeline.getKeyFrames().removeAll(updateFrame);
            updateFrame = new KeyFrame(
                Duration.millis(30 + 300 * timeScaling.getValue()),
                event -> tick()
            );
            timeline.getKeyFrames().add(updateFrame);
            if (restart) {
                timeline.play();
            }
        });

        // Listen for changes to wrapping
        isWrapping.setOnMouseReleased(e -> {
            Board.WRAP = isWrapping.isSelected();
            if (Board.WRAP) NeuralNetwork.INPUT_NODES = 5;
            else NeuralNetwork.INPUT_NODES = 7;
            core.nnet = new NeuralNetwork();
        });
        isPulling.setOnMouseReleased(e -> {
            Board.PULL = isPulling.isSelected();
            if (Board.PULL) NeuralNetwork.OUTPUT_NODES = 3;
            else NeuralNetwork.OUTPUT_NODES = 2;
            core.nnet = new NeuralNetwork();
        });
    }

    public void clearCanvas() {
        gc.clearRect(-2, -2, Main.CANVAS_WIDTH + 2, Main.CANVAS_HEIGHT + 2);
        gc.setFill(Color.WHITESMOKE);
        gc.fillRect(0., 0., Main.CANVAS_WIDTH, Main.CANVAS_HEIGHT);
    }

    public void tick() {
        clearCanvas();

        // Move the object
        double[] results = core.nnet.fire(board.sense());
        int maxIndex = Tools.argMax(results);
        int steps = Tools.moveIntensity(results[0], results[1]);

        log.info("Sensing: " + Arrays.toString(results) + " ArgMax: " + maxIndex + " " + board);

        switch (maxIndex) {
            case 0:
                board.left(steps);
                break;
            case 1:
                board.right(steps);
                break;
            case 2:
                board.pull();
                break;
        }
        board.tick();

        // Re-draw canvas
        drawGrid();
        drawBlock();
        drawAgent();
    }

    @FXML
    public void handleStartButtonClicked(ActionEvent e) {
        if (!timeline.getStatus().equals(Animation.Status.RUNNING)) {
            log.info("Starting Beer Tracker Agent replay!");
            board = new Board();
            timeline.playFromStart();
        }
    }

    @FXML
    public void handleStopButtonClicked(ActionEvent e) {
        if (timeline.getStatus().equals(Animation.Status.RUNNING)) {
            log.info("Stopping Beer Tracker Agent replay!");
            timeline.stop();
        }
    }

    @FXML
    public void handleTrainButton(ActionEvent e) {
        if (timeline.getStatus().equals(Animation.Status.RUNNING)) {
            timeline.stop();
            timeline = new Timeline(updateFrame);
        }
        Platform.runLater(() -> {
            core.nnet = new NeuralNetwork();
            core.ea = new EAController(core);
            core.nnet.reconfigure(core.ea.evolveNeuralNetwork().translate());
            System.out.println(core.nnet);
            System.out.println(Arrays.toString(core.nnet.fire(new double[]{0.0, 1.0, 1.0, 0.0, 0.0})));
            System.out.println(Arrays.toString(core.nnet.fire(new double[]{0.0, 1.0, 1.0, 0.0, 0.0})));
            System.out.println(Arrays.toString(core.nnet.fire(new double[]{0.0, 1.0, 1.0, 0.0, 0.0})));
            System.out.println(Arrays.toString(core.nnet.fire(new double[]{0.0, 1.0, 1.0, 0.0, 0.0})));
        });
    }

    public void drawCanvas() {
        clearCanvas();
        drawGrid();
        drawBlock();
        drawAgent();
    }

    private void drawGrid() {
        gc.setFill(Color.WHITE);
        gc.setStroke(Color.BLACK);
        gc.setLineWidth(1);
        for (int y = 0; y < Board.BOARD_HEIGHT; y++) {
            for (int x = 0; x < Board.BOARD_WIDTH; x++) {
                gc.fillRect(x * cellSize, y * cellSize, cellSize, cellSize);
                gc.strokeRect(x * cellSize, y * cellSize, cellSize, cellSize);
            }
        }
    }

    private void drawAgent() {
        gc.setFill(board.agent.color);
        gc.setStroke(Color.BLACK);
        gc.setLineWidth(1);

        int start = board.agent.x;
        int stop = start + board.agent.size;
        for (int x = start; x < stop; x++) {
            gc.fillRect((x % Board.BOARD_WIDTH) * cellSize , board.agent.y * cellSize, cellSize, cellSize);
            gc.strokeRect((x % Board.BOARD_WIDTH) * cellSize, board.agent.y * cellSize, cellSize, cellSize);
        }

        board.agent.color = Color.GOLD;
    }

    private void drawBlock() {
        gc.setStroke(Color.BLACK);
        gc.setLineWidth(1);

        if (board.block.size > 4) gc.setFill(Color.DARKRED);
        else gc.setFill(Color.DARKOLIVEGREEN);

        int start = board.block.x;
        int stop = start + board.block.size;
        for (int x = start; x < stop; x++) {
            gc.fillRect((x % Board.BOARD_WIDTH) * cellSize, board.block.y * cellSize, cellSize, cellSize);
            gc.strokeRect((x % Board.BOARD_WIDTH) * cellSize, board.block.y * cellSize, cellSize, cellSize);
        }
    }
}
