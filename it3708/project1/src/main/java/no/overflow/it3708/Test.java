package no.overflow.it3708;

import no.overflow.it3708.controller.BoidController;
import no.overflow.it3708.model.Obstruction;
import no.overflow.it3708.model.Vector;

/**
 * Created by Aleksander Skraastad (myth) on 2/1/16.
 * <p>
 * project1 is licenced under the MIT licence.
 */
public class Test {
    public static void main(String[] args) {
        Vector P = new Vector(2);
        Vector V = new Vector(2);
        Vector C = new Vector(2);
        P.set(new double[]{1, 1});
        C.set(new double[]{4, 4});
        V.set(new double[]{0.9, 1.1});
        double s = 0, t = 0, k = 0;
        V.normalize();

        System.out.println(P);
        System.out.println(V);
        System.out.println(C);
        System.out.println("S:" + s + " T:" + t + " K:" + k);

        s = Vector.subtract(C, P).length();

        System.out.println("S:" + s);
        k = Vector.subtract(C, P).dot(V);
        System.out.println("K:" + k);
        t = Math.sqrt(Math.pow(s, 2) - Math.pow(k, 2));
        System.out.println("T:" + t);
        System.out.println("" + Math.pow(k, 2) + " + " + Math.pow(t, 2) + " (" + (Math.pow(k, 2) + Math.pow(t, 2)) + ") = " + Math.pow(s, 2));
    }
}
