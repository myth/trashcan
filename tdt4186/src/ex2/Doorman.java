package ex2;

import java.nio.BufferOverflowException;

/**
 * This class implements the doorman's part of the
 * Barbershop thread synchronization example.
 */
public class Doorman extends Thread {

	CustomerQueue queue;
	Gui gui;
	private boolean running;

	/**
	 * Creates a new doorman.
	 * @param queue		The customer queue.
	 * @param gui		A reference to the GUI interface.
	 */
	public Doorman(CustomerQueue queue, Gui gui) {
		this.queue = queue;
		this.gui = gui;
		running = false;
	}

	/**
	 * Starts the doorman running as a separate thread.
	 */
	public void startThread() {
		this.running = true;
		this.start();
	}

	/**
	 * Stops the doorman thread.
	 */
	public void stopThread() {
		this.running = false;
	}

	// Add more methods as needed
	@Override
	public void run() {
		while (running) {
			// Display statustext
			this.gui.println("Doorman is waiting for available seat.");

			// Add a new customer to queue
			this.queue.add(new Customer());

			// Display statustext
			this.gui.println("Doorman was notified of available seat.");

			// Set the doorman to sleep
			try {
				this.sleep(Globals.doormanSleep);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}
}
