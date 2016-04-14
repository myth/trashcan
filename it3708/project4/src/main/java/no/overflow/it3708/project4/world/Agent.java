package no.overflow.it3708.project4.world;

import javafx.scene.paint.Color;
import no.overflow.it3708.project4.controller.WorldController;

/**
 * Created by Aleksander Skraastad (myth) on 4/11/16.
 * <p/>
 * project4 is licenced under the MIT licence.
 */
public class Agent {
    public int size = 5;
    public int x = 5;
    public int y = Board.BOARD_HEIGHT - 1;
    public int numCaptured = 0;
    public int numAvoided = 0;
    public int numStruck = 0;
    public int numMissed = 0;
    public Color color = Color.GOLD;

    public String toString() {
        return "Agent{" + x + ", " + y + "} Cap:" + numCaptured + " Avoid:" + numAvoided +
            " Miss:" + numMissed + " Struck:" + numStruck;
    }
}
