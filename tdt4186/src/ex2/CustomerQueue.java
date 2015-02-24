package no.overflow.opsys.p2;

import java.nio.BufferOverflowException;
import java.nio.BufferUnderflowException;

/**
 * This class implements a queue of customers as a circular buffer.
 */
public class CustomerQueue {

	private Customer[] buffer;
	private Gui gui;
	private int head, tail;

	/**
	 * Creates a new customer queue.
	 * @param queueLength	The maximum length of the queue.
	 * @param gui			A reference to the GUI interface.
	 */
    public CustomerQueue(int queueLength, Gui gui) {
		this.gui = gui;
		buffer = new Customer[queueLength + 1];
		head = 0;
		tail = 0;
	}

	public void add(Customer c) {
		if (!isFull()) {
			buffer[head++] = c;
			if (head == buffer.length) head = 0;
		}
		else throw new BufferOverflowException();
	}

	public Customer get() {
		if (isEmpty()) throw new BufferUnderflowException();
		else {
			Customer c = buffer[tail++];
			if (tail == buffer.length) tail = 0;
			return c;
		}
	}

	public boolean isEmpty() {
		return head == tail;
	}

	public boolean isFull() {
		if (tail == 0) return head == buffer.length - 1;
		return head == tail - 1;
	}

	public void printQueue() {
		System.out.println("Head: " + head + " Tail: " + tail);
		for (Customer c: buffer) {
			if (c != null) System.out.println(c.getCustomerID());
			else System.out.println("null");
		}
	}

	public static void main(String[] args) {
		CustomerQueue cq = new CustomerQueue(5, null);
		System.out.println("Empty: " + cq.isEmpty());
		cq.add(new Customer());
		cq.add(new Customer());
		cq.add(new Customer());
		cq.add(new Customer());
		cq.add(new Customer());
		cq.printQueue();
		System.out.println("Full: " + cq.isFull());
		cq.get();
		cq.get();
		cq.get();
		cq.get();
		cq.get();
		cq.printQueue();
		System.out.println("Empty: " + cq.isEmpty());
		cq.add(new Customer());
		cq.printQueue();
		cq.get();
		cq.printQueue();
		System.out.println("Empty: " + cq.isEmpty());
		cq.add(new Customer());
		cq.printQueue();
		cq.add(new Customer());
		cq.printQueue();
		cq.add(new Customer());
		cq.printQueue();
		cq.add(new Customer());
		cq.printQueue();
		cq.add(new Customer());
		cq.printQueue();
		System.out.println("Full: " + cq.isFull());
	}
}
