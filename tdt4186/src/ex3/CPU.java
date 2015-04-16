package ex3;

/**
 * Created by Aleksander Skraastad (myth) on 4/14/15.
 * <p>
 * TDT4186 is licenced under the MIT licence.
 */
public class CPU {

    private Queue queue;
    private Simulator simulator;
    private Gui gui;
    private IO io;
    private Memory memory;
    private Statistics statistics;
    private long maxCpuTime;
    private Process activeJob;
    private boolean working;

    public CPU(Queue queue, Simulator simulator, Gui gui, Memory memory, Statistics statistics, long maxCpuTime) {
        this.queue = queue;
        this.simulator = simulator;
        this.gui = gui;
        this.memory = memory;
        this.statistics = statistics;
        this.maxCpuTime = maxCpuTime;
        this.working = false;
        this.activeJob = null;
    }

    public void addProcessToQueue(Process p) {
        queue.insert(p);
        p.setNofTimesInReadyQueue(p.getNofTimesInReadyQueue() + 1);
        statistics.nofProcessesPlacedInCpuQueue++;
        if (statistics.cpuQueueLargestLength < queue.getQueueLength()) {
            statistics.cpuQueueLargestLength = queue.getQueueLength();
            simulator.debug("STATS", "UPDATED MAX CPU QUEUE LENGTH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
        }
    }

    public boolean isWorking() {
        return this.working;
    }

    public Process fetchProcess() {
        // Return null of queue is empty
        if (queue.isEmpty()) return null;

        // Fetch and load the next job
        activeJob = (Process) queue.removeNext();
        simulator.debug("CPU", "Setting active job to: " + activeJob.getProcessId());
        working = true;

        // Debug output
        simulator.debug("CPU", "Process " + activeJob.getProcessId() + " loaded into CPU. (Time left: " + activeJob.getCpuTimeNeeded() + "ms)" +
        " (Next I/O: " + activeJob.getTimeToNextIoOperation() + "ms)");

        // Update the gUI
        gui.setCpuActive(activeJob);

        // Return the active job
        return activeJob;
    }

    public void switchProcess() {

        simulator.debug("CPU", "Forcing switch on process: " + activeJob.getProcessId());
        long cpuTime = Math.abs(simulator.getClock() - activeJob.getTimeOfLastEvent());
        activeJob.setTimeSpentInCpu(activeJob.getTimeSpentInCpu() + cpuTime);
        activeJob.setCpuTimeNeeded(activeJob.getCpuTimeNeeded() - cpuTime);
        activeJob.setTimeToNextIoOperation(activeJob.getTimeToNextIoOperation() - cpuTime);
        activeJob.setTimeOfLastEvent(simulator.getClock());

        // Re-add the process to the queue
        addProcessToQueue(activeJob);

        // Update statistics
        statistics.nofSwitchedProcesses++;

        // Stop the CPU
        stop();

        // Fetch next job
        Process p = fetchProcess();

        // If we have a next job, generate a new event
        if (p != null) {
            generateEvent(p);
            p.setTimeOfLastEvent(simulator.getClock());
        }
    }

    public void endProcess() {
        simulator.debug("CPU", "Terminating process: " + activeJob.getProcessId() + " after " + activeJob.getTimeSpentInCpu() + "ms");

        // Update times
        long cpuTime = Math.abs(simulator.getClock() - activeJob.getTimeOfLastEvent());
        activeJob.setTimeSpentInCpu(activeJob.getTimeSpentInCpu() + cpuTime);
        activeJob.setCpuTimeNeeded(activeJob.getCpuTimeNeeded() - cpuTime);

        // Extra negative reset check
        if (activeJob.getCpuTimeNeeded() < 0) activeJob.setCpuTimeNeeded(0L);

        memory.processCompleted(activeJob);
        statistics.nofCompletedProcesses++;
        activeJob.setTimeOfLastEvent(simulator.getClock());

        // Stop current execution
        stop();

        // Fetch next job
        Process p = fetchProcess();

        // If we have a next job, generate a new event
        if (p != null) {
            generateEvent(p);
            p.setTimeOfLastEvent(simulator.getClock());
        }
    }

    public void processIoRequest() {

        simulator.debug("CPU", "Ending process: " + activeJob.getProcessId() + " to perform I/O instead.");

        // Update times
        long cpuTime = Math.abs(simulator.getClock() - activeJob.getTimeOfLastEvent());
        activeJob.setTimeSpentInCpu(activeJob.getTimeSpentInCpu() + cpuTime);
        activeJob.setCpuTimeNeeded(activeJob.getCpuTimeNeeded() - cpuTime);

        io.addProcessToQueue(activeJob);

        // Stop current execution
        stop();

        // Tell I/O to get kicking if it's slacking
        if (!io.isWorking()) {
            Process ioProcess = io.executeNext();
            // If we have
            if (ioProcess != null) {
                // Debug
                simulator.debug("IO", "Executing I/O on process " + ioProcess.getProcessId());

                // Fire the event
                simulator.fireEvent(Constants.END_IO, simulator.getClock() + io.getAvgIoTime());
                ioProcess.setTimeOfLastEvent(simulator.getClock());
            }
        }

        // Fetch next job
        Process p = fetchProcess();

        // If we have a next job, generate a new event
        if (p != null) {
            generateEvent(p);
            p.setTimeOfLastEvent(simulator.getClock());
        }
    }

    public void stop() {
        simulator.debug("CPU", "Stopping execution of process " + activeJob.getProcessId());
        activeJob = null;
        working = false;
        gui.setCpuActive(null);
    }

    public void generateEvent(Process p) {
        // Will the process terminate?
        if (p.getCpuTimeNeeded() < maxCpuTime && p.getCpuTimeNeeded() < p.getTimeToNextIoOperation()) {
            simulator.debug("CPU", "Process " + p.getProcessId() + " will be completed.");
            simulator.fireEvent(Constants.END_PROCESS, simulator.getClock() + p.getCpuTimeNeeded());
        // Will the process be forecfully switched?
        } else if (maxCpuTime < p.getCpuTimeNeeded() && maxCpuTime < p.getTimeToNextIoOperation()) {
            simulator.debug("CPU", "Process " + p.getProcessId() + " will be forcefully switched.");
            simulator.fireEvent(Constants.SWITCH_PROCESS, simulator.getClock() + maxCpuTime);
        // The process will encounter I/O
        } else {
            simulator.debug("CPU", "Process " + p.getProcessId() + " will encounter I/O");
            simulator.fireEvent(Constants.IO_REQUEST, simulator.getClock() + p.getTimeToNextIoOperation());
        }
    }

    public void setIo(IO io) {
        this.io = io;
    }

    public Queue getQueue() {
        return queue;
    }

    public void setQueue(Queue queue) {
        this.queue = queue;
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

    public Memory getMemory() {
        return memory;
    }

    public void setMemory(Memory memory) {
        this.memory = memory;
    }

    public Statistics getStatistics() {
        return statistics;
    }

    public void setStatistics(Statistics statistics) {
        this.statistics = statistics;
    }

    public void timePassed(long timedelta) {

        if (activeJob != null) simulator.debug("CPU-TICK", "Active job: " + activeJob.getProcessId());
        else simulator.debug("CPU-TICK", "Active job: " + activeJob);

        if (!working) statistics.cpuTimeSpentWaiting += timedelta;
        else statistics.cpuTimeSpentProcessing += timedelta;
    }
}