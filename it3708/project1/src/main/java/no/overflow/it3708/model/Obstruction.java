package no.overflow.it3708.model;

import no.overflow.it3708.controller.BoidController;
import org.apache.log4j.Logger;

/**
 * Created by Aleksander Skraastad (myth) on 1/28/16.
 * <p>
 * project1 is licenced under the MIT licence.
 */
public class Obstruction extends Physical {
    private Logger log = Logger.getLogger(Obstruction.class);

    public Obstruction(BoidController ctrl) {
        this.ctrl = ctrl;
        this.radius = 20;
        this.velocity = new Vector(2);
        this.ctrl.getObstructions().add(this);
    }

    /**
     * Sets the position of this obstruction
     * @param x X coordinate
     * @param y Y coordinate
     */
    public void setPosition(int x, int y) {
        this.position = new Vector(new double[]{x, y});
    }
}
