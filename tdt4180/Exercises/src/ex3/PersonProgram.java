package ex3;

import javax.swing.JFrame;
import javax.swing.SwingUtilities;

import ex3.Person.Gender;
import ex3.listener.Listener;

public class PersonProgram {

	public static void main(String[] args) {
		SwingUtilities.invokeLater(new Runnable() {
			
			public void run () {
				JFrame frame = new JFrame("Person Program");
				PersonPanel panel = new PersonPanel();
				Person person = new Person();
				Listener listener = new Listener();
				
				person.setName("Aleksander Skraastad");
				person.setEmail("aleksans@stud.ntnu.no");;
				person.setDateOfBirth("1987-03-05");
				person.setGender(Gender.MALE);
				person.setHeight(175);
				
				panel.setModel(person);
				
				listener.setSniffer(panel);
				
				person.addChangeListener(listener);
				
				frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
				frame.setBounds(50, 50, 400, 300);
				frame.setContentPane(panel);
				frame.setVisible(true);
				
				JFrame frame2 = new JFrame("Person Program");
				PersonPanelPassiveTwo panel2 = new PersonPanelPassiveTwo();
				Listener listener2 = new Listener();
				
				panel2.setModel(person);
				
				listener2.setSniffer(panel2);
				
				person.addChangeListener(listener2);
				
				panel2.toggleState();
				
				frame2.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
				frame2.setBounds(500, 50, 400, 350);
				frame2.setContentPane(panel2);
				frame2.setVisible(true);
			}
			
		});	
	}
}
