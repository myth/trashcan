package ex3.listener;

import ex3.PersonPanel;
import ex3.PersonPanelPassiveTwo;
import ex4.PersonListPanel;

public class Listener {
	
	private PersonPanel sniffer = null;
	private PersonListPanel listsniffer = null;
	private PersonPanelPassiveTwo passivesniffer = null;
	
	public void setSniffer(PersonPanel p) {
		sniffer = p;
	}
	
	public void setSniffer(PersonListPanel p) {
		listsniffer = p;
	}
	
	public void setSniffer(PersonPanelPassiveTwo p) {
		passivesniffer = p;
	}
	
	public PersonPanel getSniffer(PersonPanel p) {
		return sniffer;
	}
	
	public PersonListPanel getSniffer() {
		return listsniffer;
	}
	
	public void fireChange() {
		if (sniffer != null) sniffer.changeEvent();
		if (listsniffer != null) listsniffer.changeEvent();
		if (passivesniffer != null) passivesniffer.changeEvent();
	}
}
