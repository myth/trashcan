package no.overflow.it3708.model;

import no.overflow.it3708.controller.BoidController;

/**
 * Created by Aleksander Skraastad (myth) on 1/28/16.
 * <p>
 * project1 is licenced under the MIT licence.
 */
public abstract class Physical {
    public Vector position;
    public Vector velocity;
    public double radius;
    public int id;
    protected BoidController ctrl;
}
