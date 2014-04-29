package ex3;

import java.awt.GridBagConstraints;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;

@SuppressWarnings("serial")
public class PersonPanelPassive extends PersonPanel {
	
	private boolean enabled = true;
	private JButton toggle = new JButton("Toggle");
	
	public void addToggleButton () {
		GridBagConstraints c = new GridBagConstraints();
		
		c.gridx = 1;
		c.gridy = 5;
		c.ipadx = 5;
		c.ipady = 5;
		c.fill = 0;
		
		toggle.setName("ToggleButtonComponent");
		this.add(toggle, c);
		
		toggle.addActionListener(new ActionListener () {
			@Override
			public void actionPerformed(ActionEvent e) {
				toggleState();
			}
		});
		
	}
	
	public void toggleState() {
		namefield.setEnabled(!enabled);
		emailfield.setEnabled(!enabled);
		birthdatefield.setEnabled(!enabled);
		genderfield.setEnabled(!enabled);
		heightslider.setEnabled(!enabled);
		enabled = !enabled;
	}
	
	public void disable() {
		enabled = true;
		toggleState();
	}
	
	public void enable() {
		enabled = false;
		toggleState();
	}
	
}
