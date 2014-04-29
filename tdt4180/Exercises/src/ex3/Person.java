package ex3;

import java.util.ArrayList;
import ex3.listener.ChangeListenerSupport;
import ex3.listener.Listener;

public class Person implements ChangeListenerSupport {
	private String name, dateOfBirth, email;
	private int height;
	private Gender gender;
	private ArrayList<Listener> listeners = new ArrayList<Listener>();
	
	public Person () {
		name = "";
		dateOfBirth = "";
		email = "";
		gender = Gender.MALE;
		height = 120;
	}
	public Person(String name) {
		this.name = name;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
		fireChange();
	}

	public String getDateOfBirth() {
		return dateOfBirth;
	}

	public void setDateOfBirth(String dateOfBirth) {
		this.dateOfBirth = dateOfBirth;
		fireChange();
	}

	public String getEmail() {
		return email;
	}

	public void setEmail(String email) {
		this.email = email;
		fireChange();
	}

	public int getHeight() {
		return height;
	}

	public void setHeight(int height) {
		this.height = height;
		fireChange();
	}

	public Gender getGender() {
		return gender;
	}

	public void setGender(Gender gender) {
		this.gender = gender;
		fireChange();
	}

	public enum Gender {
		MALE, FEMALE;
	}
	
	public void addChangeListener(Listener listener) {
		listeners.add(listener);
	}

	public void removeChangeListener(Listener listener) {
		listeners.remove(listener);
	}

	public void fireChange() {
		for (Listener sniff : listeners) {
			sniff.fireChange();
		}
	}
	
	public String toString() {
		String sname, semail;
		if (name == "") sname = "No name";
		else sname = name;
		if (email == "") semail = "No Email";
		else semail = email;
		return sname + " (" + semail + ")";
	}
	
}
