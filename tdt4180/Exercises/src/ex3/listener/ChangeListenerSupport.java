package ex3.listener;

public interface ChangeListenerSupport {
	
	public void addChangeListener(Listener listener);
	public void removeChangeListener(Listener listener);
	public void fireChange();
	
}