package ex1;

import javax.swing.*;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;

@SuppressWarnings("serial")
public class ButtonsNText extends JPanel {

	private ButtonGroup buttons = new ButtonGroup();
	private JToggleButton UpperCaseButton = new JToggleButton("Uppercase"), LowerCaseButton = new JToggleButton("Lowercase");
	private JCheckBox ContinuousButton = new JCheckBox("Continuous");
	private JTextField TextLine = new JTextField(16);
	public static int CaretPosition = 0;
	
	public static void main(String[] args) {
		JFrame frame = new JFrame("Buttons & Text");
		frame.setContentPane(new ButtonsNText());
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setTitle("Buttons & Text");
		frame.setSize(500, 70);
		frame.pack();
		frame.setVisible(true);
	}
	
	public ButtonsNText() {
		
		buttons.add(UpperCaseButton);
		buttons.add(LowerCaseButton);
		
		TextLine.addKeyListener(new KeyPress());
		TextLine.addMouseListener(new CaretClick());
		UpperCaseButton.addActionListener(new Click());
		LowerCaseButton.addActionListener(new Click());
		
		this.add(TextLine);
		this.add(UpperCaseButton);
		this.add(LowerCaseButton);
		this.add(ContinuousButton);
		
		UpperCaseButton.doClick();
		
	}
	
	public void massageTheText() {
		if (UpperCaseButton.isSelected()) {
			TextLine.setText(TextLine.getText().toUpperCase());
		}
		else {
			TextLine.setText(TextLine.getText().toLowerCase());
		}
	}
	
	public class Click implements ActionListener {
		@Override
		public void actionPerformed(ActionEvent e) {
			massageTheText();
		}
	}
	
	public class CaretClick implements MouseListener {

		@Override
		public void mouseClicked(MouseEvent e) {
			ButtonsNText.CaretPosition = TextLine.getCaretPosition();
		}

		@Override
		public void mousePressed(MouseEvent e) {
			// TODO Auto-generated method stub
			
		}

		@Override
		public void mouseReleased(MouseEvent e) {
			// TODO Auto-generated method stub
			
		}

		@Override
		public void mouseEntered(MouseEvent e) {
			// TODO Auto-generated method stub
			
		}

		@Override
		public void mouseExited(MouseEvent e) {
			// TODO Auto-generated method stub
			
		}
	}
	
	public class KeyPress implements KeyListener {

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
			if (!ContinuousButton.isSelected()) {
				if (e.getKeyCode() == KeyEvent.VK_ENTER) {
					massageTheText();
					TextLine.setCaretPosition(ButtonsNText.CaretPosition);
				}
				else {
					ButtonsNText.CaretPosition = TextLine.getCaretPosition();
				}
				
			}
			else {
				if (e.getKeyCode() == KeyEvent.VK_BACK_SPACE || e.getKeyCode() == KeyEvent.VK_LEFT) {
					ButtonsNText.CaretPosition--;
				}
				else if (e.getKeyCode() == KeyEvent.VK_ENTER){
					// Skeet skeet
				}
				else {
					ButtonsNText.CaretPosition++;
				}
				massageTheText();
				TextLine.setCaretPosition(ButtonsNText.CaretPosition);
			}
			
		}
		
	}
}
