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
    private Process activeJob;
    private Statistics statistics;
    private long maxCpuTime;

    public CPU(Queue queue, Simulator simulator, Gui gui, Memory memory, Statistics statistics, long maxCpuTime) {
        this.queue = queue;
        this.simulator = simulator;
        this.gui = gui;
        this.memory = memory;
        this.statistics = statistics;
        this.maxCpuTime = maxCpuTime;
    }

    public void addProcessToQueue(Process p) {
        queue.insert(p);
        p.setTimeOfLastEvent(simulator.getClock());
        p.setNofTimesInReadyQueue(p.getNofTimesInReadyQueue() + 1);

        if (queue.getQueueLength() > statistics.cpuQueueLargestLength) statistics.cpuQueueLargestLength = queue.getQueueLength();
        statistics.nofProcessesPlacedInCpuQueue++;
    }

    public void executeProcess() {
        Simulator.debug("CPU", "Clock: " + simulator.getClock());
        // Setup
        long cpuTime = 0L;
        Process p = (Process) queue.removeNext();
        Simulator.debug("CPU", "Queue Size: " + this.queue.getQueueLength());
        Simulator.debug("CPU", "Executing job on process " + p.getProcessId() + " (Time left: " + p.getCpuTimeNeeded() + " ms. " +
            "Time until next I/O: " + p.getTimeToNextIoOperation() + ")");
        gui.setCpuActive(p);
        p.setTimeSpentInReadyQueue(p.getTimeSpentInReadyQueue() + simulator.getClock() - p.getTimeOfLastEvent());

        /* What will happen with this process? */
        // Will it terminate during this cycle?
        if (p.getCpuTimeNeeded() < p.getTimeToNextIoOperation() && p.getCpuTimeNeeded() < maxCpuTime) {

            Simulator.debug("CPU", "Process " + p.getProcessId() + " will terminate this cycle.");

            // Update the time spent in CPU
            cpuTime = p.getCpuTimeNeeded();
            p.setTimeSpentInCpu(p.getTimeSpentInCpu() + cpuTime);

            // Insert an event that should call end_process after this time has passed
            simulator.fireEvent(Constants.END_PROCESS, simulator.getClock() + cpuTime);

            memory.processCompleted(p);

            return;

        // We will encounter either an I/O operation or force switch
        } else {

            // Will there be an I/O operation?
            if (p.getTimeToNextIoOperation() < maxCpuTime && p.getTimeToNextIoOperation() < p.getCpuTimeNeeded()) {

                Simulator.debug("CPU", "Process " + p.getProcessId() + " must perform I/O.");

                // Set the cpuTime
                cpuTime = p.getTimeToNextIoOperation();

                // Set the time spent in CPU
                p.setTimeSpentInCpu(p.getTimeSpentInCpu() + cpuTime);

                // Add the process to I/O queue
                io.addProcessToQueue(p);

                // Reduce CPU time needed
                p.setCpuTimeNeeded(p.getCpuTimeNeeded() - cpuTime);

                // Fire the event
                simulator.fireEvent(Constants.IO_REQUEST, simulator.getClock() + cpuTime);

            } else if (p.getCpuTimeNeeded() > maxCpuTime && p.getTimeToNextIoOperation() > maxCpuTime) {
                // We will have a forced process switch

                Simulator.debug("CPU", "Process " + p.getProcessId() + " will be force-switched.");

                // Set the cpuTime
                cpuTime = maxCpuTime;

                // Set the time spent
                p.setTimeSpentInCpu(p.getTimeSpentInCpu() + cpuTime);

                // Reduce cpu time needed and time left to next I/O op
                p.setCpuTimeNeeded(p.getCpuTimeNeeded() - cpuTime);
                p.setTimeToNextIoOperation(p.getTimeToNextIoOperation() - cpuTime);

                // Reinsert the process into the queue
                addProcessToQueue(p);

                simulator.fireEvent(Constants.SWITCH_PROCESS, simulator.getClock() + cpuTime);

                // Update statistics
                statistics.nofSwitchedProcesses++;
            } else {
                Simulator.debug("CPU", "WARNING: WE SHOULDN'T BE HERE!");
            }
        }
        p.setTimeOfLastEvent(simulator.getClock());
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