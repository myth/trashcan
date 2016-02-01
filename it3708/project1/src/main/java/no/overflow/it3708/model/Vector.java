package no.overflow.it3708.model;

/**
 * Created by Aleksander Skraastad (myth) on 1/28/16.
 * <p>
 * project1 is licenced under the MIT licence.
 */
public class Vector {
    private double[] vec;

    /**
     * Construct a vector with N dimensions
     * @param dimensions The number of dimensions
     */
    public Vector(int dimensions) {
        vec = new double[dimensions];
        for (int i = 0; i < dimensions; i++) {
            vec[i] = 0.0;
        }
    }

    /**
     * Construct a vector given an array of doubles
     * @param dimensions An array of doubles containing the magnitudes of each vector component
     */
    public Vector(double[] dimensions) {
        vec = dimensions;
    }

    /**
     * Replace current vector with provided array values
     * @param initVec An array of doubles containing the new vector values
     */
    public void set(double[] initVec) {
        assert(initVec.length == vec.length);
        for (int i = 0; i < vec.length; i ++) {
            vec[i] = initVec[i];
        }
    }

    /**
     * Creates a copy of this vector
     * @return A Vector instance
     */
    public Vector copy() {
        Vector p = new Vector(vec.length);
        p.set(vec);

        return p;
    }

    /**
     * Calculate the distance to another vector
     * @param other An instance of Vector
     * @return The euclidean distance to another vector
     */
    public double distanceTo(Vector other) {
        checkDimensionality(other);

        double compSum = 0.0;
        for (int i = 0; i < vec.length; i++) {
            compSum += Math.pow(vec[i] - other.vec[i], 2);
        }

        return Math.sqrt(compSum);
    }

    /**
     * Returns the length of this Vector
     */
    public double length() {
        double compSum = 0.0;
        for (int i = 0; i < vec.length; i++) {
            compSum += Math.pow(vec[i], 2);
        }

        return Math.sqrt(compSum);
    }

    /**
     * Normalize this vector
     */
    public void normalize() {
        double vecLength = this.length();
        if (vecLength > 0) {
            for (int i = 0; i < vec.length; i++) {
                vec[i] /= vecLength;
            }
        }
    }

    /**
     * Add a vector to this vector
     * @param p A Vector instance
     */
    public void add(Vector p) {
        checkDimensionality(p);

        for (int i = 0; i < vec.length; i++) {
            vec[i] += p.vec[i];
        }
    }

    /**
     * Add two vectors together
     */
    public static Vector add(Vector a, Vector b) {
        Vector v = new Vector(a.vec.length);
        for (int i = 0; i < v.vec.length; i++) {
            v.vec[i] = a.vec[i] + b.vec[i];
        }
        return v;
    }

    /**
     * Subtract a vector from this vector
     * @param p A Vector instance
     */
    public void subtract(Vector p) {
        checkDimensionality(p);

        for (int i = 0; i < vec.length; i ++) {
            vec[i] -= p.vec[i];
        }
    }

    public static Vector subtract(Vector a, Vector b) {
        Vector v = new Vector(a.vec.length);
        for (int i = 0; i < v.vec.length; i++) {
            v.vec[i] = a.vec[i] - b.vec[i];
        }
        return v;
    }

    /**
     * Multiply this vector by a constant
     * @param n An arbitrary real number
     */
    public void multiply(double n) {
        for (int i = 0; i < vec.length; i++) {
            vec[i] *= n;
        }
    }

    public static Vector multiply(Vector a, double n) {
        Vector v = new Vector(a.vec.length);
        for (int i = 0; i < v.vec.length; i++) {
            v.vec[i] = a.vec[i] * n;
        }
        return v;
    }

    /**
     * Multiply this vector by another vector
     * @param other A Vector instance
     */
    public void multiply(Vector other) {
        checkDimensionality(other);

        for (int i = 0; i < vec.length; i++) {
            vec[i] *= other.vec[i];
        }
    }

    /**
     * Divide this vector by a constant
     * @param n An arbitrary constant
     */
    public void divide(double n) {
        for (int i = 0; i < vec.length; i++) {
            vec[i] /= n;
        }
    }

    /**
     * Returns the dot product of this and other vector
     * @param other A Vector instance of the same dimensionality
     * @return The dot product
     */
    public double dot(Vector other) {
        checkDimensionality(other);

        double compSum = 0.0;
        for (int i = 0; i < vec.length; i++) {
            compSum += vec[i] * other.vec[i];
        }

        return compSum;
    }

    public static Vector rotateLeft(Vector v) {
        Vector rotated = new Vector(2);
        rotated.set(new double[]{v.get(1), -v.get(0)});
        return rotated;
    }
    public static Vector rotateRight(Vector v) {
        Vector rotated = new Vector(2);
        rotated.set(new double[]{-v.get(1), v.get(0)});
        return rotated;
    }

    /**
     * Limit this vector by magnitude n, both positively and negatively
     * @param n A maximum magnitude of this vector.
     */
    public void limit(double n) {
        for (int i = 0; i < vec.length; i++) {
            if (vec[i] > n) vec[i] = n;
            if (vec[i] < -1 * n) vec[i] = -1 * n;
        }
    }

    /**
     * Returns the angle between this vector and the other vector
     * @param other A Vector instance
     * @return The angle between the vectors in degrees
     */
    public double angle(Vector other) {
        return Math.acos(this.dot(other) / (this.length() * other.length()));
    }

    /**
     * Get the value of vector component i
     * @param i The component index
     * @return The value of vector component with index i as double
     */
    public double get(int i) {
        if (i < 0 || i >= vec.length) throw new ArrayIndexOutOfBoundsException("Index outside vector dimensions");

        return vec[i];
    }

    // HELPERS

    private void checkDimensionality(Vector other) {
        if (other.vec.length != this.vec.length) {
            throw new IllegalArgumentException("The provided vector dimensions does not match current: " +
                this.vec.length + " != " + other.vec.length);
        }
    }

    public String toString() {
        return "Vector[" + vec[0] + ", " + vec[1] + "]";
    }
}
