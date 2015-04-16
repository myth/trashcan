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
    private boolean working;

    public IO(Queue queue, Simulator simulator, Gui gui, Memory memory, Statistics statistics, long avgIoTime, CPU cpu) {
        this.queue = queue;
        this.simulator = simulator;
        this.gui = gui;
        this.memory = memory;
        this.statistics = statistics;
        this.avgIoTime = avgIoTime;
        this.activeJob = null;
        this.cpu = cpu;
        this.working = false;
    }

    public void addProcessToQueue(Process p) {
        p.setNofTimesInIoQueue(p.getNofTimesInIoQueue() + 1);
        this.queue.insert(p);
        simulator.debug("IO", "Adding process " + p.getProcessId() + " to I/O queue (" + p.getNofTimesInIoQueue() + " times in I/O queue).");
        statistics.nofProcessesPlacedInIoQueue++;
        if (queue.getQueueLength() > statistics.getIoQueueLargestLength()) {
            statistics.setIoQueueLargestLength(queue.getQueueLength());
        }
    }

    public boolean isWorking() {
        return this.working;
    }

    public Process executeNext() {
        // Return null of queue is empty
        if (queue.isEmpty()) return null;

        // Fetch and load the next job
        activeJob = (Process) queue.removeNext();
        simulator.debug("IO", "Setting active job to " + activeJob.getProcessId());
        working = true;

        // Update stats
        activeJob.setTimeSpentWaitingForIo(activeJob.getTimeSpentWaitingForIo() + simulator.getClock() - activeJob.getTimeOfLastEvent());
        // Debug output
        simulator.debug("IO", "Process " + activeJob.getProcessId() + " loaded into IO. (Time waited in queue: " + (simulator.getClock() - activeJob.getTimeOfLastEvent()) + "ms)");
        activeJob.setTimeOfLastEvent(simulator.getClock());
        // Update the GUI
        gui.setIoActive(activeJob);

        // Return the active job
        return activeJob;
    }

    public void stop() {
        simulator.debug("IO", "Stopping process " + activeJob.getProcessId() + " and moving back to CPU queue.");

        // Update statistics
        activeJob.setTimeSpentInIo(activeJob.getTimeSpentInIo() + avgIoTime);
        statistics.nofProcessedIoOps++;

        // Reset the time to next IO
        activeJob.setTimeToNextIoOperation(activeJob.getAvgIoInterval());

        // Re-add to cpuQueue
        cpu.addProcessToQueue(activeJob);

        // If there are more things in CPU queue, load them and fire event
        if (!cpu.isWorking()) {
            Process p = cpu.fetchProcess();
            if (p != null) {
                cpu.generateEvent(p);
                p.setTimeOfLastEvent(simulator.getClock());
            }
        }

        // Update the current job stop event time
        activeJob.setTimeOfLastEvent(simulator.getClock());

        // Check if we have more stuff in ioQueue, if so, load it and fire next event.
        Process p = executeNext();
        if (p != null) {
            simulator.fireEvent(Constants.END_IO, simulator.getClock() + avgIoTime);
            p.setTimeOfLastEvent(simulator.getClock());
        } else {
            // We have no more work for now, reset stuff.
            gui.setIoActive(null);
            working = false;
            activeJob = null;
        }
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

    public void timePassed(long timedelta) {

        if (activeJob != null) simulator.debug("IO-TICK", "Active job: " + activeJob.getProcessId());
        else simulator.debug("IO-TICK", "Active job: " + activeJob);

        if (!working) statistics.ioTimeSpentWaiting += timedelta;
        else statistics.ioTimeSpentIn += timedelta;
    }
}
