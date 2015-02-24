package ex2;

import java.nio.BufferOverflowException;
import java.nio.BufferUnderflowException;

/**
 * This class implements a queue of customers as a circular buffer.
 */
public class CustomerQueue {

	private Customer[] buffer;
	private Gui gui;
	private int head, tail;
	private int customerCount;

	/**
	 * Creates a new customer queue.
	 * @param queueLength	The maximum length of the queue.
	 * @param gui			A reference to the GUI interface.
	 */
    public CustomerQueue(int queueLength, Gui gui) {
		this.gui = gui;
		buffer = new Customer[queueLength];
		head = 0;
		tail = 0;
		this.customerCount = 0;
	}

	/**
	 * Adds a customer to the queue if there is room left.
	 * Updates the GUI and notifies other threads.
	 *
	 * @param c	The customer object to be added
	 */
	public synchronized void add(Customer c) {
		while (isFull()) {
			try {
				// Tell the doorman thread to wait until notified
				wait();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
		// Add the customer and increment  customerCount
		buffer[head] = c;
		customerCount++;

		// Update the GUI
		this.gui.fillLoungeChair(head, c);

		// Increment head
		head++;

		// Reset head if it has reached end of buffer
		if (head == buffer.length) head = 0;

		// Notify other threads of state change
		notifyAll();
	}

	/**
	 * Retrieves a customer if queue is non-empty.
	 * Updates GUI and notifies other threads.
	 */
	public synchronized Customer get() {
		while (isEmpty()) {
			try {
				// Tell the thread to wait until notified
				wait();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
		// Cache the customer
		Customer c = buffer[tail];

		// Decrement customerCount
		customerCount--;

		// Update the GUI
		this.gui.emptyLoungeChair(tail);

		// Increment tail
		tail++;

		// If tail has reached end of buffer, reset.
		if (tail == buffer.length) tail = 0;

		// Notify other threads of state change
		notifyAll();

		// Return the customer
		return c;
	}

	/**
	 * Checks if the queue is empty
	 */
	private boolean isEmpty() {
		return (head == tail && customerCount == 0);
	}

	/**
	 * Checks if the queue is full
	 */
	private boolean isFull() {
		return (head == tail && customerCount != 0);
	}
}
