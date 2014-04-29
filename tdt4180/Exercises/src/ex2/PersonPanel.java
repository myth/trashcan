package ex2;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;

import javax.swing.*;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

public class PersonPanel extends JPanel {
	
	private static final long serialVersionUID = 1L;
//	private Person model;
	protected Person model;
	private String[] genderlist = {"Male", "Female"};
	
	private JLabel name = new JLabel("Navn: ");
	protected JTextField namefield = new JTextField(25);
	private JLabel email = new JLabel("Email: ");
	protected JTextField emailfield = new JTextField(25);
	private JLabel birthdate = new JLabel("Birthday: ");
	protected JTextField birthdatefield = new JTextField(25);
	private JLabel gender = new JLabel("Gender: ");
	@SuppressWarnings({ "unchecked", "rawtypes" })
	protected JComboBox genderfield = new JComboBox(genderlist);
	private JLabel height = new JLabel("Height: ");
	protected JSlider heightslider = new JSlider(120, 225);

	public PersonPanel() {;
		this.setLayout(new GridBagLayout());
		this.makeThemFields();
		this.model = null;
	}
	
	private void makeThemFields() {
		
		GridBagConstraints c = new GridBagConstraints();

		heightslider.setSize(300, 30);
		
		c.gridx = 0;
		c.gridy = 0;
		c.fill = 2;
		c.weightx = 0.5;
		c.insets = new Insets(10, 10, 10, 10);
		this.add(name, c);
		c.gridx = 1;
		this.add(namefield, c);

		c.gridx = 0;
		c.gridy = 1;
		this.add(email,c);
		c.gridx = 1;
		this.add(emailfield,c);
		
		c.gridx = 0;
		c.gridy = 2;
		this.add(birthdate, c);
		c.gridx = 1;
		this.add(birthdatefield, c);
		
		c.gridx = 0;
		c.gridy = 3;
		this.add(gender, c);
		c.gridx = 1;
		this.add(genderfield, c);
		
		c.gridx = 0;
		c.gridy = 4;
		this.add(height, c);
		c.gridx = 1;
		c.ipady = 40;
		heightslider.setMajorTickSpacing(20);
		heightslider.setMinorTickSpacing(5);
		heightslider.setPaintTicks(true);
		heightslider.setPaintLabels(true);
		this.add(heightslider, c);
		
		namefield.setName("NamePropertyComponent");
		emailfield.setName("EmailPropertyComponent");
		birthdatefield.setName("DateOfBirthPropertyComponent");
		genderfield.setName("GenderPropertyComponent");
		heightslider.setName("HeightPropertyComponent");
		
		bindEventListeners();
	}
	
	private class TextListener implements KeyListener {

		@Override
		public void keyTyped(KeyEvent e) {
			// TODO Auto-generated method stub
			
		}

		@Override
		public void keyPressed(KeyEvent e) {
			// TODO Auto-generated method stub
			
		}

		@Override
		public void keyReleased(KeyEvent e) {
			switch (e.getComponent().getName()) {
			case "NamePropertyComponent":
				model.setName(namefield.getText());
				System.out.println(namefield.getText());
				break;
			case "EmailPropertyComponent":
				model.setEmail(emailfield.getText());
				System.out.println(emailfield.getText());
				break;
			case "DateOfBirthPropertyComponent":
				model.setDateOfBirth(birthdatefield.getText());
				System.out.println(birthdatefield.getText());
				break;
			default:
				// NOOP
			}
		}
		
	}
	
	private void bindEventListeners() {
		namefield.addKeyListener(new TextListener());
		emailfield.addKeyListener(new TextListener());
		birthdatefield.addKeyListener(new TextListener());
		genderfield.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				if (genderfield.getSelectedIndex() == 0) {
					model.setGender(Person.Gender.MALE);
				}
				else {
					model.setGender(Person.Gender.FEMALE);
				}
				System.out.println("Gender selected");
			}
		});
		
		heightslider.addChangeListener(new ChangeListener() {
			@Override
			public void stateChanged(ChangeEvent e) {
				model.setHeight(heightslider.getValue());
				System.out.println(heightslider.getValue());
			}
		});
	}
	
	public void setModel(Person person) {
		this.model = person;
		populateFieldsFromModel();
	}
	
	public Person getModel() {
		return this.model;
	}

	
	public void populateFieldsFromModel() {
		this.namefield.setText(model.getName());
		this.emailfield.setText(model.getEmail());
		this.birthdatefield.setText(model.getDateOfBirth());
		if (model.getGender() == Person.Gender.MALE) {
			this.genderfield.setSelectedIndex(0);
		}
		else {
			this.genderfield.setSelectedIndex(1);
		}
		this.heightslider.setValue(model.getHeight());
	}

	public static void main(String[] args) {
		SwingUtilities.invokeLater(new Runnable() {
			public void run() {
				JFrame window = new JFrame("Test");
				window.setBounds(50, 50, 400, 300);
				window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
				PersonPanel p = new PersonPanel();
				window.setContentPane(p);
				Person person = new Person();
				person.setGender(Person.Gender.MALE);
				person.setDateOfBirth("1987-03-05");
				person.setName("Aleksander Skraastad");
				person.setEmail("aleksans@stud.ntnu.no");
				person.setHeight(175);
				p.setModel(person);
				window.setVisible(true);
			}
		});
	}

}
