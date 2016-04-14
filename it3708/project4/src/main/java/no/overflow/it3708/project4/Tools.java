package no.overflow.it3708.project4;

import java.util.Arrays;

/**
 * Created by Aleksander Skraastad (myth) on 4/12/16.
 * <p/>
 * project4 is licenced under the MIT licence.
 */
public class Tools {
    public static int argMax(double[] arr) {
        double max = Double.NEGATIVE_INFINITY;
        int maxIndex = 0;
        for (int i = maxIndex; i < arr.length; i++) {
            if (arr[i] > max) {
                maxIndex = i;
                max = arr[i];
            }
        }
        return maxIndex;
    }

    public static double[] concat(double[] first, double[] second) {
        double[] result = Arrays.copyOf(first, first.length + second.length);
        System.arraycopy(second, 0, result, first.length, second.length);
        return result;
    }

    public static int moveIntensity(double left, double right) {
        double tot = left + right;
        if (tot == 0) return 2;
        double leftForce = left / tot;
        double rightForce = right / tot;

        double coeff = Math.min(leftForce, rightForce) / Math.max(leftForce, rightForce);

        if (coeff < 0.05) return 4;
        else if (coeff < 0.1) return 3;
        else if (coeff < 0.5) return 2;
        return 1;
    }
}
