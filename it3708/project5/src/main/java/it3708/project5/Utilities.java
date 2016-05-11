package it3708.project5;

import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFSheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.io.*;
import java.util.Random;
import java.util.concurrent.ThreadLocalRandom;

/**
 * Created by Aleksander Skraastad (myth) on 4/21/16.
 * <p>
 * project5 is licenced under the MIT licence.
 */
public class Utilities {

    /**
     * Shuffle the elements of an array in-place using Fisher-Yates shuffle algorithm
     * @param arr An array of shorts.
     */
    public static void FisherYatesShuffle(short[] arr) {
        Random rnd = ThreadLocalRandom.current();
        for (int i = arr.length - 1; i > 0; i--)
        {
            int index = rnd.nextInt(i + 1);
            // Simple swap
            short a = arr[index];
            arr[index] = arr[i];
            arr[i] = a;
        }
    }

    /**
     * Reads in an Excel file from the resources folder
     * @param path The path on the classpath to the Excel document
     */
    public static int[][] ReadExcelFile(String path) {

        int[][] matrix = new int[48][48];

        try {
            FileInputStream file = new FileInputStream(new File(path));
            XSSFWorkbook wb = new XSSFWorkbook(file);

            //Get first/desired sheet from the workbook
            XSSFSheet sheet = wb.getSheetAt(0);

            for (Row row : sheet) {
                if (row.getRowNum() == 0) continue;
                for (Cell cell : row) {
                    if (cell.getColumnIndex() == 0) continue;

                    matrix[row.getRowNum() - 1][cell.getColumnIndex() - 1] = new Double(cell.getNumericCellValue()).intValue();
                    matrix[cell.getColumnIndex() - 1][row.getRowNum() - 1] = new Double(cell.getNumericCellValue()).intValue();

                    if (cell.getColumnIndex() == 49) break;
                }
                if (row.getRowNum() == 49) break;
            }

            file.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return matrix;
    }

    /**
     * Calculates the mean value from a cost or distance matrix
     * @param dataMatrix A two dimensional int array
     * @return The mean value in the matrix
     */
    public static double calculateAverageFromMatrix(int[][] dataMatrix) {
        int sum = 0;
        for (int y = 0; y < dataMatrix.length; y++) {
            for (int x = 0; x < dataMatrix[y].length; x++) {
                sum += dataMatrix[y][x];
            }
        }

        return (double) sum / (dataMatrix.length * dataMatrix.length);
    }

    /**
     * Prints the contents of the provided matrix to stdout
     * @param dataMatrix A two dimensional matrix
     */
    public static void printMatrix(int[][] dataMatrix) {
        for (int y = 0; y < dataMatrix.length; y++) {
            for (int x = 0; x < dataMatrix[y].length; x++) {
                System.out.print(String.format("%d,\t", dataMatrix[y][x]));
            }
            System.out.print("\n");
        }
    }
}
