package no.overflow.it3708.project4.world;

import java.util.Random;

/**
 * Created by Aleksander Skraastad (myth) on 4/11/16.
 * <p/>
 * project4 is licenced under the MIT licence.
 */
public class Block {
    public int size;
    public int x;
    public int y;

    public Block() {
        Random rand = new Random();
        size = 1 + rand.nextInt(6);
        y = 0;

        if (Board.WRAP) {
            x = rand.nextInt(Board.BOARD_WIDTH);
        } else {
            x = rand.nextInt(Board.BOARD_WIDTH - size);
        }
    }

    public boolean contains(int i) {
        for (int j = x; j < x + size; j++) {
            if (i == j % Board.BOARD_WIDTH) return true;
        }
        return false;
    }

    public String toString() {
        return "Block{" + x + ", " + y + "} (" + size + ")";
    }
}
