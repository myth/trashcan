package ex4;

import java.awt.Color;
import java.awt.Component;
import java.awt.Image;

import javax.swing.DefaultListCellRenderer;
import javax.swing.ImageIcon;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.ListCellRenderer;

import ex3.Person;
import ex3.Person.Gender;

@SuppressWarnings("serial")
public class PersonRenderer extends DefaultListCellRenderer implements ListCellRenderer<Object> {

	ImageIcon male = new ImageIcon(getClass().getResource("male.png"));
	ImageIcon female = new ImageIcon(getClass().getResource("female.png"));
	
	@Override
	public Component getListCellRendererComponent(@SuppressWarnings("rawtypes") JList list, Object value,
			int index, boolean isSelected, boolean cellHasFocus) {
		JLabel label = (JLabel) super.getListCellRendererComponent(list, value, index, isSelected, cellHasFocus);
		Person p = (Person) value;
		label.setText(p.toString());
		if (isSelected) label.setBackground(Color.GREEN);
		if (p.getGender() == Gender.MALE) {
			Image img = male.getImage();
			label.setIcon(new ImageIcon(img));
		}
		else {
			Image img = female.getImage();
			label.setIcon(new ImageIcon(img));
		}
		return label;
	}

}
