package ex3;

/**
 * This class contains a lot of public variables that can be updated
 * by other classes during a simulation, to collect information about
 * the run.
 */
public class Statistics
{
	/** The number of processes that have exited the system */
	public long nofCompletedProcesses = 0L;
	/** The number of processes that have entered the system */
	public long nofCreatedProcesses = 0L;
	/** The total time that all completed processes have spent waiting for memory */
	public long totalTimeSpentWaitingForMemory = 0L;
	/** The time-weighted length of the memory queue, divide this number by the total time to get average queue length */
	public long memoryQueueLengthTime = 0L;
	/** The largest memory queue length that has occured */
	public long memoryQueueLargestLength = 0L;

	public long nofSwitchedProcesses=0L;

	public long nofProcessedIoOps=0L;

	public long cpuTimeSpentProcessing=0L;

	public long cpuQueueLargestLength=0L;

	public long ioQueueLargestLength=0L;

	public long nofProcessesPlacedInCpuQueue=0L;

	public long nofProcessesPlacedInIoQueue=0L;

	public long cpuTimeSpentWaiting=0L;

	public long getNofCompletedProcesses() {
		return nofCompletedProcesses;
	}

	public void setNofCompletedProcesses(long nofCompletedProcesses) {
		this.nofCompletedProcesses = nofCompletedProcesses;
	}

	public long getNofCreatedProcesses() {
		return nofCreatedProcesses;
	}

	public void setNofCreatedProcesses(long nofCreatedProcesses) {
		this.nofCreatedProcesses = nofCreatedProcesses;
	}

	public long getTotalTimeSpentWaitingForMemory() {
		return totalTimeSpentWaitingForMemory;
	}

	public void setTotalTimeSpentWaitingForMemory(long totalTimeSpentWaitingForMemory) {
		this.totalTimeSpentWaitingForMemory = totalTimeSpentWaitingForMemory;
	}

	public long getMemoryQueueLengthTime() {
		return memoryQueueLengthTime;
	}

	public void setMemoryQueueLengthTime(long memoryQueueLengthTime) {
		this.memoryQueueLengthTime = memoryQueueLengthTime;
	}

	public long getMemoryQueueLargestLength() {
		return memoryQueueLargestLength;
	}

	public void setMemoryQueueLargestLength(long memoryQueueLargestLength) {
		this.memoryQueueLargestLength = memoryQueueLargestLength;
	}

	public long getNofSwitchedProcesses() {
		return nofSwitchedProcesses;
	}

	public void setNofSwitchedProcesses(long nofSwitchedProcesses) {
		this.nofSwitchedProcesses = nofSwitchedProcesses;
	}

	public long getNofProcessedIoOps() {
		return nofProcessedIoOps;
	}

	public void setNofProcessedIoOps(long nofProcessedIoOps) {
		this.nofProcessedIoOps = nofProcessedIoOps;
	}

	public long getCpuTimeSpentProcessing() {
		return cpuTimeSpentProcessing;
	}

	public void setCpuTimeSpentProcessing(long cpuTimeSpentProcessing) {
		this.cpuTimeSpentProcessing = cpuTimeSpentProcessing;
	}

	public long getCpuQueueLargestLength() {
		return cpuQueueLargestLength;
	}

	public void setCpuQueueLargestLength(long cpuQueueLargestLength) {
		this.cpuQueueLargestLength = cpuQueueLargestLength;
	}

	public long getIoQueueLargestLength() {
		return ioQueueLargestLength;
	}

	public long getNofProcessesPlacedInCpuQueue() {
		return nofProcessesPlacedInCpuQueue;
	}

	public void setNofProcessesPlacedInCpuQueue(long nofProcessesPlacedInCpuQueue) {
		this.nofProcessesPlacedInCpuQueue = nofProcessesPlacedInCpuQueue;
	}

	public long getNofProcessesPlacedInIoQueue() {
		return nofProcessesPlacedInIoQueue;
	}

	public void setNofProcessesPlacedInIoQueue(long nofProcessesPlacedInIoQueue) {
		this.nofProcessesPlacedInIoQueue = nofProcessesPlacedInIoQueue;
	}

	public long getCpuTimeSpentWaiting() {
		return cpuTimeSpentWaiting;
	}

	public void setCpuTimeSpentWaiting(long cpuTimeSpentWaiting) {
		this.cpuTimeSpentWaiting = cpuTimeSpentWaiting;
	}

	public long getIoTimeSpentWaiting() {
		return ioTimeSpentWaiting;
	}

	public void setIoTimeSpentWaiting(long ioTimeSpentWaiting) {
		this.ioTimeSpentWaiting = ioTimeSpentWaiting;
	}

	public long getIoTimeSpentIn() {
		return ioTimeSpentIn;
	}

	public void setIoTimeSpentIn(long ioTimeSpentIn) {
		this.ioTimeSpentIn = ioTimeSpentIn;
	}

	public long ioTimeSpentWaiting=0L;

	public long ioTimeSpentIn=0L;


	public void setIoQueueLargestLength(long size) {
		ioQueueLargestLength = size;
	}

	/**
	 * Prints out a report summarizing all collected data about the simulation.
	 * @param simulationLength	The number of milliseconds that the simulation covered.
	 */
	public void printReport(long simulationLength) {
		System.out.println();
		System.out.println("Simulation statistics:");
		System.out.println();
		System.out.println("Number of completed processes:                                "+nofCompletedProcesses);
		System.out.println("Number of created processes:                                  "+nofCreatedProcesses);
		System.out.println("Number of (forced) process switches:						  "+nofSwitchedProcesses);
		System.out.println("Number of processed I/O operations:                           "+nofProcessedIoOps);
		System.out.println("Avarage throughput (processes per second):                    "+(float)nofCompletedProcesses/simulationLength);
		System.out.println();
		System.out.println("Total CPU time spent processing:                              "+cpuTimeSpentProcessing + " ms");
		System.out.println("Fraction of CPU time spent processing:                        "+100*(float)cpuTimeSpentProcessing/simulationLength + " %");
		System.out.println("Total cpu time spent waiting:                                 "+(simulationLength-cpuTimeSpentProcessing) + " ms");
		System.out.println("Fraction of CPU time spent waiting:                           "+100*(float)(simulationLength-cpuTimeSpentProcessing)/simulationLength+ " %");
		System.out.println();
		System.out.println("Largest occuring memory queue length:                         "+memoryQueueLargestLength);
		System.out.println("Average memory queue length:                                  "+(float)memoryQueueLengthTime/simulationLength);
		System.out.println("Largest occuring cpu queue length:                            "+ cpuQueueLargestLength);
		System.out.println("Avarage cpu queue length:                                     "+ (float)cpuQueueLargestLength/simulationLength);
		System.out.println("Largest occuring I/O queue length:                            "+ioQueueLargestLength);
		System.out.println("Avarage occuring I/O queue length:                            "+(float)ioQueueLargestLength/simulationLength);
		System.out.println("Average # of times a process has been placed in memory queue: "+1);
		System.out.println("Avarage # of times a process has been placed in cpu queue:    "+nofProcessesPlacedInCpuQueue/nofCreatedProcesses);
		System.out.println("Avarage # of times a process has been placed in I/O queue:    "+nofProcessesPlacedInIoQueue/nofCreatedProcesses);
		System.out.println();
		System.out.println("Avarage time spent in system per process:                     "+(float)simulationLength/nofCreatedProcesses+" ms");
		System.out.println("Average time spent waiting for memory per process:            "+
				totalTimeSpentWaitingForMemory/nofCompletedProcesses+" ms");
		System.out.println("Average time spent waiting for cpu per process:               "+(float)(simulationLength-cpuTimeSpentProcessing)/nofCreatedProcesses+" ms");
		System.out.println("Avarage time spent processing per process:                    "+(float)cpuTimeSpentProcessing/simulationLength+" ms");
		System.out.println("Avarage time spent waiting for I/O per process:               "+(float)ioTimeSpentWaiting/simulationLength+ " ms");
		System.out.println("Avarage time spent in I/O per process:                        "+(float)ioTimeSpentIn/simulationLength+" ms");
	}
}
