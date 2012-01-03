package br.com.thewar.server.lang;

public interface ISubject {
	
	public void attach(IObserver observer);
	
	public void detach(IObserver observer);
	
	public void notifyObservers();
	
}
