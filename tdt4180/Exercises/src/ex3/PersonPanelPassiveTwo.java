package ex3;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;

import javax.swing.*;
import javax.swing.event.ChangeEvent;

import ex3.Person.Gender;
import ex3.listener.ChangeListener;

public class PersonPanelPassiveTwo extends JPanel implements ChangeListener {
	
	private static final long serialVersionUID = 1L;
	private Person model;
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
	protected JTextField genderfield_two = new JTextField(25);
	protected JTextField heightfield = new JTextField(25);


	public PersonPanelPassiveTwo() {;
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
		this.add(genderfield_two, c);
		
		c.gridx = 0;
		c.gridy = 4;
		this.add(height, c);
		c.gridx = 1;
		c.ipady = 40;
		heightslider.setMajorTickSpacing(20);
		heightslider.setMinorTickSpacing(5);
		heightslider.setPaintTicks(true);
		heightslider.setPaintLabels(true);
		this.add(heightfield, c);
		
		namefield.setName("NamePropertyComponent");
		emailfield.setName("EmailPropertyComponent");
		birthdatefield.setName("DateOfBirthPropertyComponent");
		genderfield.setName("GenderPropertyComponent");
		heightslider.setName("HeightPropertyComponent");
		
		bindActionListeners();
	}
	
	public void setModel(Person person) {
		this.model = person;
		populateFieldsFromModel();
	}
	
	public Person getModel() {
		return this.model;
	}
	
	private void populateFieldsFromModel() {
		this.namefield.setText(model.getName());
		this.emailfield.setText(model.getEmail());
		this.birthdatefield.setText(model.getDateOfBirth());
		if (model.getGender() == Person.Gender.MALE) {
			this.genderfield_two.setText("Male");
		}
		else {
			this.genderfield_two.setText("Female");
		}
		this.heightfield.setText(Integer.toString(model.getHeight()));
	}
	
	public void toggleState() {
		namefield.setEnabled(false);
		emailfield.setEnabled(false);
		birthdatefield.setEnabled(false);
		genderfield_two.setEnabled(false);
		heightfield.setEnabled(false);
	}
	
	public class TypeEvent implements KeyListener {
		public void keyTyped(KeyEvent e) {}
		public void keyPressed(KeyEvent e) {}
		public void keyReleased(KeyEvent e) {
			switch (e.getComponent().getName()) {
			case "NamePropertyComponent":
				System.out.println("Name event");
				model.setName(namefield.getText());
				break;
			case "EmailPropertyComponent":
				model.setEmail(emailfield.getText());
				break;
			case "DateOfBirthPropertyComponent":
				model.setDateOfBirth(birthdatefield.getText());
				break;
			}
		}
		
	}

	private void bindActionListeners() {
		TypeEvent kl = new TypeEvent();
		namefield.addKeyListener(kl);
		emailfield.addKeyListener(kl);
		birthdatefield.addKeyListener(kl);
		genderfield.addActionListener(new ActionListener () {
			public void actionPerformed(ActionEvent e) {
				if (genderfield.getSelectedIndex() == 0) {
					model.setGender(Gender.MALE);
				}
				else {
					model.setGender(Gender.FEMALE);
				}
			}
		});
		heightslider.addChangeListener(new javax.swing.event.ChangeListener() {
			public void stateChanged(ChangeEvent e) {
				model.setHeight(heightslider.getValue());	
			}
		});
	}

	@Override
	public void changeEvent() {
		this.populateFieldsFromModel();
	}

}
