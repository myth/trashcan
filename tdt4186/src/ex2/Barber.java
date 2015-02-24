package ex2;

/**
 * This class implements the barber's part of the
 * Barbershop thread synchronization example.
 */
public class Barber extends Thread {

	CustomerQueue queue;
	Gui gui;
	int pos;
	private boolean running;

	/**
	 * Creates a new barber.
	 * @param queue		The customer queue.
	 * @param gui		The GUI.
	 * @param pos		The position of this barber's chair
	 */
	public Barber(CustomerQueue queue, Gui gui, int pos) {
		this.queue = queue;
		this.gui = gui;
		this.pos = pos;
		this.running = false;
	}

	/**
	 * Starts the barber running as a separate thread.
	 */
	public void startThread() {
		running = true;
		this.start();
	}

	/**
	 * Stops the barber thread.
	 */
	public void stopThread() {
		running = false;
	}

	// Add more methods as needed
	@Override
	public void run() {
		while (running) {
			// Update GUI to set Barber to awake state
			this.gui.barberIsAwake(this.pos);

			// Print current state
			this.gui.println("Barber " + this.pos + " is waiting for customer.");

			// Try to fetch a customer from queue
			Customer c = this.queue.get();

			// Print current state
			this.gui.println("Barber " + this.pos + " was notified of new customer.");

			// Fill this barbers chair
			this.gui.fillBarberChair(this.pos, c);

			try {
				// Set the sleep time for barber working
				this.sleep(Globals.barberWork);

				// Print current state
				this.gui.println("Barber " + this.pos + " has finished with customer.");

				// Clear the chair
				this.gui.emptyBarberChair(this.pos);

				// Update the GUI to set barber to sleeping
				this.gui.barberIsSleeping(this.pos);

				// Set the sleep time for barber sleeping
				this.sleep(Globals.barberSleep);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}
}

