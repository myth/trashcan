package no.overflow.it3708;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.control.SplitPane;
import javafx.stage.Stage;
import no.overflow.it3708.controller.BoidController;
import org.apache.log4j.Logger;
import org.apache.log4j.PropertyConfigurator;

import java.io.IOException;


public class Main extends Application {

    public static final int GUI_FRAME_INTERVAL = 21; // Milliseconds
    public static final int CANVAS_WIDTH = 623; // 623
    public static final int CANVAS_HEIGHT = 498; // 498
    public static final int NUM_BOIDS = 300;
    public static final double BOID_RADIUS = 2.5;
    public static final int NEIGHBOR_RADIUS = 75;
    public static final double PREDATOR_VELOCITY = 1.2;

    private static final Logger log = Logger.getLogger(Main.class);
    private Stage primaryStage;
    private Scene scene;
    private SplitPane root;
    private BoidController controller;

    @Override
    public void start(Stage primaryStage) throws Exception {
        PropertyConfigurator.configure(getClass().getClassLoader().getResource("config/log4j.properties"));
        log.info("Starting Boids simulator...");
        this.primaryStage = primaryStage;

        loadCanvasAndSetScene();
        configureAndShowStage();
    }

    private void configureAndShowStage() {
        primaryStage.setResizable(false);
        primaryStage.setTitle("Flocking simulator");
        primaryStage.show();
    }

    private void loadCanvasAndSetScene() {
        log.info("Loading Canvas.fxml onto primaryStage");
        FXMLLoader loader = new FXMLLoader();
        loader.setLocation(getClass().getClassLoader().getResource("fxml/Canvas.fxml"));

        try {
            root = loader.load();
            controller = loader.getController();
        } catch (IOException e) {
            e.printStackTrace();
        }

        scene = new Scene(root);
        scene.getStylesheets().add("css/style.css");
        this.primaryStage.setScene(scene);
    }

    public static void main(String[] args) {
        launch(args);
    }
}