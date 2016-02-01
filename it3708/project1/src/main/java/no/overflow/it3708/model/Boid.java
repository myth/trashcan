package no.overflow.it3708.model;

import no.overflow.it3708.Main;
import no.overflow.it3708.controller.BoidController;
import org.apache.log4j.Logger;

import java.util.ArrayList;
import java.util.Random;

public class Boid extends Physical {
    protected static int OBJECT_ID = 0;
    private Logger log = Logger.getLogger(Boid.class);
    protected ArrayList<Boid> flock;
    protected BoidController ctrl;

    public Boid() {}
    public Boid(ArrayList<Boid> flock, BoidController ctrl) {
        this.flock = flock;
        this.ctrl = ctrl;
        radius = Main.BOID_RADIUS;
        id = OBJECT_ID++;

        position = new Vector(2);
        velocity = new Vector(2);

        initializeRandomValues();
        this.flock.add(this);
    }

    public void initializeRandomValues() {
        Random r = new Random();
        double[] pos = new double[]{0.0, 0.0};
        double[] vel = new double[]{0.0, 0.0};
        pos[0] = r.nextDouble() * Main.CANVAS_WIDTH;
        pos[1] = r.nextDouble() * Main.CANVAS_HEIGHT;
        vel[0] = r.nextDouble() * 4 - 2;
        vel[1] = r.nextDouble() * 4 - 2;

        position.set(pos);
        velocity.set(vel);
    }

    public void applyForce() {
        Vector ali = calcAlignment();
        Vector coh = calcCohesion();
        Vector sep = calcSeparation();
        Vector avo = calcObstructionAvoidance();
        Vector fle = calcFlee();

        velocity.add(avo);
        avo.multiply(2);
        velocity.add(ali);
        velocity.add(coh);
        velocity.add(sep);
        velocity.add(fle);

        velocity.normalize();
        velocity.multiply(ctrl.velocity.getValue());
        position.add(velocity);

        correctOutOfBounds();
    }

    public String toString() {
        return "Boid{" + id + "} X:" + position.get(0) + ",Y:" + position.get(1) + " (" + velocity.get(0) + "," + velocity.get(1) + ")";
    }

    // Helpers

    /**
     * Calculate the separation force vector
     * @return A Vector representing the separation force between the boids
     */
    private Vector calcSeparation() {
        Vector force = new Vector(2);
        int count = 0;
        int totDist = 0;
        for (Boid b : flock) {
            if (b == this) continue;
            double dist = this.position.distanceTo(b.position);
            if (dist <= Main.NEIGHBOR_RADIUS) {
                Vector diff = this.position.copy();
                diff.subtract(b.position);
                diff.divide(Math.pow(dist, 2)); // Weight by distance
                force.add(diff);
                count++;
                totDist += dist;
            }
        }

        if (count > 0) {
            force.divide((double) count);
            force.normalize();
            force.multiply(ctrl.separation.getValue());
        }

        return force;
    }

    /**
     * Calculate the cohesion force vector
     * @return A Vector representing the cohesion force between the boids
     */
    protected Vector calcCohesion() {
        Vector sentroid = new Vector(2);
        int count = 0;
        for (Boid b: flock) {
            if (this == b) continue;
            double dist = position.distanceTo(b.position);
            if (dist < Main.NEIGHBOR_RADIUS && dist > 15) {
                sentroid.add(b.position);
                count++;
            }
        }

        if (count > 0) {
            // Calculate average position
            sentroid.divide(count);

            // Create a force vector from current position towards centroid
            Vector current = position.copy();
            sentroid.subtract(current);

            // Normalize and weight by distance and control slider
            sentroid.normalize();
            sentroid.multiply(ctrl.cohesion.getValue()); // Overall weight adjustment
        }

        return sentroid;
    }

    /**
     * Calculate the alignment force vector
     * @return A Vector representing the alignment force between the boids
     */
    protected Vector calcAlignment() {
        Vector alignment = new Vector(2);
        int count = 0;
        for (Boid b : flock) {
            if (b == this) continue;
            double dist = this.position.distanceTo(b.position);
            if (dist < Main.NEIGHBOR_RADIUS) {
                Vector p = b.velocity.copy();
                alignment.add(p);
                count++;
            }
        }

        if (count > 0) {
            alignment.divide(count);
            alignment.normalize();
            alignment.multiply(ctrl.alignment.getValue());
        }

        return alignment;
    }

    protected Vector calcObstructionAvoidance() {
        Vector avoidance = new Vector(2);
        // Fetch the closest obstacle, if any inside neighbor radius
        Obstruction obs = null;
        for (Obstruction o: ctrl.getObstructions()) {
            if (obs == null) obs = o;
            if (position.distanceTo(o.position) < Main.NEIGHBOR_RADIUS) {
                if (position.distanceTo(o.position) < position.distanceTo(obs.position)) {
                    obs = o;
                }
            }
        }

        // Abort early if we have no obstacle
        if (obs == null) return avoidance;

        // Set up our vars
        Vector B = new Vector(2);
        Vector P = this.position.copy();
        Vector C = obs.position.copy();
        Vector V = this.velocity.copy();
        V.normalize();
        Vector U;
        double s = this.position.distanceTo(C);
        double r = obs.radius;
        double k = Vector.subtract(C, P).dot(V);
        // Check if we have passed the obstacle
        if (k < 0) {
            return avoidance;
        }
        double t = Math.sqrt(Math.pow(s, 2) - Math.pow(k, 2));

        // Check if we are on a collision course
        if (t < r + 15) {

            Vector left = velocity.copy();
            Vector right = velocity.copy();
            left.add(Vector.rotateLeft(left));
            right.add(Vector.rotateRight(right));

            double angleLeft = Vector.subtract(C, P).dot(left) / Vector.subtract(C, P).length() * left.length();
            double angleRight = Vector.subtract(C, P).dot(right) / Vector.subtract(C, P).length() * right.length();

            if (Math.abs(angleLeft) < Math.abs(angleRight)) {
                avoidance.add(left);
            } else {
                avoidance.add(right);
            }
            avoidance.multiply(1 + Math.abs(.5 / s - radius - obs.radius));
        }

        return avoidance;
    }

    private Vector calcFlee() {
        Vector force = new Vector(2);
        int count = 0;
        for (Predator p : ctrl.getPredators()) {
            double dist = this.position.distanceTo(p.position);
            if (dist - radius * 2 <= Main.NEIGHBOR_RADIUS) {
                Vector diff = this.position.copy();
                diff.subtract(p.position);
                diff.divide(Math.pow(dist, 2)); // Weight by distance
                force.add(diff);
                count++;
            }
        }

        if (count > 0) {
            force.divide((double) count);
            force.normalize();
            force.multiply(ctrl.fear.getValue());
        }

        return force;
    }

    /**
     * Rectifies position of out of bounds
     */
    protected void correctOutOfBounds() {
        double[] vec = new double[]{position.get(0), position.get(1)};
        if (position.get(0) < 0.0) {
            vec[0] = Main.CANVAS_WIDTH + vec[0];
        }
        else if (position.get(0) > Main.CANVAS_WIDTH){
            vec[0] = vec[0] % Main.CANVAS_WIDTH;
        }
        if (position.get(1) < 0.0) {
            vec[1] = Main.CANVAS_HEIGHT + vec[1];
        }
        else if (position.get(1) > Main.CANVAS_HEIGHT) {
            vec[1] = vec[1] % Main.CANVAS_HEIGHT;
        }

        position.set(vec);
    }
}