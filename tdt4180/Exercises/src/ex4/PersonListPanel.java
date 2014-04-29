package ex4;

import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.BorderFactory;
import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.DefaultListModel;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JList;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.ListSelectionModel;
import javax.swing.SwingUtilities;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;

import ex3.Person;
import ex3.Person.Gender;
import ex3.PersonPanelPassive;
import ex3.listener.ChangeListener;
import ex3.listener.Listener;

public class PersonListPanel extends JPanel implements ChangeListener {
	
	private static final long serialVersionUID = 1L;

	private DefaultListModel<Person> listmodel;
	@SuppressWarnings("rawtypes")
	private JList list;
	private PersonPanelPassive personpanel;
	private Person blank = new Person();
	public Listener listener = new Listener();
	
	@SuppressWarnings({ "unchecked", "rawtypes" })
	public PersonListPanel () {
		listmodel = new DefaultListModel();
		list = new JList(listmodel);
		personpanel = new PersonPanelPassive();
	}
	
	@SuppressWarnings("unchecked")
	public void setListLayout() {
		list.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
		list.setSelectedIndex(0);
		list.setVisibleRowCount(15);
		list.setCellRenderer(new PersonRenderer());
		list.setName("PersonList");
		JScrollPane listScrollPane = new JScrollPane(list);
		add(listScrollPane, BorderLayout.CENTER);
		list.addListSelectionListener(new SelectListener());
	}
	
	public void addButtons() {
		JButton add = new JButton("Legg til");
		JButton remove = new JButton("Slett");
		add.setName("NewPersonButton");
		remove.setName("DeletePersonButton");
		JPanel buttonpane = new JPanel();
		buttonpane.setLayout(new FlowLayout(FlowLayout.LEFT));
		buttonpane.add(add);
		buttonpane.add(Box.createHorizontalStrut(10));
		buttonpane.add(remove);
		buttonpane.setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5));
		add(buttonpane);
		add.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				if (listmodel.getSize() == 0) {
					personpanel.enable();
				}
				Person p = new Person();
				p.addChangeListener(listener);
				listmodel.add(0, p);
				list.setSelectedValue(p, true);
				personpanel.setModel(p);
			}
		});
		remove.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				listmodel.removeElement(list.getSelectedValue());
				if (listmodel.getSize() == 0) {
					personpanel.disable();
				}
			}
		});
	}
	
	public void setEditLayout() {
		personpanel.setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5));
		if (personpanel.getModel() == null) {
			personpanel.toggleState();
		}
		add(personpanel);
	}
	
	public void setSniffer(PersonListPanel panel) {
		listener.setSniffer(panel);
	}
	
	public void populateList() {
		Person p = new Person();
		p.setName("Aleksander Skraastad");
		p.setEmail("aleksans@stud.ntnu.no");
		p.setDateOfBirth("1987-03-05");
		p.setGender(Gender.MALE);
		p.setHeight(175);
		listmodel.add(0, p);
		personpanel.setModel(p);
		p.addChangeListener(listener);
		
		p = new Person();
		p.setName("Fredrik T.");
		p.setEmail("freboto@stud.ntnu.no");
		p.setDateOfBirth("1985-02-07");
		p.setGender(Gender.MALE);
		p.setHeight(186);
		listmodel.add(0, p);
		p.addChangeListener(listener);
		
		p = new Person();
		p.setName("Ragnhild Jenssen");
		p.setEmail("r.jensen@gmail.com");
		p.setDateOfBirth("1990-11-21");
		p.setGender(Gender.FEMALE);
		p.setHeight(169);
		listmodel.add(0, p);
		p.addChangeListener(listener);
	}
	
	class SelectListener implements ListSelectionListener {
		@Override
		public void valueChanged(ListSelectionEvent e) {
			try {
				int index = list.getSelectedIndex();
				if (index >= 0 && index < listmodel.getSize()) {
					personpanel.setModel(listmodel.get(index));
					personpanel.enable();
				}
				else {
					if (index >= listmodel.getSize()) {
						index = listmodel.getSize() - 1;
						personpanel.setModel(listmodel.get(index));
						personpanel.enable();
					}
					else {
						personpanel.setModel(blank);
						personpanel.disable();
					}
				}
			}
			catch (Exception ex) {
				System.out.println(ex.getMessage());
			}
		}
	}

	public static void main(String[] args) {
		SwingUtilities.invokeLater(new Runnable() {
			
			public void run () {
				JFrame frame = new JFrame("PersonListPanel");
				frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
				PersonListPanel panel = new PersonListPanel();
				panel.setBorder(BorderFactory.createEmptyBorder(15, 15, 15, 15));
				panel.setSniffer(panel);
				panel.populateList();
				panel.setListLayout();
				panel.setEditLayout();
				panel.setLayout(new BoxLayout(panel, BoxLayout.PAGE_AXIS));
				panel.addButtons();
				panel.setOpaque(true);
				frame.add(panel);
				frame.pack();
				frame.setVisible(true);
			}
		
		});
	}

	public void changeEvent() {
		list.updateUI();
	}
	
}
