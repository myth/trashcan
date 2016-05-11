package it3708.project5;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.geom.Ellipse2D;
import java.awt.geom.Rectangle2D;
import javax.swing.*;

import it3708.project5.population.Individual;
import org.jfree.chart.axis.NumberAxis;
import org.jfree.chart.axis.NumberTickUnit;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.chart.plot.XYPlot;
import org.jfree.chart.renderer.xy.XYItemRenderer;
import org.jfree.data.xy.XYSeries;
import org.jfree.data.xy.XYSeriesCollection;
import it3708.project5.event.EvolutionEventListener;
import it3708.project5.population.Population;
import org.apache.log4j.PropertyConfigurator;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Created by Aleksander Skraastad (myth) on 4/21/16.
 * <p>
 * project5 is licenced under the MIT licence.
 */
public class Main extends JFrame implements EvolutionEventListener {
    public static final int NUM_GENERATIONS = 10000;
    public static final int NUM_CITIES = 48;
    public static final int POPULATION_SIZE = 200;
    public static final double MUTATION_RATE = 0.5;
    public static final int MUTATION_STRENGTH = 3;
    public static final int TOURNAMENT_SELECTION_K = 5;
    public static final int GUI_GENERATION_UPDATE = 4;
    public static final boolean GUI_LINE_CHART = true;
    public static final boolean GUI_PARETO = true;
    public static final boolean GUI_NON_PARETO = true;

    private static final String title = "MTSP";
    public JFreeChart chart;
    public XYItemRenderer renderer;
    public XYSeriesCollection dataset = new XYSeriesCollection();
    public static Evolution evolution;

    /**
     * Constructs a new application frame.
     *
     * @param title the frame title.
     */
    public Main(String title) {
        super(title);

        // Set up logging
        PropertyConfigurator.configure(Main.class.getClassLoader().getResourceAsStream("config/log4j.properties"));
        Logger log = LoggerFactory.getLogger(Main.class);

        log.info("Initializing Multi-Objective Evolutionary Algorithm solver for MTSP ...");

        Main.evolution = new Evolution();
        Main.evolution.setMain(this);

        // Chart stuff
        final ChartPanel chartPanel = createDemoPanel();
        this.add(chartPanel, BorderLayout.CENTER);

        // Start button
        JPanel control = new JPanel();
        control.add(new JButton(new AbstractAction("Start") {
            @Override
            public void actionPerformed(ActionEvent e) {
                EventQueue.invokeLater(() -> Main.evolution.execute());
            }
        }));
        this.add(control, BorderLayout.SOUTH);
    }

    public XYSeriesCollection createDataset(Population p) {
        dataset.removeAllSeries();
        XYSeries pareto = new XYSeries("Pareto");

        double size = 4.0;
        double delta = size / 2.0;
        Shape rect = new Rectangle2D.Double(-delta, -delta, size, size);
        Shape ellipse = new Ellipse2D.Double(-delta, -delta, size - 2 , size - 2);
        BasicStroke thinStroke = new BasicStroke(
            1.0f, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND,
            1.0f, new float[] {6.0f, 6.0f}, 0.0f
        );
        BasicStroke thickStroke = new BasicStroke(
            3.0f, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND,
            1.0f, new float[] {6.0f, 6.0f}, 0.0f
        );

        if (GUI_PARETO) {
            for (Individual i : p.fronts.get(0)) {
                pareto.add(i.distance, i.cost);
            }
            dataset.addSeries(pareto);
            if (renderer != null) {
                renderer.setSeriesShape(0, rect);
                renderer.setSeriesStroke(0, thickStroke);
            }
        }

        if (GUI_NON_PARETO) {
            for (int x = 1; x < p.fronts.size(); x++) {
                XYSeries front = new XYSeries("Front_" + x);
                for (Individual i : p.fronts.get(x)) {
                    front.add(i.distance, i.cost);
                }
                dataset.addSeries(front);
                if (renderer != null) {
                    int seriesIndex = x;
                    if (!GUI_PARETO) seriesIndex -= 1;
                    renderer.setSeriesShape(seriesIndex, ellipse);
                    renderer.setSeriesStroke(seriesIndex, thinStroke);
                }
            }
        }

        return dataset;
    }

    /**
     * Main program method
     * @param args Command line argument array
     */
    public static void main(String[] args) {
        EventQueue.invokeLater(() -> {
            Main demo = new Main(title);
            demo.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            demo.pack();
            demo.setLocationRelativeTo(null);
            demo.setVisible(true);
        });
    }

    private ChartPanel createDemoPanel() {
        if (GUI_LINE_CHART) {
            chart = ChartFactory.createXYLineChart(
                title,
                "Distance",
                "Cost",
                createDataset(new Population(0)),
                PlotOrientation.VERTICAL,
                true,
                true,
                false
            );
        } else {
            chart = ChartFactory.createScatterPlot(
                title,
                "Distance",
                "Cost",
                createDataset(new Population(0)),
                PlotOrientation.VERTICAL,
                true,
                true,
                false
            );
        }

        XYPlot xyPlot = (XYPlot) chart.getPlot();
        this.renderer = xyPlot.getRenderer();
        NumberAxis domain = (NumberAxis) xyPlot.getDomainAxis();
        domain.setRange(35000, 170000);
        domain.setTickUnit(new NumberTickUnit(10000));
        NumberAxis range = (NumberAxis) xyPlot.getRangeAxis();
        range.setRange(300, 1900);
        range.setTickUnit(new NumberTickUnit(100));

        return new ChartPanel(chart) {
            @Override
            public Dimension getPreferredSize() {
                return new Dimension(800, 550);
            }
        };
    }

    @Override
    public void newGeneration(Population p, int generation) {
        createDataset(p);
    }
}