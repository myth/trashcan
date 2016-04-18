package no.overflow.it3708.project4.world;

import javafx.scene.paint.Color;
import no.overflow.it3708.project4.nnet.NeuralNetwork;
import org.apache.log4j.Logger;

import java.util.HashSet;

/**
 * Created by Aleksander Skraastad (myth) on 4/11/16.
 * <p/>
 * project4 is licenced under the MIT licence.
 */
public class Board {
    public static Logger log = Logger.getLogger(Board.class);

    public final static int BOARD_WIDTH = 30;
    public final static int BOARD_HEIGHT = 15;
    public static boolean WRAP = true;
    public static boolean PULL = false;
    public int totalBlocks = 0;

    public Agent agent;
    public Block block;

    public Board() {
        agent = new Agent();
        block = new Block();
        totalBlocks++;
    }

    public boolean left(int steps) {
        if (WRAP) {
            agent.x -= steps;
            if (agent.x < 0) {
                agent.x = BOARD_WIDTH - 1;
            }
            return true;
        } else {
            if (agent.x > 0) {
                if (agent.x - steps < 0) agent.x = 0;
                else agent.x -= steps;
                return true;
            }
            return false;
        }
    }

    public boolean right(int steps) {
        if (WRAP) {
            agent.x += steps;
            if (agent.x >= BOARD_WIDTH) {
                agent.x %= BOARD_WIDTH;
            }
            return true;
        } else {
            if (agent.x + agent.size < BOARD_WIDTH) {
                if (agent.x + agent.size + steps >= BOARD_WIDTH) agent.x = BOARD_WIDTH - agent.size;
                else agent.x += steps;
                return true;
            }
            return false;
        }
    }

    public void pull() {
        if (PULL) {
            if (block.y == agent.y) return;
            block.y = BOARD_HEIGHT - 2;
            agent.color = Color.BLUE;
        }
    }

    public void tick() {
        if (block.y == agent.y - 1) {
            double[] sns = sense();
            int offset = 0;
            if (!Board.WRAP) offset = 1;
            double sum = sns[offset]+sns[offset+1]+sns[offset+2]+sns[offset+3]+sns[offset+4];
            if (sum == 0) {
                if (block.size < 5) agent.numMissed += 1;
                else agent.numAvoided += 1;
            }
            else if (sum == block.size) {
                if (block.size < 5) {
                    agent.numCaptured += 1;
                } else {
                    agent.numStruck += 1;
                }
            } else {
                if (block.size < 5) agent.numMissed += 1;
                else agent.numStruck += 1;
            }
            // log.info(block + " reached end! Agent status: " + agent);
            block = new Block();
            totalBlocks++;
        } else {
            block.y++;
        }
    }

    public double[] sense() {
        double[] sense = new double[NeuralNetwork.INPUT_NODES];
        for (int i = 0; i < agent.size; i++) {
            int x = (agent.x + i) % BOARD_WIDTH;
            if (block.contains(x)) sense[i] = 1.0d;
            else sense[i] = 0.0d;
        }

        if (!WRAP) {
            if (agent.x == 0) {
                sense[0] = 2.5d;
            }
            else if (agent.x + agent.size == BOARD_WIDTH) {
                sense[6] = 2.5d;
            }
        }

        return sense;
    }

    public String toString() {
        return agent.toString() + " " + block.toString();
    }
}
