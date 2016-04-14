package no.overflow.it3708.project4;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.control.SplitPane;
import javafx.stage.Stage;
import no.overflow.it3708.project4.controller.CoreController;
import org.apache.log4j.Logger;
import org.apache.log4j.PropertyConfigurator;

import java.io.IOException;

/**
 * Created by Aleksander Skraastad (myth) on 4/11/16.
 * <p/>
 * project4 is licenced under the MIT licence.
 */
public class Main extends Application {
    public final static int CANVAS_WIDTH = 814;
    public final static int CANVAS_HEIGHT = 640;

    private final static Logger log = Logger.getLogger(Main.class);

    private Scene scene;
    private Stage stage;
    private SplitPane root;
    private CoreController core;

    @Override
    public void start(Stage primaryStage) throws Exception {
        PropertyConfigurator.configure(getClass().getClassLoader().getResource("config/log4j.properties"));
        log.info("Starting Beer Tracker (Project 4) ...");
        this.stage = primaryStage;
        core = new CoreController();

        loadCanvasAndSetScene();
        configureAndShowStage();

        core.bindKeyListeners(scene);

        log.info("Initialization complete");
    }

    private void configureAndShowStage() {
        stage.setResizable(false);
        stage.setTitle("Beer Tracker (Project 4)");
        stage.show();
    }

    private void loadCanvasAndSetScene() {
        log.info("Loading Canvas.fxml onto primaryStage");
        FXMLLoader loader = new FXMLLoader();
        loader.setLocation(getClass().getClassLoader().getResource("fxml/Canvas.fxml"));

        try {
            root = loader.load();
            core.world = loader.getController();
            core.world.core = core;
        } catch (IOException e) {
            e.printStackTrace();
        }

        scene = new Scene(root);
        scene.getStylesheets().add("css/style.css");
        stage.setScene(scene);
    }


    public static void main(String[] args) {
        launch(args);
    }
}
