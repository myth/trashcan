package ex3;

/**
 * Created by Aleksander Skraastad (myth) on 4/14/15.
 * <p>
 * TDT4186 is licenced under the MIT licence.
 */
public class IO {
    private Queue queue;
    private Simulator simulator;
    private Gui gui;
    private IO io;
    private Memory memory;
    private Process activeJob;
    private Statistics statistics;
    private long avgIoTime;
    private CPU cpu;

    public IO(Queue queue, Simulator simulator, Gui gui, Memory memory, Statistics statistics, long avgIoTime, CPU cpu) {
        this.queue = queue;
        this.simulator = simulator;
        this.gui = gui;
        this.memory = memory;
        this.statistics = statistics;
        this.avgIoTime = avgIoTime;
        this.activeJob = null;
        this.cpu = cpu;
    }

    public void addProcessToQueue(Process p) {
        p.setNofTimesInIoQueue(p.getNofTimesInIoQueue() + 1);
        Simulator.debug("IO", "Adding process " + p.getProcessId() + " to I/O queue (" + p.getNofTimesInIoQueue() + " times in I/O queue).");
        this.queue.insert(p);

        statistics.nofProcessesPlacedInIoQueue++;
    }

    public void executeProcess() {
        Simulator.debug("IO", "Clock: " + simulator.getClock());
        // Setup
        long ioTime = 0L;
        Process p = (Process) queue.removeNext();
        activeJob = p;
        Simulator.debug("IO", "Executing I/O on process " + p.getProcessId());
        p.setTimeSpentWaitingForIo(p.getTimeSpentWaitingForIo() + simulator.getClock() - p.getTimeOfLastEvent());
        Simulator.debug("IO", "Process " + p.getProcessId() + " waited " + (simulator.getClock() - p.getTimeOfLastEvent()) + " ms. in I/O queue.");

        // Update stats
        statistics.nofProcessedIoOps++;

        // Update the GUI
        this.gui.setIoActive(p);

        // Fire the END_IO event after the I/O is completed.
        simulator.fireEvent(Constants.END_IO, simulator.getClock() + avgIoTime);

        // Update the time
        p.setTimeOfLastEvent(simulator.getClock());
    }

    public void endIoProcess() {
        Simulator.debug("IO", "EndIoProcess called on " + activeJob.getProcessId());

        // Update time spent
        activeJob.setTimeSpentInIo(activeJob.getTimeSpentInIo() + avgIoTime);

        // Add the process back into CPU queue
        cpu.addProcessToQueue(activeJob);

        simulator.fireEvent(Constants.IO_REQUEST, simulator.getClock());
        simulator.fireEvent(Constants.SWITCH_PROCESS, simulator.getClock());

        // Set time of last event
        activeJob.setTimeOfLastEvent(simulator.getClock());
    }
    

    public Queue getQueue() {
        return queue;
    }

    public void setQueue(Queue queue) {
        this.queue = queue;
    }

    public long getAvgIoTime() {
        return this.avgIoTime;
    }

    public Simulator getSimulator() {
        return simulator;
    }

    public void setSimulator(Simulator simulator) {
        this.simulator = simulator;
    }

    public Gui getGui() {
        return gui;
    }

    public void setGui(Gui gui) {
        this.gui = gui;
    }

    public IO getIo() {
        return io;
    }

    public void setIo(IO io) {
        this.io = io;
    }

    public Memory getMemory() {
        return memory;
    }

    public void setMemory(Memory memory) {
        this.memory = memory;
    }

    public Process getActiveJob() {
        return activeJob;
    }

    public void setActiveJob(Process activeJob) {
        this.activeJob = activeJob;
    }

    public Statistics getStatistics() {
        return statistics;
    }

    public void setStatistics(Statistics statistics) {
        this.statistics = statistics;
    }
}
