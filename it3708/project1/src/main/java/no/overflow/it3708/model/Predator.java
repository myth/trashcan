package no.overflow.it3708.model;

import no.overflow.it3708.Main;
import no.overflow.it3708.controller.BoidController;

import java.util.ArrayList;

/**
 * Created by Aleksander Skraastad (myth) on 1/28/16.
 * <p>
 * project1 is licenced under the MIT licence.
 */
public class Predator extends Boid {
    public Predator(BoidController ctrl) {
        this.ctrl = ctrl;
        this.flock = ctrl.getFlock();
        this.radius = 5;
        id = OBJECT_ID++;
        position = new Vector(2);
        velocity = new Vector(2);
        this.ctrl.getPredators().add(this);
        this.initializeRandomValues();
    }

    @Override
    public void applyForce() {
        Vector coh = calcCohesion();
        Vector avo = calcObstructionAvoidance();
        Vector ste = calcSteer();
        Vector sep = calcSeparation();
        velocity.add(avo);
        velocity.add(coh);
        velocity.add(ste);
        velocity.add(sep);
        velocity.normalize();
        velocity.multiply(Main.PREDATOR_VELOCITY);
        position.add(velocity);

        correctOutOfBounds();
    }

    private Vector calcSeparation() {
        Vector force = new Vector(2);
        int count = 0;
        int totDist = 0;
        for (Predator b : ctrl.getPredators()) {
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

    private Vector calcSteer() {
        Boid closest = null;
        Vector steer = new Vector(2);
        ArrayList<Boid> eaten = new ArrayList<>();
        for (Boid b : ctrl.getFlock()) {
            double dist = position.distanceTo(b.position);
            if (dist > Main.NEIGHBOR_RADIUS - radius - b.radius) continue;
            if (closest == null || this.position.distanceTo(closest.position) < dist - radius - b.radius) {
                closest = b;
            }


            // "Eat" the boid and remove it from the flock
            if (position.distanceTo(b.position) - radius - b.radius <= 0) {
                eaten.add(b);
                System.out.println("OM NOM NOM (Boids left: " + ctrl.getFlock().size() + ")");
            }
        }
        if (closest != null) {
            steer = Vector.subtract(closest.position, position);
            double dist = steer.length();
            steer.normalize();
            steer.multiply(1 + ((1 / dist) * 10));
        }

        // Remove the "eaten" boids from canvas
        eaten.forEach(b -> ctrl.getFlock().remove(b));

        return steer;
    }
}
